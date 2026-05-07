# Kavishree Enterprises – Website

## Quick Setup

```bash
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Pages
- `/`         → Home
- `/about`    → About Us
- `/services` → Services
- `/contact`  → Contact Form
- `/admin`    → Admin Dashboard (login required)

## Admin Login
- Username: `admin`
- Password: `kavishree@123`
**Change these in app.py before deploying!**

## Before Going Live
1. Replace all `+91 99999 99999` with real phone number
2. Replace `info@kavishree.com` with real email
3. Update office address
4. Change admin credentials in app.py
5. Set `debug=False` in app.py
6. Change `app.secret_key` to a random strong string

## Deploy on Render (Free)
1. Push to GitHub
2. Go to render.com → New Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

## Deploy on PythonAnywhere (Free)
1. Upload files via Files tab
2. Create web app → Flask → Python 3.x
3. Set source directory and WSGI file path
