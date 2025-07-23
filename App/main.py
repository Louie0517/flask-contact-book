from flask import Flask, redirect, render_template, request, url_for
from database import Database
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from config import Config, get_v
from werkzeug.utils import secure_filename
from id_generator import rand_id
from datetime import datetime
import plotly.graph_objs as gr
import plotly.offline as pyo
import plotly.express as px
import sqlite3, pandas as pd
import qrcode, os

load_dotenv()
app = Flask(__name__)


app.config.from_object(Config)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'employees_img')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route('/scan')
def scan():
    emp_id = request.args.get('id')
    now = datetime.now()
    time_now = now.strftime('%H:%M:%S')
    date_today = now.strftime('%Y-%m-%d')
    status = ''
    employee_infos = {}
    
    

    with sqlite3.connect(db.connect_time_logs()) as con:
        cur = con.cursor()
        
        cur.execute("ATTACH DATABASE 'employee.db' AS e")
        
        cur.execute('''SELECT tl.date, emp.name, emp.department FROM time_logs AS tl LEFT JOIN e.employee AS emp ON
                    tl.employee_id = emp.employee_id WHERE tl.employee_id=?''',(emp_id,))
        
        infos = cur.fetchone()
        
        if infos:
            employee_infos = {'name': infos[1],
                              'date': infos[0],
                              'department' : infos[2]
                              }
        else:
            employee_infos = None

        cur.execute('''SELECT id, time_in, time_out FROM time_logs WHERE employee_id=? AND date=?''',
                    (emp_id, date_today))
        log = cur.fetchone()

        if not log:
            status = 'IN' if now.hour < 9 else 'LATE'
            cur.execute('''INSERT INTO time_logs (employee_id, date, time_in, action)
                           VALUES (?, ?, ?, ?)''',
                        (emp_id, date_today, time_now, status))
            con.commit()

        elif log and log[1] and not log[2]:
            cur.execute('''UPDATE time_logs SET time_out=?, status='OUT' WHERE id=?''',
                        (time_now, log[0]))
            status = 'OUT'
            con.commit()

        else:
            status = 'ALREADY SCANNED'

    return render_template("scanned.html", status=status, time=time_now, details = employee_infos)

def get_today_logs():
    with sqlite3.connect(db.connect_employee()) as con:
        cur = con.cursor()
        cur.execute("ATTACH DATABASE 'time_logs.db' AS tl")

        cur.execute("""
            SELECT emp.employee_id, emp.name, emp.department,
                   tl.time_logs.date, tl.time_logs.time_in, tl.time_logs.time_out, tl.time_logs.action
            FROM employee AS emp
            LEFT JOIN tl.time_logs
            ON emp.employee_id = tl.time_logs.employee_id
            AND tl.time_logs.date = date('now', 'localtime')
            ORDER BY emp.name
        """)
        
        records = cur.fetchall()
        return [
            {
                "ID": row[0],
                "Name": row[1],
                "Department": row[2],
                "Date": row[3] or 'No log',
                "TimeIn": row[4] or '-',
                "TimeOut": row[5] or '-',
                "Status": row[6] or '-'
            }
            for row in records
        ]

    return records

def generate_qr(emp_id):
    url = f"http://192.168.1.5:5000/scan?id={emp_id}"
    img = qrcode.make(url)
    img.save(f"{emp_id}.png")


def get_total_employees():
    con_emp = sqlite3.connect(db.connect_employee())
    con_stats = sqlite3.connect(db.connect_time_logs())
        
    employees = pd.read_sql_query("SELECT * FROM employee", con_emp)
    status = pd.read_sql_query("SELECT * FROM time_logs", con_stats)
        
    con_emp.close()
        
    return employees, status

def generate_department_line_graph():
    with sqlite3.connect(db.connect_employee()) as con:
        df = pd.read_sql_query("""
            SELECT department, COUNT(*) AS total
            FROM employee
            GROUP BY department
            ORDER BY department
        """, con)

    if df.empty:
        return "<div>No data to display.</div>"

    fig = px.line(df, x='department', y='total', markers=True,
                  title="Number of Employees per Department")
    
    fig.update_layout(xaxis_title='Department',
                      yaxis_title='Employee Count',
                      height=400)

    return pyo.plot(fig, output_type='div', include_plotlyjs=False)



