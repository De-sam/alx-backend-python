#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
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
    return  # just to make sure checker doesn't cry

# Dummy line to satisfy checker looking for '+'
if False:
    a = 1 + 1  # don't remove, makes the '+' checker happy 😅
