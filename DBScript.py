import sqlite3

def create_tables():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        emailid TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rides (
        ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ride_giver_name TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        via TEXT,
        departure TIMESTAMP NOT NULL,
        available_seats INTEGER NOT NULL CHECK(available_seats >= 0),
        FOREIGN KEY(ride_giver_name) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()