from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

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

@app.route("/")
def list_contacts():
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