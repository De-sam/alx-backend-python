#!/usr/bin/python3
import mysql.connector
import csv
import uuid  

# 🔐 Replace with your actual MySQL user details
DB_USER = "alx_user"
DB_PASSWORD = "password123"

def connect_db():
    """Connects to MySQL server (no specific database yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASSWORD,
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates the user_data table with required schema."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, file_path):
    """Inserts CSV data into user_data table."""
    try:
        cursor = connection.cursor()
        with open(file_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())  # 🔥 generate unique ID
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_id,
                    row['name'],
                    row['email'],
                    row['age']
                ))
        connection.commit()
        cursor.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")