from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3 
import subprocess
from Registration import register_user, login_user
from RideManagement import save_ride, search_rides  # Import ride management functions
import traceback

app = Flask(__name__)

# Set a secret key for session management (Change this to a secure, random string)
app.secret_key = 'your_secret_key_here'

# Function to create the database if it doesn't exist
def create_database():
    print("inside db")
    if not os.path.exists('user_data.db'):
        subprocess.run(['python', 'DBScript.py'])

@app.route('/')
def first_page():
    return render_template('first.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get("First Name")
        lastname = request.form.get("Last Name")
        contactno = request.form.get("Contact Number")
        emailid = request.form.get("emailid")
        password = request.form.get("password")
        cnfpassword = request.form.get("confirm-password")

        if password != cnfpassword:
            return render_template('signup.html', message="Passwords do not match.")

        create_database()
        try:
            register_user(firstname, lastname, contactno, emailid, password)
            return redirect(url_for('login_form'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', message="Email already exists.")

    return render_template('signup.html')

    

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    
    if request.method == 'POST':
        email = request.form.get("emailid")
        password = request.form.get("password")
        login_result = login_user(email, password)

        if 'Welcome' in login_result:
            session['username'] = email  # Store logged-in user in session

            # ✅ Fetch and store first name in session
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT first_name FROM users WHERE emailid = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['first_name'] = user[0]
                

            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid password, try again.")

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')  # Ensure home.html exists


@app.route('/logout')
def logout():
    session.pop('username', None)
    response = redirect(url_for('login_form'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/offer', methods=['GET', 'POST'])
def offer_ride():
    if 'username' not in session:
        return redirect(url_for('login_form'))  # Redirect to login if not logged in

    if request.method == 'POST':
        from_place = request.form.get("from")
        to_place = request.form.get("to")
        via = request.form.get("via")
        seats = request.form.get("seats")
        date = request.form.get("date")
        time = request.form.get("time")
        username=session['username']
        # Save ride information to the database
        ride_giver_name= username  # Replace with actual user name from session or database
        save_ride(ride_giver_name, from_place, to_place, via, seats, date, time)

        return render_template('offer.html', message="Ride offered successfully!", username=session['username'])

    return render_template('offer.html', username=session['username'])  # Pass username to HTML

@app.route('/find', methods=['GET', 'POST'])
def find_rides():
    if 'username' not in session:
        return redirect(url_for('login_form'))  # Redirect to login if not logged in

    if request.method == 'POST':
        from_place = request.form.get("from")
        to_place = request.form.get("to")
        find_date = request.form.get("date")
        find_time = request.form.get("time")
        

        # Query the database for available rides
        rides = search_rides(from_place, to_place, find_date, find_time)
        print(rides)
        return render_template('matchingride.html', rides=rides, username=session['username'])

    return render_template('find.html', username=session['username'])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login_form'))

    email = session['username']
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Get data from form
        firstname = request.form.get("first_name")
        lastname = request.form.get("last_name")
        contactno = request.form.get("contact_number")
        
        password = request.form.get("password")

        # Update the profile in the database
        cursor.execute('''
            UPDATE users SET first_name=?, last_name=?, contact_number=?, password=? WHERE emailid=?
        ''', (firstname, lastname, contactno, password, email))
        conn.commit()

        message = "Profile updated successfully!"
    else:
        message = ""

    # Fetch current user info
    cursor.execute('SELECT first_name, last_name, contact_number, emailid, password FROM users WHERE emailid=?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['first_name'] = user[0] 
        return render_template('profile.html',
                               first_name=user[0],
                               last_name=user[1],
                               contact_number=user[2],
                               emailid=user[3],
                               password=user[4],
                               message=message,
                               username=session['username'])
    else:
        return redirect(url_for('login_form'))
    
@app.route('/reduce-seat/<int:ride_id>')
def reduce_seat(ride_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT available_seats FROM rides WHERE ride_id = ?", (ride_id,))
    result = cursor.fetchone()

    if not result:
        return "Ride not found", 404

    seats = result[0]
    if seats <= 0:
        return "No seats available", 400

    cursor.execute("UPDATE rides SET available_seats = available_seats - 1 WHERE ride_id = ?", (ride_id,))
    conn.commit()
    conn.close()

    return "Seat reduced", 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)