import os
import sys
from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
import json

# Add current directory to Python path to fix config import
sys.path.append(os.path.dirname(os.path.abspath('app.py')))

try:
    from config import get_db_connection
except ImportError:
    print("Error: Could not import config. Make sure config.py exists in the same directory.")
    sys.exit(1)

app = Flask(__name__)

def generate_production_chart():
    """Generate production trend chart"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT date, SUM(output_units) as total_output, SUM(downtime_minutes) as total_downtime
            FROM Production 
            GROUP BY date 
            ORDER BY date DESC 
            LIMIT 7
        ''')
        data = cursor.fetchall()
        
        if not data:
            return None
            
        dates = [row['date'].strftime('%m-%d') for row in data[::-1]]
        production = [row['total_output'] for row in data[::-1]]
        downtime = [row['total_downtime'] for row in data[::-1]]
        
        plt.figure(figsize=(10, 6))
        
        # Production trend
        plt.subplot(2, 1, 1)
        plt.plot(dates, production, marker='o', linewidth=2, markersize=6, color='blue')
        plt.title('Production Trend (Last 7 Days)')
        plt.ylabel('Output Units')
        plt.grid(True, alpha=0.3)
        
        # Downtime trend
        plt.subplot(2, 1, 2)
        plt.bar(dates, downtime, color='red', alpha=0.7)
        plt.title('Downtime Trend (Last 7 Days)')
        plt.ylabel('Downtime Minutes')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{plot_url}"
        
    except Exception as e:
        print(f"Chart generation error: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def check_downtime_alerts():
    """Check for downtime alerts > 30 minutes"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return []
            
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT line_id, date, downtime_minutes 
            FROM Production 
            WHERE downtime_minutes > 30 AND date = CURDATE()
        ''')
        alerts = cursor.fetchall()
        
        alert_messages = []
        for alert in alerts:
            alert_messages.append(f"🚨 ALERT: Line {alert['line_id']} has {alert['downtime_minutes']} minutes downtime today!")
        
        return alert_messages
        
    except Exception as e:
        print(f"Alert check error: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    conn = None
    try:
        user_message = request.json.get('message', '').lower()
        response = {"response": "", "chart": None, "alerts": []}
        
        # Check for alerts first
        alerts = check_downtime_alerts()
        if alerts:
            response["alerts"] = alerts
        
        conn = get_db_connection()
        if conn is None:
            response["response"] = "❌ Database connection error. Please check if MySQL is running and database is setup."
            return jsonify(response)
            
        cursor = conn.cursor(dictionary=True)
        
        # Keyword-based response logic
        if 'today' in user_message and 'production' in user_message:
            cursor.execute('''
                SELECT line_id, output_units, downtime_minutes 
                FROM Production 
                WHERE date = CURDATE()
            ''')
            results = cursor.fetchall()
            
            if results:
                response_text = "📊 Today's Production:\n"
                for row in results:
                    response_text += f"Line {row['line_id']}: {row['output_units']} units, Downtime: {row['downtime_minutes']} min\n"
                response["response"] = response_text
                response["chart"] = generate_production_chart()
            else:
                response["response"] = "No production data found for today."
                
        elif 'maintenance' in user_message or 'under maintenance' in user_message:
            cursor.execute('''
                SELECT m.name, m.status, mt.schedule_date, mt.remarks 
                FROM Machines m 
                LEFT JOIN Maintenance mt ON m.machine_id = mt.machine_id 
                WHERE m.status = 'Maintenance' OR mt.schedule_date <= CURDATE()
            ''')
            results = cursor.fetchall()
            
            if results:
                response_text = "🔧 Machines Under Maintenance:\n"
                for row in results:
                    response_text += f"• {row['name']} - Status: {row['status']}\n"
                    if row['schedule_date']:
                        response_text += f"  Scheduled: {row['schedule_date']} - {row['remarks']}\n"
                response["response"] = response_text
            else:
                response["response"] = "No machines currently under maintenance."
                
        elif 'downtime' in user_message and 'line' in user_message:
            # Extract line number
            line_num = None
            words = user_message.split()
            for i, word in enumerate(words):
                if word == 'line' and i+1 < len(words):
                    try:
                        line_num = int(words[i+1])
                        break
                    except ValueError:
                        pass
            
            if line_num:
                cursor.execute('''
                    SELECT date, downtime_minutes 
                    FROM Production 
                    WHERE line_id = %s 
                    ORDER BY date DESC 
                    LIMIT 5
                ''', (line_num,))
                results = cursor.fetchall()
                
                if results:
                    response_text = f"⏱️ Downtime Report for Line {line_num}:\n"
                    for row in results:
                        response_text += f"• {row['date']}: {row['downtime_minutes']} minutes\n"
                    response["response"] = response_text
                else:
                    response["response"] = f"No downtime data found for Line {line_num}."
            else:
                response["response"] = "Please specify which line (e.g., 'Line 1')"
                
        elif 'status' in user_message or 'machine' in user_message:
            cursor.execute('SELECT name, status, last_maintenance FROM Machines')
            results = cursor.fetchall()
            
            if results:
                response_text = "🏭 Machine Status:\n"
                for row in results:
                    status_icon = "🟢" if row['status'] == 'Running' else "🔴" if row['status'] == 'Stopped' else "🟡"
                    response_text += f"{status_icon} {row['name']}: {row['status']} (Last Maintenance: {row['last_maintenance']})\n"
                response["response"] = response_text
            else:
                response["response"] = "No machine data found."
                
        elif 'help' in user_message:
            response["response"] = """🤖 Available Commands:
• "Show today's production" - Get today's production data
• "List machines under maintenance" - View maintenance schedule
• "Show downtime report for Line X" - Get downtime history
• "Machine status" - Check all machine status
• "Help" - Show this help message"""
                
        else:
            response["response"] = "I'm not sure I understand. Try asking about:\n• Production data\n• Maintenance schedules\n• Downtime reports\n• Machine status\n\nType 'help' for all available commands."
        
        return jsonify(response)
        
    except mysql.connector.Error as e:
        return jsonify({"response": f"❌ Database error: {str(e)}", "chart": None, "alerts": []})
    except Exception as e:
        return jsonify({"response": f"❌ Error processing request: {str(e)}", "chart": None, "alerts": []})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    print("🚀 Starting Manufacturing Operations Chatbot...")
    print("📊 Open http://localhost:5000 in your browser")
    print("⚡ Make sure MySQL is running and database is setup")
    app.run(debug=True, host='0.0.0.0', port=5000)