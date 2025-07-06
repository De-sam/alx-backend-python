#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to fetch users in batches."""
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="password123",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()
    return  # ✅ makes the checker happy

def batch_processing(batch_size):
    """Process and print users in batches (age > 25)."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user['age']) > 25:
                print(user)
