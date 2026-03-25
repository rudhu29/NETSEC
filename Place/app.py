from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import redis
import json

app = Flask(__name__)
# Session secure rakhne ke liye ek secret key zaroori hoti hai
app.secret_key = "super_secret_placement_key" 

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 1. THE LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Security Check (Abhi hardcoded hai, real mein DB se check hota hai)
        if username == 'admin' and password == 'superdream':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid Credentials. Try Again!")
            
    return render_template('login.html')

# 2. SECURE DASHBOARD ROUTE
@app.route('/')
def dashboard():
    # Agar user logged in nahi hai, toh wapas login page par bhej do
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# 3. LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.pop('logged_in', None) # Session delete kar do
    return redirect(url_for('login'))

# 4. API ROUTE (Ye pehle jaisa hi hai)
@app.route('/api/logs')
def get_logs():
    # API ko bhi secure kar sakte hain, abhi ke liye simple rakhte hain
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
        
    try:
        logs = r.lrange('recent_logs', 0, 19)
        parsed_logs = [json.loads(log) for log in logs]
        return jsonify(parsed_logs)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("🌐 Secure Server Started at http://localhost:5000")
    app.run(port=5000, debug=True)