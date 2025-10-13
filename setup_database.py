import mysql.connector
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('setup_database.py'))))

from config import Config

def create_database():
    conn = None
    try:
        # Connect to MySQL server (without database first)
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
        print("Database created successfully!")
        
        cursor.close()
        conn.close()
        
        # Connect to the new database
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Machines (
                machine_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                status ENUM('Running', 'Stopped', 'Maintenance') DEFAULT 'Running',
                last_maintenance DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Production (
                production_id INT PRIMARY KEY AUTO_INCREMENT,
                line_id INT NOT NULL,
                date DATE NOT NULL,
                output_units INT DEFAULT 0,
                downtime_minutes INT DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Maintenance (
                maintenance_id INT PRIMARY KEY AUTO_INCREMENT,
                machine_id INT,
                schedule_date DATE NOT NULL,
                remarks TEXT,
                FOREIGN KEY (machine_id) REFERENCES Machines(machine_id)
            )
        ''')
        
        # Clear existing data and insert fresh sample data
        cursor.execute('DELETE FROM Maintenance')
        cursor.execute('DELETE FROM Production')
        cursor.execute('DELETE FROM Machines')
        
        # Insert sample data
        cursor.execute('''
            INSERT INTO Machines (machine_id, name, status, last_maintenance) VALUES
            (1, 'Injection Molder A', 'Running', '2024-01-15'),
            (2, 'CNC Machine B', 'Maintenance', '2024-01-10'),
            (3, 'Assembly Robot C', 'Running', '2024-01-20'),
            (4, 'Packaging Line D', 'Stopped', '2024-01-18')
        ''')
        
        cursor.execute('''
            INSERT INTO Production (line_id, date, output_units, downtime_minutes) VALUES
            (1, CURDATE(), 1250, 45),
            (2, CURDATE(), 890, 120),
            (1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 1100, 25),
            (2, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 950, 15),
            (1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 1300, 10),
            (2, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 1000, 5)
        ''')
        
        cursor.execute('''
            INSERT INTO Maintenance (machine_id, schedule_date, remarks) VALUES
            (2, CURDATE(), 'Routine maintenance - bearing replacement'),
            (1, DATE_ADD(CURDATE(), INTERVAL 7 DAY), 'Scheduled calibration'),
            (3, DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Software update')
        ''')
        
        conn.commit()
        print("Tables created and sample data inserted successfully!")
        
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_database()