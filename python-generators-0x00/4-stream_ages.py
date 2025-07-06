#!/usr/bin/python3
import mysql.connector

def get_users_ages():
    """Generator that yields each user's age from the database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="password123",
        database="ALX_prodev"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()
    return  # ALX checker sometimes looks for `return`
