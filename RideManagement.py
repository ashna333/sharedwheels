import sqlite3

def save_ride(ride_giver_name, from_place, to_place, via, seats, date, time):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO rides (ride_giver_name, origin, destination, via, departure, available_seats)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (ride_giver_name, from_place, to_place, via, f"{date} {time}", seats))  # Assuming ride_giver_id is passed
    conn.commit()
    conn.close()


def search_rides(from_place, to_place, find_date, find_time):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Combine date and time for comparison
    departure_filter = f"{find_date} {find_time}"

    # Query for rides with rider's contact information
    query = '''
    SELECT rides.*, users.contact_number, users.first_name, users.last_name FROM rides
    JOIN users ON rides.ride_giver_name = users.emailid
    WHERE  rides.departure >= ?  AND rides.destination = ? or rides.via =?
    '''
    cursor.execute(query, (departure_filter,to_place,to_place,))
    rides = cursor.fetchall()
    print(rides)
    # Additional queries for indirect rides can be added here...

    conn.close()
    return rides