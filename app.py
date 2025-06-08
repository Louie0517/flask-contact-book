from flask import Flask, render_template, request, url_for, redirect, session, make_response
from werkzeug.utils import secure_filename
from pathlib import Path
from itsdangerous import URLSafeSerializer
from flask_mail import Mail, Message
import secrets
import sqlite3
import os

app = Flask(__name__)

SECRETE_FILE_PATH =  Path(".flask_secret")
try:
    with SECRETE_FILE_PATH.open('r') as secret_file:
        app.secret_key = secret_file.read()
except FileNotFoundError:
    with SECRETE_FILE_PATH.open('w') as secret_file:
        app.secret_key = secrets.token_hex(32)
        secret_file.write(app.secret_key)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def database_init():
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS owners 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT UNIQUE NOT NULL, 
        password TEXT UNIQUE NULL, 
        image TEXT) 
               ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        image TEXT)
               ''')
    
    conn.commit()
    conn.close()
    print("Database initialized!")
    
    
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_gmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
s = URLSafeSerializer(app.secret_key)

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        with sqlite3.connect("contacts.db") as con:
            user = con.execute("SELECT * FROM owners WHERE email=?", (email,)).fetchone()
            if user:
                token = s.dump(email, salt='recover-password')
                link = url_for('reset_password', token=token, _external=True)
                msg = Message("Password Reset Request", sender="your_gmail@gmail.com", recipients=[email])
                msg.body = f"Click the link to reset your password: {link}"
                mail.send(msg)
                return "A password reset link has been sent to your email."
            else:
                return "Email not found."
        return render_template("forgot_password.html")
    
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = s.load(token, salt='recover_password', max_age = 3600)
    except:
        return "The reset link is invalid or expired."
    
    if request.method == "POST":
        new_password = request.form["password"]
        with sqlite3.connect("contacts.db") as con:
            con.execute("UPDATE owners SET passwords=? WHERE email?", (new_password, email))
            con.commit()
        return redirect(url_for("login"))
    
    return render_template("reset_password.html", token=token)

# USER ACCOUNT 
@app.route("/register", methods=["GET", "POST"])
def register_account():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        owner_image = request.files["image"]
        if owner_image and owner_image.filename != "":
            filename = secure_filename(owner_image.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            owner_image.save(image_path)
            
        else:
            filename = None
        
        try:
            with sqlite3.connect("contacts.db") as con:
                con.execute("INSERT INTO owners (email, password, image) VALUES (?, ?, ?)", (email, password, filename))
                con.commit()
            print("Redirecting to:", url_for("login"))
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
                return render_template("register.html", error="Email already exists.")
                
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    login_attempts = None
    if "login_attemps" not in session:
        session["login_attemps"] = 0
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        remember = "remember" in request.form
        
        if session["login_attemps"] > 5:
            login_attempts = "Too many failed attempts. Please reset your password."
            return redirect(url_for("forgot_password"))
        
        with sqlite3.connect("contacts.db") as con:
            user = con.execute("SELECT * FROM owners WHERE email=? AND password=?", (email, password)).fetchone()
            if user:
                session["user_id"] = user[0]
                session["email"] = user[1]
                resp = make_response(redirect(url_for("list_contacts")))
                if remember:
                    resp.set_cookie("remember_user", email, max_age=60*60*24*30)
                return resp
            else:
                session["login_attempts"] += 1
                error = "Invalid username and password"
            
                
    return render_template("login.html", error=error, success = "Password reset succesful", login_attempts=login_attempts)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register_account"))

@app.route("/edit_account", methods=["GET", "POST"])
def edit_account():
    if "user_id" not in session:
        return redirect(url_for("register_account"))
    
    if request.method == "POST":
        new_username = request.form["username"]
        new_password  = request.form["password"]
        
        with sqlite3.connect("contacts.db") as con:
            con.execute("UPDATE owners SET username=? AND password=? WHERE id=?", (new_username, new_password, session["user_id"]))
            
@app.route("/delete_account")
def delete_account():
    if "user_id" in session:
        with sqlite3.connect("contacts.db") as con:
            con.execute("DELETE FROM owners WHERE id=?", (session["user_id"],))
        session.clear()
    return redirect(url_for("register_account"))

# HOME PAGE
@app.route("/")
def list_contacts():
    if "user_id" not in session:
        return redirect(url_for("register_account"))
    
    con = sqlite3.connect("contacts.db")
    c = con.cursor()
    
    search_contact_number = request.args.get("search")
    if search_contact_number:
        c.execute("SELECT * FROM contacts WHERE phone LIKE ?", ('%' + search_contact_number + '%',))
    else:
       c.execute("SELECT * FROM contacts")
       
    contacts = c.fetchall()
    contact_count = len(contacts)
    con.close()
    return render_template("index.html", contacts=contacts, contact_count=contact_count, search = search_contact_number)

@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        
        if not phone.isdigit() or len(phone) != 10:
            return render_template("add.html", error="Phone number must be exactly 10 digits.")
        
        #SELECT IF SAME EMAIL IN DATABASE
        con = sqlite3.connect("contacts.db")
        c = con.cursor()
        c.execute("SELECT * FROM contacts WHERE email=?", (email,))
        existing_email = c.fetchone()
        
        if existing_email:
            con.close()
            return render_template("add.html", error="Email already exist.")
        
        image_file = request.files["image"]
        if image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            
        else:
            filename = None
        #INSERT NEW CONTACT
        c.execute("INSERT INTO contacts (name, phone, email, address, image) VALUES (?, ?, ?, ?, ?)", (name, phone, email, address, filename))
        con.commit()
        con.close()
        return redirect(url_for("list_contacts"))
    
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    con = sqlite3.connect("contacts.db")
    c = con.cursor()
    
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        
        image_file = request.files["image"]
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            #KEEP IMAGE IF THERE IS NO CHANGES
            c.execute("SELECT image FROM contacts WHERE id=?", (id,))
            filename = c.fetchone()[0]
            
        c.execute("""
                  UPDATE contacts SET name=?, phone=?, email=?, address=?, image=? WHERE id=?
                  """, (name, phone, email, address, filename, id))
        
        con.commit()
        con.close()
        return redirect(url_for("list_contacts"))
    
   
    c.execute("SELECT * FROM contacts WHERE id=?", (id,))
    contact = c.fetchone()
    con.close()
    return render_template("edit.html", contact=contact)
  
@app.route("/delete/<int:id>")
def delete_contact(id):
    con = sqlite3.connect("contacts.db")
    c = con.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("list_contacts"))

@app.route("/routes")
def show_routes():
    return "<br>".join(str(rule) for rule in app.url_map.iter_rules())


if __name__=="__main__":
    database_init()
    app.run(debug=True)