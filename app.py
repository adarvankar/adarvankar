from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'kavishree_secret_2024'

DB_PATH = '/tmp/database.db'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'kavishree@123'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            service TEXT NOT NULL,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        phone   = request.form.get('phone', '').strip()
        email   = request.form.get('email', '').strip()
        service = request.form.get('service', '').strip()
        message = request.form.get('message', '').strip()

        if name and phone and service:
            conn = get_db()
            conn.execute(
                'INSERT INTO inquiries (name, phone, email, service, message) VALUES (?,?,?,?,?)',
                (name, phone, email, service, message)
            )
            conn.commit()
            conn.close()
            flash('Thank you! Your inquiry has been submitted. We will contact you shortly.', 'success')
        else:
            flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db()
    inquiries = conn.execute('SELECT * FROM inquiries ORDER BY id DESC').fetchall()
    total = conn.execute('SELECT COUNT(*) FROM inquiries').fetchone()[0]
    conn.close()
    return render_template('admin.html', inquiries=inquiries, total=total)

@app.route('/admin/delete/<int:inquiry_id>')
def delete_inquiry(inquiry_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db()
    conn.execute('DELETE FROM inquiries WHERE id=?', (inquiry_id,))
    conn.commit()
    conn.close()
    flash('Inquiry deleted.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
