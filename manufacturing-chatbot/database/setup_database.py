import mysql.connector
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.config import Config
from datetime import datetime, timedelta

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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Machines (
                machine_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                status ENUM('Running', 'Stopped', 'Maintenance') DEFAULT 'Running',
                last_maintenance DATE,
                location VARCHAR(50),
                manufacturer VARCHAR(50),
                installed_date DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Production (
                production_id INT PRIMARY KEY AUTO_INCREMENT,
                line_id INT NOT NULL,
                date DATE NOT NULL,
                shift ENUM('Morning', 'Evening', 'Night') DEFAULT 'Morning',
                output_units INT DEFAULT 0,
                target_units INT DEFAULT 0,
                downtime_minutes INT DEFAULT 0,
                quality_defects INT DEFAULT 0,
                operator_name VARCHAR(50)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Maintenance (
                maintenance_id INT PRIMARY KEY AUTO_INCREMENT,
                machine_id INT,
                schedule_date DATE NOT NULL,
                completion_date DATE,
                maintenance_type ENUM('Preventive', 'Corrective', 'Emergency') DEFAULT 'Preventive',
                status ENUM('Scheduled', 'In Progress', 'Completed') DEFAULT 'Scheduled',
                remarks TEXT,
                technician VARCHAR(50),
                duration_hours DECIMAL(4,2),
                cost DECIMAL(10,2),
                FOREIGN KEY (machine_id) REFERENCES Machines(machine_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Downtime (
                downtime_id INT PRIMARY KEY AUTO_INCREMENT,
                machine_id INT,
                line_id INT,
                start_time DATETIME,
                end_time DATETIME,
                duration_minutes INT,
                reason ENUM('Breakdown', 'Maintenance', 'Material Shortage', 'Quality Check', 'Power Outage', 'Other'),
                description TEXT,
                reported_by VARCHAR(50),
                FOREIGN KEY (machine_id) REFERENCES Machines(machine_id)
            )
        ''')
        
        # Clear existing data
        cursor.execute('DELETE FROM Downtime')
        cursor.execute('DELETE FROM Maintenance')
        cursor.execute('DELETE FROM Production')
        cursor.execute('DELETE FROM Machines')
        
        print("✅ Tables created successfully!")
        
        # Get current date for dynamic data
        today = datetime.now().date()
        
        # Insert comprehensive sample data for Machines
        cursor.execute(f'''
            INSERT INTO Machines (machine_id, name, status, last_maintenance, location, manufacturer, installed_date) VALUES
            (1, 'Injection Molding Machine A', 'Running', '{today - timedelta(days=20)}', 'Section A', 'Haitian', '2020-03-15'),
            (2, 'CNC Machining Center B', 'Maintenance', '{today - timedelta(days=25)}', 'Section B', 'Mazak', '2019-08-20'),
            (3, 'Assembly Robot C', 'Running', '{today - timedelta(days=15)}', 'Assembly Line', 'Fanuc', '2021-05-10'),
            (4, 'Packaging Line D', 'Stopped', '{today - timedelta(days=17)}', 'Packaging Area', 'Bosch', '2020-11-30'),
            (5, 'Laser Cutting Machine E', 'Running', '{today - timedelta(days=10)}', 'Section C', 'Trumpf', '2022-02-14'),
            (6, '3D Printer F', 'Running', '{today - timedelta(days=8)}', 'R&D Lab', 'Stratasys', '2023-01-15'),
            (7, 'Quality Scanner G', 'Maintenance', '{today - timedelta(days=5)}', 'Quality Control', 'Keyence', '2021-09-05'),
            (8, 'Conveyor System H', 'Running', '{today - timedelta(days=12)}', 'Assembly Line', 'Siemens', '2020-07-22')
        ''')
        print("✅ Machines data inserted!")
        
        # Generate comprehensive production data for the last 10 days
        production_data = []
        operators = ['John Smith', 'Maria Garcia', 'Robert Johnson', 'Lisa Chen', 'Mike Brown', 'Sarah Wilson']
        
        for days_ago in range(10):  # Last 10 days
            date = today - timedelta(days=days_ago)
            
            # Line 1 - All shifts
            production_data.append((1, date, 'Morning', 1250, 1200, 25, 8, operators[days_ago % 6]))
            production_data.append((1, date, 'Evening', 1180, 1150, 45, 12, operators[(days_ago + 1) % 6]))
            production_data.append((1, date, 'Night', 1100, 1100, 60, 15, operators[(days_ago + 2) % 6]))
            
            # Line 2 - All shifts
            production_data.append((2, date, 'Morning', 980, 1000, 35, 10, operators[(days_ago + 3) % 6]))
            production_data.append((2, date, 'Evening', 920, 950, 75, 18, operators[(days_ago + 4) % 6]))
            production_data.append((2, date, 'Night', 850, 900, 90, 22, operators[(days_ago + 5) % 6]))

        cursor.executemany('''
            INSERT INTO Production (line_id, date, shift, output_units, target_units, downtime_minutes, quality_defects, operator_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', production_data)
        print("✅ Production data inserted!")
        
        # Insert comprehensive maintenance data
        cursor.execute(f'''
            INSERT INTO Maintenance (machine_id, schedule_date, completion_date, maintenance_type, status, remarks, technician, duration_hours, cost) VALUES
            (2, '{today}', '{today}', 'Corrective', 'Completed', 'Bearing replacement and calibration', 'Tech Raj Sharma', 6.5, 12500.00),
            (1, '{today + timedelta(days=7)}', NULL, 'Preventive', 'Scheduled', 'Quarterly maintenance - hydraulic system check', 'Tech Singh', 4.0, 8000.00),
            (3, '{today + timedelta(days=14)}', NULL, 'Preventive', 'Scheduled', 'Software update and sensor calibration', 'Tech Kumar', 3.5, 5500.00),
            (7, '{today}', '{today}', 'Emergency', 'Completed', 'Lens replacement and alignment', 'Tech Sharma', 2.5, 3200.00),
            (4, '{today - timedelta(days=2)}', '{today - timedelta(days=2)}', 'Corrective', 'Completed', 'Motor replacement and belt adjustment', 'Tech Verma', 8.0, 15000.00),
            (5, '{today + timedelta(days=3)}', NULL, 'Preventive', 'Scheduled', 'Laser calibration and mirror cleaning', 'Tech Gupta', 5.0, 9200.00),
            (8, '{today + timedelta(days=10)}', NULL, 'Preventive', 'Scheduled', 'Conveyor belt inspection and roller replacement', 'Tech Joshi', 6.0, 11000.00),
            (6, '{today}', NULL, 'Preventive', 'In Progress', 'Nozzle cleaning and firmware update', 'Tech Malhotra', 3.0, 4500.00),
            (1, '{today - timedelta(days=30)}', '{today - timedelta(days=30)}', 'Preventive', 'Completed', 'Routine inspection and lubrication', 'Tech Patel', 2.0, 3000.00),
            (2, '{today + timedelta(days=21)}', NULL, 'Preventive', 'Scheduled', 'Complete overhaul and upgrades', 'Tech Reddy', 12.0, 25000.00)
        ''')
        print("✅ Maintenance data inserted!")
        
        # Insert comprehensive downtime incidents
        cursor.execute(f'''
            INSERT INTO Downtime (machine_id, line_id, start_time, end_time, duration_minutes, reason, description, reported_by) VALUES
            (2, 2, '{today} 08:30:00', '{today} 15:00:00', 390, 'Breakdown', 'Main bearing failure requiring replacement', 'Supervisor A'),
            (4, 2, '{today - timedelta(days=1)} 10:15:00', '{today - timedelta(days=1)} 18:15:00', 480, 'Breakdown', 'Motor burnt out - emergency replacement', 'Supervisor B'),
            (1, 1, '{today - timedelta(days=2)} 14:00:00', '{today - timedelta(days=2)} 16:30:00', 150, 'Material Shortage', 'Raw material delivery delayed due to supplier issues', 'Operator A'),
            (3, 1, '{today - timedelta(days=3)} 11:45:00', '{today - timedelta(days=3)} 12:30:00', 45, 'Quality Check', 'Routine quality inspection and calibration', 'Quality Inspector'),
            (5, 1, '{today - timedelta(days=4)} 09:00:00', '{today - timedelta(days=4)} 09:45:00', 45, 'Power Outage', 'Scheduled power maintenance by utility company', 'Facility Manager'),
            (7, 2, '{today - timedelta(days=5)} 13:20:00', '{today - timedelta(days=5)} 15:50:00', 150, 'Breakdown', 'Scanner lens cracked during operation', 'Operator C'),
            (8, 1, '{today - timedelta(days=6)} 16:00:00', '{today - timedelta(days=6)} 17:30:00', 90, 'Maintenance', 'Preventive maintenance - belt tension adjustment', 'Tech Team'),
            (6, 2, '{today - timedelta(days=7)} 10:00:00', '{today - timedelta(days=7)} 13:00:00', 180, 'Maintenance', 'Scheduled nozzle replacement and calibration', 'Tech Team'),
            (2, 1, '{today - timedelta(days=8)} 07:30:00', '{today - timedelta(days=8)} 08:15:00', 45, 'Quality Check', 'Product quality validation and testing', 'Quality Control'),
            (4, 2, '{today - timedelta(days=9)} 12:00:00', '{today - timedelta(days=9)} 14:30:00', 150, 'Material Shortage', 'Packaging material stock depletion', 'Logistics Manager')
        ''')
        print("✅ Downtime data inserted!")
        
        conn.commit()
        
        print("\n🎉 DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("📊 ENHANCED SAMPLE DATA OVERVIEW:")
        print("   ┌─────────────────┬─────────────┐")
        print("   │ Data Type       │ Records     │")
        print("   ├─────────────────┼─────────────┤")
        print("   │ Machines        │ 8           │")
        print("   │ Production      │ 60          │")
        print("   │ Maintenance     │ 10          │")
        print("   │ Downtime        │ 10          │")
        print("   └─────────────────┴─────────────┘")
        print(f"📅 Data covers: {today - timedelta(days=9)} to {today + timedelta(days=21)}")
        
        print("\n💡 NEW FEATURES DEMONSTRATED:")
        print("   • Multiple shifts (Morning/Evening/Night)")
        print("   • Quality defect tracking")
        print("   • Operator performance data")
        print("   • Maintenance cost analysis")
        print("   • Detailed downtime reasons")
        print("   • Equipment location tracking")
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("\n✅ Database connection closed.")

if __name__ == "__main__":
    create_database()