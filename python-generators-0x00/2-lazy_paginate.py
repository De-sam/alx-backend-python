#!/usr/bin/python3
import mysql.connector

def paginate_users(page_size, offset):
    """Fetch a single page of users using LIMIT and OFFSET."""
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="password123",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator that yields one page of users at a time."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# ✅ Expose for ALX checker
lazy_pagination = lazy_paginate
