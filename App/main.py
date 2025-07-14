from flask import Flask, redirect, render_template, request, url_for
from database import Database
from datetime import datetime
from dotenv import load_dotenv
from config import Config, get_v
import plotly.graph_objs as gr
import plotly.offline as pyo
import sqlite3, pandas as pd
import json, os

load_dotenv()
app = Flask(__name__)

app.config.from_object(Config)

db : Database = Database()

def database_init():
    db.employee_db()
    db.time_logs()
    db.leave_request()
    db.user_admin_table()
    db.settings()

@app.route('/')  
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    
    if request.method == 'POST':
        
        input_email = request.form['admin_email']
        input_password = request.form['admin_password']
        e_s, p_s = get_v()
    
        with sqlite3.connect(db.connect_admin_table()) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO admin (admin_email, password) VALUES (?, ?)", (input_email, input_password))
            con.commit()
            
            cur.execute("SELECT * FROM admin WHERE admin_email=? AND password=?", (e_s, p_s))
            dis = cur.fetchone()
            
            if dis and len(dis) >= 3:
                verified =  dis[1] ==  input_email and dis[2] == input_password
            
            else:
                verified = False
            
            if verified:
                return redirect('/management')
            else:
                return render_template('admin_login.html', error="Invalid admin details.")
    
    return render_template('admin_login.html')

def get_total_employees():
    con_emp = sqlite3.connect(db.connect_employee())
    con_stats = sqlite3.connect(db.connect_time_logs())
        
    employees = pd.read_sql_query("SELECT * FROM employee", con_emp)
    status = pd.read_sql_query("SELECT * FROM time_logs", con_stats)
        
    con_emp.close()
        
    return employees, status

@app.route('/management', methods=['GET', 'POST'])
def management():
    
    employees, status = get_total_employees()
    
    total_employees = len(employees)
    active_employees = len(status[status['action'] == 'active'])
    lates = len(status[pd.to_datetime(status['status'], format='%H:%M:%S') > pd.to_datetime('9:00:00', format='%H:%M:%S')])
    
    values = [total_employees, active_employees, lates - (total_employees + active_employees)]
    labels = ['Total Employees', 'Active Employees', 'Late Employees']
    donut = gr.Pie(values=values, labels=labels, hole=0.5)
    
    layout = gr.Layout(title="Employee Distribuition", height=500)
    figure = gr.Figure(data=[donut], layout=layout)
    
    chart = pyo.plot(figure, output_type='div', include_plotlyjs=False)
    
    with sqlite3.connect(db.connect_time_logs()) as con:
        cur = con.cursor()
        cur.execute("ATTACH DATABASE 'employee.db' AS emp")
        cur.execute("""SELECT emp.employee.name, emp.employee.department, time_logs.date, time_logs.action 
                    FROM time_logs JOIN emp.employee ON time_logs.id = emp.employee.id ORDER BY time_logs.date DESC
                    """)
        records = cur.fetchall()
    
    return render_template('dash.html', records = records, chart = chart)

# Display in management page
@app.route('/employee_management', methods=['GET', 'POST'])
def employees_management():
    try:
        with sqlite3.connect(db.connect_employee()) as sql_con:
            cur = sql_con.cursor()
            cur.execute('''SELECT employee_id, name, department, email, photo_path FROM employee''')
            updated = cur.fetchall()
            
        
    except sqlite3.Error as e:
        print("Fetch error.", e)
        updated = []
        
    return render_template('e_manage.html', updated=updated)


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        image = db.upload_img()
        
        with sqlite3.connect(db.connect_employee()) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO employee (employee_id, name, department, email, photo_path) VALUE (?, ?, ?, ?)", (id, name, department,email, image))
            con.commit()
            return redirect('/employee_management')
        
    with sqlite3.connect(db.connect_employee()) as con:
        cur = con.cursor()
        cur.execute('''SELECT * FROM employee''')
        show = cur.fetchall()
        
    return render_template('add_employee.html', show=show)

@app.route('/delete_employee_profile/<int:id>', methods=['GET'])
def delete_employee_profile(id):
    database_path = os.path.join(os.path.dirname(__file__), 'employee.db')
    
    with sqlite3.connect(database_path) as con:
        cur = con.cursor()
        cur.execute("ATTACH DATABASE 'time_logs.db' AS t_logs ")
        
        try:
            cur.execute(''' DELETE FROM emloyee WHERE id=?  ''', (id,))
            cur.execute(''' DELETE FROM time_logs WHERE id=?  ''', (id,))
            con.commit()
                    
        except Exception as e:
            print("Error deleting employees profile.", e)
        
        return redirect('/employee_management')
    
    with sqlite3.connect(db.connect_employee()) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT id FROM employee''')
        e_id = cur.fetchall()
        
    return render_template('e_manage.html', employee=e_id)

    

@app.route('/edit_employees_profile', methods=['GET', 'POST'])
def edit_employees_profile():
    
    if request.method == 'POST':
        new_id = request.form.get('new_id', '').strip()
        new_name = request.form.get('new_name', '').strip()
        new_department = request.form.get('new_department', '').strip()
        new_email = request.form.get('new_email').strip()
        new_photo = db.update_img()
        e_id = db.get_user_id()
        tl_id = db.get_time_logs_id()
        
        try:
            with sqlite3.connect(db.connect_employee()) as con:
                cur = con.cursor()
                cur.execute("ATTACH DATABASE 'time_logs.db' AS t_logs ")
                cur.execute('''SELECT e.employee_id, tl.employee_id FROM employee e JOIN
                            t_logs.time_logs tl ON e.employee_id = tl.employee_id WHERE e.id=?''', (e_id,))
                i_matched = cur.fetchone()
                    
                if i_matched:
                        
                    cur.execute('''UPDATE employee SET employee_id=?, name=?, department=?, email=?, photo_path=? 
                                WHERE id=?''', (new_id, new_name, new_department, new_email, new_photo, e_id))
                        
                    cur.execute('''UPDATE time_logs SET employee_id=?, name=? WHERE id=?''', (new_id, new_name, tl_id))
                    con.commit()
                    
                    return redirect('/employees_management')
                    
                cur.execute("DETACH DATABASE time_logs")
                
        except sqlite3.OperationalError as e:
            print("Operational error.", e)
        except sqlite3.Error as e:
            print("SQLite error." , e)
        
    return render_template('edit_e_pf.html')
   
   
if __name__ == "__main__":
    database_init()
    app.run(debug=True)