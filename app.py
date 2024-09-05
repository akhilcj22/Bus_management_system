import hashlib
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_owner_db_connection():
    conn = sqlite3.connect('owner_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the database table
def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

create_table()

def create_owner_table():
    conn = get_owner_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS owners (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

create_owner_table()

def init_db():
    conn = sqlite3.connect('bus_timings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus_timings (
            id INTEGER PRIMARY KEY,
            current_location TEXT NOT NULL,
            desired_location TEXT NOT NULL,
            bus_name TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))  # Redirect to login page after registering
    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect(url_for('search'))  # Redirect to the search results page if credentials match
        else:
            return render_template('index.html', error='Invalid username or password')
    return render_template('index.html')

def update_password(username, new_password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()

# Route for resetting password
@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form['username']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    if new_password == confirm_password:
        # Hash the new password before storing it in the database
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        update_password(username, hashed_password)
        return redirect(url_for('login'))
    else:
        return "Password mismatch error"

@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_owner_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM owners WHERE username = ? AND password = ?', (username, password))
        owner = cursor.fetchone()
        conn.close()
        if owner:
            return redirect(url_for('owner_dashboard', username=username))  # Redirect to owner dashboard with username
        else:
            error = 'Invalid username or password'
            return render_template('owner_login.html', error=error)
    return render_template('owner_login.html')


@app.route('/owner_register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_owner_db_connection()
        cursor = conn.cursor()
        # Check if username already exists
        cursor.execute('SELECT * FROM owners WHERE username = ?', (username,))
        existing_owner = cursor.fetchone()
        if existing_owner:
            error = 'Username already exists. Please choose a different username.'
            conn.close()
            return render_template('owner_register.html', error=error)
        else:
            # Register new owner
            cursor.execute('INSERT INTO owners (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('owner'))  # Redirect to login page after successful registration
    return render_template('owner_register.html')

# Route for the search page
@app.route('/search')
def search():
    return render_template('search.html')

# Route for displaying search results
@app.route('/search_results', methods=['POST'])
def search_results():
    desired_location = request.form['desired_location']
    conn = sqlite3.connect('bus_timings.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT destination, time, bus_name
        FROM bus_timings
        WHERE destination = ?
    """, (desired_location,))
    search_results = cursor.fetchall()
    conn.close()
    if search_results:
        return render_template('search_results.html', search_results=search_results)
    else:
        return render_template('no_results.html')

# Route for submitting feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    # Process the submitted feedback (e.g., save to database)
    # Redirect to the home page after processing
    return redirect(url_for('index'))

@app.route('/owner_dashboard')
def owner_dashboard():
    username = request.args.get('username')  # Get username from query parameter
    if username == 'anjali':
        conn = sqlite3.connect('bus_timings.db')
        cursor = conn.cursor()
        # Update SQL query to select valid columns from the bus_timings table
        cursor.execute('SELECT destination, time, bus_name FROM bus_timings')
        bus_details = cursor.fetchall()
        conn.close()
        return render_template('owner_dashboard.html', bus_details=bus_details)
    else:
        return "Unauthorized access: You are not authorized to view this page."

# Route for the home page (root URL)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/owner')
def owner():
    # Logic for owner page
    return render_template('owner.html')

@app.route('/owner1')
def owner1():
    return render_template('owner1.html')

if __name__ == '__main__':
    app.run(debug=True)