import sqlite3, os
from werkzeug.utils import secure_filename
class Database():
    
    def __init__(self) -> None:
        self.employee_database = 'employee.db'
        self.employee_time_logs = 'time_logs.db'
        self.employee_leave_request = 'leave_request.db'
        self.admin_table = 'admin.db'
        self.settings_table = 'settings.db'        

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
                
                '''
                try:
                    cur.execute("ALTER TABLE time_logs ADD COLUMN time_in TEXT")
                    print("Columns time_in successfully.")
                except sqlite3.OperationalError as e:
                    print("Column time_in already exists", e)
                    
                try:
                    cur.execute("ALTER TABLE time_logs ADD COLUMN time_out TEXT")
                    print("Columns time_out successfully.")
                except sqlite3.OperationalError as e:
                    print("Column time_in already exists", e)
                '''
        
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
            
    def leave_request(self):
        try:
            with sqlite3.connect(self.employee_leave_request) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS leave_request 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
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
    '''      
    def verify_auth(self, email: str, password: str) -> str:
        with sqlite3.connect(self.admin_table) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM admin WHERE admin_email=?, password=? ", (email, password))
            components = cur.fetchone()
            return components and components[0] == email, components[1] == password
    '''
    
    def settings(self):
        try:
            with sqlite3.connect(self.settings_table) as con:
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS settings 
                            (key TEXT, value TEXT)''')
                con.commit()
                
        except sqlite3.OperationalError as e:
            print("Failed to open database", e)
    
    # get employee and time logs id   
    def get_user_id(self, employee_id):
        con = sqlite3.connect(self.connect_employee())  
        cur = con.cursor()
        cur.execute("SELECT id FROM employee WHERE employee_id=?", (employee_id,))
        row = cur.fetchone()
        con.close()
        return row[0] if row else None

    def get_time_logs_id(self):
        with sqlite3.connect(self.connect_time_logs()) as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM employee WHERE employee_id=?")
            id = cur.fetchone()
            return id[0] if id else None

            
            
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
    
    