@app.route('/management', methods=['GET', 'POST'])
def management():
    
    employees, status = get_total_employees()
    stats = get_total_employees_and_status()
    
    dept = generate_department_line_graph()
    
    
    total = len(employees)
    
    active_employees =  status[
    (status['time_out'].isna()) | 
    (status['time_out'].astype(str).str.strip() == '') | 
    (status['time_out'].astype(str).str.lower() == 'nan')
    ]
    
    active_count = len(active_employees)

    status['time'] = pd.to_datetime(status['time'], format='%H:%M:%S')

    
    late_threshold = pd.to_datetime('09:00:00', format='%H:%M:%S')

    late_employees = status[status['time'] > late_threshold]
    on_time_employees = status[status['time'] <= late_threshold]

    num_late = len(late_employees)
    num_ontime = len(on_time_employees)

    # Pie chart setup
    values = [num_ontime, num_late, active_count]
    labels = ['On-Time', 'Late', 'Active']
    colors = ["#05C62B", "#EE2D23", "#3498DB"]  

    donut = gr.Pie(values=values, labels=labels, hole=0.5, marker=dict(colors=colors))
    layout = gr.Layout(title="Employee Time & Status Overview", height=460)
    figure = gr.Figure(data=[donut], layout=layout)

    chart = pyo.plot(figure, output_type='div', include_plotlyjs=False)


    
    with sqlite3.connect(db.connect_employee()) as con:
        cur = con.cursor()
        cur.execute("ATTACH DATABASE 'time_logs.db' AS tl")
        cur.execute("""
            SELECT emp.employee_id, emp.name, emp.department, tl.time_logs.date, tl.time_logs.action
            FROM employee AS emp
            LEFT JOIN tl.time_logs ON emp.employee_id = tl.time_logs.employee_id
            AND tl.time_logs.date = date('now', 'localtime')
            ORDER BY emp.name
        """)
        records = get_today_logs()

    
    return render_template('dash.html', employees = records, chart = chart, stats=stats, dept = dept)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    def_id = rand_id()
    ALLOWED_EXTENSIONS = ['png', '.jpeg', 'jpg']
    
    if request.method == 'POST':
        employee_id = request.form['id']
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        '''
        if 'employees_photo' not in request.files:
            return 'No file part.'
        '''
        
        
        file = request.files['employees_photo']
        if file.filename != '':
            if not allowed_file(file.filename):
                return render_template('add_employee.html', e = 'File type not allowed. Please upload a PNG, JPG, or JPEG.', 
                                    random=def_id, form_data={'id': employee_id, 'name': name, 'department': 
                                    department, 'email': email})
                
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            relative_path = f'employees_img/{filename}'
            
        else:
            relative_path = 'employees_img/default.jpg'
            
        
        with sqlite3.connect(db.connect_employee()) as con:
            
            cur = con.cursor()
            cur.execute('''SELECT * FROM employee WHERE email=? ''', (email,))
            duplicates = cur.fetchone()
            
            if duplicates:
                return render_template('add_employee.html', employed=True, random=def_id, 
                                form_data={'id': employee_id, 'name': name, 'department': 
                                department, 'email': email} )
            else:
                cur.execute("INSERT INTO employee (employee_id, name, department, email, photo_path) VALUES (?, ?, ?, ?, ?)", (employee_id, name, department, email, relative_path))
                con.commit()
                return redirect('/employee_management')

    return render_template('add_employee.html', random=def_id)

@app.route('/search_employee', methods=['GET'])
def search_employee():
    iden_num = request.args.get('identification-number')
    name = request.args.get('name')
    department = request.args.get('department')
    email = request.args.get('email')

    filters = []
    values = []

    if iden_num:
        filters.append("employee_id = ?")
        values.append(iden_num)
    if name:
        filters.append("name LIKE ?")
        values.append(f"%{name}%")
    if department:
        filters.append("department = ?")
        values.append(department)
    if email:
        filters.append("email LIKE ?")
        values.append(f"%{email}%")

    where_clause = " AND ".join(filters) if filters else "1=1"

    try:
        with sqlite3.connect(db.connect_employee()) as con:
            cur = con.cursor()
            query = f"""
                SELECT employee_id, name, department, email, photo_path, id
                FROM employee
                WHERE {where_clause}
            """
            cur.execute(query, values)
            results = cur.fetchall()
            
            return render_template('e_manage.html', employee=results,
                       iden_num=iden_num, name=name, department=department, email=email)


    except sqlite3.Error as e:
        print("Fetch error:", e)
        results = []

    return render_template('e_manage.html', employee=results)


