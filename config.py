import mysql.connector
import os

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'hello'  # Change to your MySQL password
    MYSQL_DATABASE = 'manufacturing_db'
    MYSQL_PORT = 3306

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
    


