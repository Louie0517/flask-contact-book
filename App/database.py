import sqlite3, os
from flask import Flask, request, url_for
from werkzeug.utils import secure_filename

class Database():
    
    def __init__(self) -> None:
        self.employee_database = 'employee.db'
        self.employee_time_logs = 'time_logs.db'
        self.employee_leave_request = 'leave_request.db'
        self.admin_table = 'admin.db'
        self.settings_table = 'settings.db'
        self.file_path = 'static/employees_img'
        self.app = Flask(__name__)
        

    def employee_db(self):
        try:
            with sqlite3.connect(self.employee_database) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS employee 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            employee_id TEXT, name TEXT, department TEXT,
                            photo_path TEXT)''')
                con.commit()
                
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
    
    
    def time_logs(self):
        try:
            with sqlite3.connect(self.employee_time_logs) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS time_logs 
                            (id INTEGER PRIMARY KEY, employee_id TEXT,
                            name TEXT, date TEXT, time TEXT, action TEXT, status TEXT) ''')
                con.commit()
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
            
    def leave_request(self):
        try:
            with sqlite3.connect(self.employee_leave_request) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS leave_request 
                            (id PRIMARY KEY AUTOINCREMENT, name TEXT,
                            date TEXT, reason TEXT)''')
                con.commit()
        
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
            
            
    def user_admin_table(self):
        try:
            with sqlite3.connect(self.admin_table) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS admin 
                            (id INTEGER PRIMARY KEY, admin_email TEXT,
                            password TEXT, role TEXT)''')
                con.commit()
        
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
            
    def verify_auth(self, email: str, password: str) -> str:
        with sqlite3.connect(self.admin_table) as con:
            cur = con.cursor()
            cur.execute("SELECT FROM admin WHERE admin_email=?, password=? ", (email, password))
            components = cur.fetchone()
            return components and components[0] == email, components[1] == password
   
    def settings(self):
        try:
            with sqlite3.connect(self.settings_table) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS settings 
                            (key TEXT, value TEXT)''')
                con.commit()
                
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
            
    # uploading image
    def upload_img(self):
           self.app.config['EMPLOYEES_FOLDER'] = self.file_path
           file = request.files['employees_photo']
           filename = secure_filename(file.filename)
           file.save(os.path.join(self.app['EMPLOYEES_FOLDER'], filename))
           image_tag =  f'<img src="{url_for("static", filename="uploads/" + filename)}">'
           
           return image_tag
 
    def update_img(self, user_id):
        file = request.files['employees_photo']   
        filename = secure_filename(file.filename)
        file_path = os.path.join(self.app['EMPLOYEES_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.rename(file_path)
            
        file.save(file_path)
        
        def get_user_id():
            with sqlite3.connect('employee.db') as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM employee WHERE employee_id=?")
                id = cur.fetchone()
                return id[0] if id else None
            
        user_id = get_user_id()
        
        with sqlite3.connect('employee.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE employee SET photo_path=? WHERE id=?", (file_path, user_id))
            con.commit()
            
    # connect function    
    def connect_employee(self):
        return self.employee_database
    
    def connect_time_logs(self):
        return self.employee_time_logs
    
    def connect_leave_request(self):
        return self.employee_leave_request
            
    def connect_admin_table(self):
        return self.admin_table
    
    def connect_settings(self):
        return self.settings_table
    
if __name__ == "__main__":
    Database()
    
    
