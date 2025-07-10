from flask import Flask, redirect, render_template, request
from database import Database
from admin_det import admin_details
from datetime import datetime
from key import secret_key
import plotly.graph_objs as gr
import plotly.offline as pyo
import sqlite3, pandas as pd
import json, os

app = Flask(__name__)
app.secret_key = secret_key()

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
    
    email, password = admin_details()
    
    with sqlite3.connect(db.connect_employee) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO admin (username, password, role) VALUE (?, ?, ?)")
        con.commit()
        if db.verify_auth(email, password):
            return redirect('/management')
        else:
            return render_template('admin_login.html', error="Invalid admin details.")
    
    return render_template('admin_login.html')


def get_total_employees():
        con_emp = sqlite3.connect(db.connect_employee)
        con_stats = sqlite3.connect(db.connect_time_logs)
        
        employees = pd.read_sql_query("SELECT * FROM employee", (con_emp, ))
        status = pd.read_sql_query("SELECT * FROM time_logs", (con_stats, ))
        
        con_emp.close()
        con_stats()
        
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
    
    with sqlite3.connect(db.connect_time_logs) as con:
        cur = con.cursor()
        cur.execute("SELECT employee.name, employee.department, time_logs.date, time_logs.action FROM time_logs JOIN employee ON time_logs.employee_id = employee.employee.id ORDER BY table_logs.date DESC")
        records = cur.fetchall()
    
    return render_template('dash.html', records = records, chart = chart)

@app.route('/employee_management', methods=['GET', 'POST'])
def employees_management():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        department = request.form['department']
        image = db.upload_img()
        
        with sqlite3.connect(db.connect_employee) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO employee (employee_id, name, department, photo_path) ", (id, name, department, image))
            con.commit()
            return redirect('/employee_management')
        
    return render_template('e_management.html')

@app.route('/edit_employees_profile', methods=['GET', 'POST'])
def edit_employees_profile():
    
    
    new_id = request.form.get('new_id', '').strip()
    new_name = request.form.get('new_name', '').strip()
    new_department = request.get('new_departmenr', '').strip()
    new_photo = db.update_img()
    
    
    with sqlite3.connect(db.connect_employee) as con:
        cur = con.cursor()
        pass


if __name__ == "__main__":
    database_init()
    app.run(debug=True)