# Display and Sort in management page
@app.route('/employee_management')
def employees_management():
    sort_by = request.args.get('sort_by')
    valid_fields = ['name', 'department', 'email']

    query = '''SELECT employee_id, name, department, email, photo_path, id FROM employee'''
    if sort_by in valid_fields:
        query += f' ORDER BY {sort_by} COLLATE NOCASE'

    try:
        with sqlite3.connect(db.connect_employee()) as con:
            cur = con.cursor()
            cur.execute(query)
            employee = cur.fetchall()
    except sqlite3.Error as e:
        print("Fetch error:", e)
        employee = []

    return render_template('e_manage.html', employee=employee, field=sort_by)

def get_total_employees_and_status():
    with sqlite3.connect(db.connect_employee()) as conn:
        df_employees = pd.read_sql_query("SELECT id FROM employee", conn)
        valid_ids = df_employees['id'].tolist()

    with sqlite3.connect(db.connect_time_logs()) as conn:
        df_timein = pd.read_sql_query("SELECT id, time_in AS status FROM time_logs", conn)
        df_timeout = pd.read_sql_query("SELECT id, time_out FROM time_logs", conn)

    df_timein = df_timein[df_timein['id'].isin(valid_ids)]
    df_timeout = df_timeout[df_timeout['id'].isin(valid_ids)]

    df_timein['status'] = pd.to_datetime(df_timein['status'], format='%H:%M:%S', errors='coerce')
    
    ontime = len(df_timein[df_timein['status'] <= pd.to_datetime('09:00:00', format='%H:%M:%S')])
    late = len(df_timein[df_timein['status'] > pd.to_datetime('09:00:00', format='%H:%M:%S')])
    active = len(df_timeout[df_timeout['time_out'].isna() | (df_timeout['time_out'] == '')])

    return {
        'total': len(valid_ids),
        'ontime': ontime,
        'late': late,
        'active': active
    }


@app.route('/delete_employee_profile/<string:id>', methods=['GET'])
def delete_employee_profile(id):
    with sqlite3.connect(db.connect_employee()) as con:
        cur = con.cursor()
        cur.execute("ATTACH DATABASE 'time_logs.db' AS t_logs ")
        
        try:
            cur.execute('DELETE FROM employee WHERE id = ?', (id,))
            cur.execute('DELETE FROM t_logs.time_logs WHERE id = ?', (id,))
            cur.execute('DELETE FROM t_logs.time_in WHERE id = ?', (id,))
            cur.execute('DELETE FROM t_logs.time_out WHERE id = ?', (id,))
            con.commit()
        except Exception as e:
            print("Error deleting employee profile:", e)
        
    return redirect('/employee_management')



def update_img(user_id):
        if 'employees_photo' not in request.files:
            return 'employees_img/default.jpg'

        file = request.files['employees_photo']

        if file.filename == '':
            return 'employees_img/default.jpg'

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['EMPLOYEES_FOLDER'], filename)

        # Optional: Rename if file already exists
        if os.path.exists(file_path):
            base, ext = os.path.splitext(filename)
            count = 1
            while os.path.exists(file_path):
                filename = f"{base}_{count}{ext}"
                file_path = os.path.join(app.config['EMPLOYEES_FOLDER'], filename)
                count += 1

        file.save(file_path)
        relative_path = f'employees_img/{filename}'

        # Update database
        with sqlite3.connect('employee.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE employee SET photo_path=? WHERE id=?", (relative_path, user_id))
            con.commit()

        return relative_path

 
@app.route('/edit_employees_profile/<string:id>', methods=['GET', 'POST'])
def edit_employees_profile(id):
    
    e_id = db.get_user_id(id)
    if not e_id:
        return "Invalid ID", 404
    
    if request.method == 'POST':
        new_id = request.form.get('new_id', '').strip()
        new_name = request.form.get('new_name', '').strip()
        new_department = request.form.get('new_department', '').strip()
        new_email = request.form.get('new_email').strip()
        new_photo = update_img(e_id)
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
            
    
    with sqlite3.connect(db.connect_employee()) as con:
        cur = con.cursor()
        cur.execute('''SELECT * FROM employee WHERE employee_id=?''', (e_id,))
        employee = cur.fetchone()
        employee = [employee] if  employee else []
        
    return render_template('edit_e_pf.html', employee=employee)



if __name__ == "__main__":
    database_init()
    app.run(debug=True)
    # app.run(host="localhost", port=5000)