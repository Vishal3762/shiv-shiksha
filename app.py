import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = '123456'  # Required for session and flash messages

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Default XAMPP password
    database="virtual_classroom"
)
cursor = conn.cursor(dictionary=True)

import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload-content', methods=['GET', 'POST'])
def upload_material():
    if session.get('role') not in ['admin']:
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        uploaded_by = session['username']
        upload_date = datetime.now()

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cursor.execute("""
                INSERT INTO materials (title, description, file_path, uploaded_by, upload_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, description, filename, uploaded_by, upload_date))
            conn.commit()

            flash('Material uploaded successfully.', 'success')
            return redirect(url_for('upload_material'))

    return render_template('upload-content.html')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/view_student')
def view_student():
    if session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM users WHERE role='student'")
    students = cursor.fetchall()
    return render_template('view_student.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        college = request.form['college']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        try:
            cursor.execute("""
                INSERT INTO users (fullname, email, mobile, address, college, username, password, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (fullname, email, mobile, address, college, username, password, role))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError as e:
            flash(f"Error: {e.msg}", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash("Login successful!", "success")

            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'instructor':
                return redirect(url_for('instructor_dashboard'))
            else:
                return redirect(url_for('content'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

@app.route('/content')
def content():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("content.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html")

@app.route('/instructor_dashboard')
def instructor_dashboard():
    if session.get('role') != 'instructor':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))
    return render_template("instructor_dashboard.html")

@app.route('/courses')
def courses():
    if 'username' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    return render_template('courses.html', materials=materials)



@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')
