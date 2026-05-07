from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        service TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

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

        name = request.form['name']
        phone = request.form['phone']
        service = request.form['service']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO inquiries(name, phone, service, message) VALUES (?, ?, ?, ?)",
            (name, phone, service, message)
        )

        conn.commit()
        conn.close()

        return redirect('/contact')

    return render_template('contact.html')

@app.route('/admin')
def admin():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM inquiries ORDER BY id DESC")
    inquiries = cur.fetchall()

    conn.close()

    return render_template('admin.html', inquiries=inquiries)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)