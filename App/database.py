import sqlite3
from datetime import datetime, timedelta

class Database():
    
    def __init__(self) -> None:
        self.employee_database = 'employee.db'
        self.employee_time_logs = 'time_logs.db'
        self.employee_leave_request = 'employees_request.db'
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
            
    def employee_request(self):
        try:
            with sqlite3.connect(self.employee_leave_request) as db_con:
                cur = db_con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS request (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT,
                    name TEXT,
                    request_type TEXT,
                    date TEXT,
                    details TEXT,
                    department TEXT,
                    status TEXT DEFAULT 'PENDING',
                    action TEXT)''')
                    
                db_con.commit()
        except sqlite3.DatabaseError as e:
            print('Processing Data error', e)
            
        except sqlite3.DataError as e:
            print('Cannot access data', e)

            
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

    def get_request_employee_id(self):
        with sqlite3.connect(self.connect_request_table()) as con:
            cur = con.cursor()
            cur.execute("SELECT request_id FROM request")
            req_id = cur.fetchall()
            required = req_id[0][0] if req_id else None
            return required
        
    def request_exp(self):
        day_one = datetime.now()
        duration = timedelta(days=7)
        
        week = day_one - duration
        
        with sqlite3.connect(self.connect_request_table()) as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM request WHERE date IS NOT NULL AND date < ?''', (week,))
            con.commit()
            
    def check_id(self, employee_id):
        try:
            with sqlite3.connect(self.connect_request_table()) as con:
                cur = con.cursor()
                cur.execute("ATTACH 'employee.db' AS emp")
                cur.execute("SELECT employee_id FROM emp.employee WHERE employee_id=?", (employee_id,))
                result = cur.fetchone()
                print(f"Result from employee.db: {result}")

                cur.execute("DETACH DATABASE emp")
                return bool(result)
        
        except sqlite3.Error as e:
            print(f"Database error in check_id: {e}")
            return False
            
    # connect function    
    def connect_employee(self):
        return self.employee_database
    
    def connect_time_logs(self):
        return self.employee_time_logs
    
    def connect_request_table(self):
        return self.employee_leave_request
            
    def connect_admin_table(self):
        return self.admin_table
    
    def connect_settings(self):
        return self.settings_table
    
if __name__ == "__main__":
    Database()
    
    
