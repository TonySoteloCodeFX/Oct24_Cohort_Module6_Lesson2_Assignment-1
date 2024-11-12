import mysql.connector
from mysql.connector import Error
from config import password

def connect_to_database():
    db_name = 'fitness_center_db'
    user = 'root'
    db_password = password
    host = '127.0.0.1'

    try:
        connection = mysql.connector.connect(
            database = db_name,
            user = user,
            password = db_password,
            host = host
        )

        if connection.is_connected():
            print("Connected to Fitness Center Database successfully.\n")
            return connection
        
    except Error as e:
        print(f"Error: {e}")
        return None