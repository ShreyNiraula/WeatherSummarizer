import sqlite3

# Function to save user to SQLite database
def save_user_to_db(email, username):
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, username TEXT)")

    # Insert user if not already present
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (email, username) VALUES (?, ?)", (email, username))
        conn.commit()
    conn.close()

# Function to fetch all subscribers
def get_all_subscribers():
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    subscribers = cursor.fetchall()
    conn.close()
    return subscribers
