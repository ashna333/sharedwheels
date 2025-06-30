import sqlite3

conn = sqlite3.connect('user_data.db')  # Path to your DB file
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(rides)")
columns = cursor.fetchall()

print("Columns in 'rides' table:")
for column in columns:
    print(column)

conn.close()
