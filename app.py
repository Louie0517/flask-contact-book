from flask import Flask, render_template, request, url_for, redirect, session, make_response
from werkzeug.utils import secure_filename
from pathlib import Path
import secrets
import sqlite3
import os

app = Flask(__name__)

SECRETE_FILE_PATH =  Path(".flask_secret")
try:
    with SECRETE_FILE_PATH.open('r') as secret_file:
        app.secrete_key = secret_file.read()
except FileNotFoundError:
    with SECRETE_FILE_PATH.open('w') as secret_file:
        app.secret_key = secrets.token_hex(32)
        secret_file.write(app.secret_key)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def database_init():
    con = sqlite3.connect("contacts.db")
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address TEXT,
        image TEXT     
    )
    """)
    con.commit()
    con.close()
    
database_init()
# USER ACCOUNT 
@app.route("/register", methods=["GET", "POST"])
def register_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        owner_image = request.files["image"]
        if owner_image and owner_image.filename != "":
            filename = secure_filename(owner_image.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            owner_image.save(image_path)
            
        else:
            filename = None
        
        try:
            with sqlite3.connect("contacts.db") as con:
                con.execute("INSERT INTO owners (username, password, image) VALUES (?, ?, ?)", (username, password, filename))
                con.commit()
                con.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
                return render_template("register.html", error="Username already exists.")
                
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = "request" in request.form
        
        with sqlite3.connect("contacts.db") as con:
            user = con.execute("SELECT * FROM owners WHERE username=? AND password=?", (username, password)).fetchone()
            if user:
                session["user_id"] = user[0]
                session["username"] = user[1]
                resp = make_response(redirect(url_for("list_contacts")))
                if remember:
                    resp.set_cookie("remember_user", username, max_age=60*60*24*30)
                    return resp
            else:
                error = "Invalid username and password"
                
    return render_template("login.html", error=error)
    
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
        
        with sqlite3.connect["contacts.db"] as con:
            con.execute("UPDATE users SET username=? AND password=? WHERE id=?", (new_username, new_password, session["user_id"]))
            
@app.route("/delete_account")
def delete_account():
    if "user_id" in session:
        with sqlite3.connect["contacts.db"] as con:
            con.execute("DELETE FROM users WHERE id=?", (session["user_id"],))
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
            filename = c.fetchall()[0]
            
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

if __name__=="__main__":
    database_init()
    app.run(debug=True)