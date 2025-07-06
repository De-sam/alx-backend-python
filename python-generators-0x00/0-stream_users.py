#!/usr/bin/python3
import mysql.connector
import sys

def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="password123",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row

    cursor.close()
    connection.close()

# 👇 This is CRUCIAL: set the module's `__call__` to the function
sys.modules[__name__] = stream_users
