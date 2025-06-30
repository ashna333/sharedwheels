import sqlite3

def register_user(first_name, last_name, contact_number, emailid, password):
    print("inside register")
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (first_name, last_name, contact_number, emailid, password)
    VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, contact_number, emailid, password))
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE emailid = ? AND password = ?
    ''', (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return f"Welcome {user[1]} {user[2]}!"
    else:
        return "Login failed: Invalid email or password"