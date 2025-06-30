# SharedWheels

is a web-based carpooling system where users can share rides, reduce travel costs, and lower carbon emissions. The platform connects drivers who have available seats with passengers traveling the same route.is a web-based carpooling system where users can share rides, reduce travel costs, and lower carbon emissions. The platform connects drivers who have available seats with passengers traveling the same route.
## Features

- User registration and login
- Post rides (drivers)
- Search and book rides (passengers)
- View ride details like date, time, and available seats

## Tech Stack

- HTML, CSS, JavaScript
- Python Flask (Backend)
- SQLite (Database)

## My Role

- Developed backend APIs for posting rides, searching rides, and user authentication
- Built frontend pages using HTML, CSS, and JavaScript
- Designed database schema to store users, rides, and bookings

## Project Structure

```
sharedwheels/
│
├── __pycache__/             # Python cache files
├── instance/                # Instance-specific config or database files
├── static/                  # CSS, JS, images
│     └── style.css
├── templates/               # HTML templates
│     ├── index.html
│     ├── login.html
│     └── ...
├── app.py                   # Main backend app
├── check_columns.py         # Utility script for DB columns
├── DBScript.py              # Database schema setup
├── Registration.py          # User registration logic
├── RideManagement.py        # Ride management logic
├── style.py                 # Additional styling logic (if any)
├── User.py                  # User class and management
├── user_data.db             # User data SQLite DB
└── your_database.db         # Additional database file
```


## How to Run

1. Clone the repository:
    ```
    git clone https://github.com/ashna333/sharedwheels.git
    ```
2. Navigate to the project directory:
    ```
    cd sharedwheels
    ```
3. Install dependencies:
    ```
    pip install flask
    ```
4. Run the Flask app:
    ```
    python app.py
    ```
5. Open your browser and go to:
    ```
    http://localhost:5000
    ```


## Author

Ashna Khalid

