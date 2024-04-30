from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import random
import threading
import time

app = Flask(__name__)

DB_SENSOR_NAME = "sensor_data"
DB_RANDOM_NAME = "random_data"

DB_SENSOR = DB_SENSOR_NAME + ".sqlite"
DB_RANDOM = DB_RANDOM_NAME + ".sqlite"

def create_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    conn.commit()

def init_databases():
    try:
        conn_sensor = sqlite3.connect(DB_SENSOR)
        create_table(conn_sensor, DB_SENSOR_NAME)
        conn_sensor.close()

        conn_random = sqlite3.connect(DB_RANDOM)
        create_table(conn_random, DB_RANDOM_NAME)
        conn_random.close()

        print("Databases initialized successfully.")
    except sqlite3.Error as e:
        print("Error occurred during database initialization:", e)

# Render the main page template
@app.route("/")
def index():
    return render_template("index.html")

# Insert data into the database
def insert_data(temperature, humidity, timestamp=None, db_name=DB_SENSOR_NAME):
    if temperature == 0 and humidity == 0:
        print("Temperature and humidity are both zero, skipping insertion into the database.")
        return

    db = DB_SENSOR if db_name == "sensor_data" else DB_RANDOM
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        if timestamp is None:
            timestamp = datetime.now().replace(microsecond=0)
        
        cursor.execute(
            f"""INSERT INTO {db_name} (temperature, humidity, timestamp) VALUES (?, ?, ?)""",
            (temperature, humidity, timestamp),
        )
        
        conn.commit()
        conn.close()
        print(f"({db_name})Data inserted successfully.") 
    except sqlite3.Error as e:
        print(f"{db_name})Error inserting data: {e}")

# Generate and insert random data every 2 seconds
def generate_random_data():
    while True:
        temp = random.randint(20, 40)
        humid = random.randint(20, 40)
        insert_data(temp, humid, db_name=DB_RANDOM_NAME)
        # Wait for 2 seconds
        time.sleep(2)


# Receive sensor data and insert it into the database
@app.post("/post_data")
def receive_data():
    try:
        content = request.get_json()
        temperature = content["temperature"]
        humidity = content["humidity"]
        
        insert_data(temperature, humidity)
        
        print(f"Received data: temperature={temperature}, humidity={humidity}")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error receiving data: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# Get recent sensor data
@app.route("/get_data/Mode=<db_name>/Count=<count>")
def get_data(db_name, count):
    db = DB_SENSOR if db_name == "sensor_data" else DB_RANDOM
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'SELECT temperature, humidity, timestamp FROM {db_name} ORDER BY id DESC LIMIT {count}')
        data = c.fetchall()
        conn.close()
        # Format the data into JSON format
        formatted_data = [{"temperature": row[0], "humidity": row[1], "timestamp": row[2]} for row in data]
        return jsonify(formatted_data)
    except sqlite3.Error as e:
        print(f"Error retrieving data: {e}")
        return jsonify({"error": str(e)})

@app.route("/get_data_by_date/Mode=<db_name>/Date=<date>")
def get_data_by_date(db_name, date):
    db = DB_SENSOR if db_name == "sensor_data" else DB_RANDOM
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'SELECT temperature, humidity, timestamp FROM {db_name} WHERE DATE(timestamp) = ? ORDER BY timestamp', (date,))
        data = c.fetchall()
        conn.close()

        if not data:
            return jsonify({"error": "No data available for the selected date."})

        # Calculate average temperature and humidity
        temperature_sum = sum(row[0] for row in data)
        humidity_sum = sum(row[1] for row in data)
        average_temperature = temperature_sum / len(data)
        average_humidity = humidity_sum / len(data)

        # Format the data into JSON format
        formatted_data = [{"temperature": row[0], "humidity": row[1], "timestamp": row[2]} for row in data]
        return jsonify({"data": formatted_data, "average_temperature": average_temperature, "average_humidity": average_humidity})
    except sqlite3.Error as e:
        print(f"Error retrieving data by date: {e}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Initialize SQLite databases
    init_databases()
    # Start generating random sensor data
    random_data_thread = threading.Thread(target=generate_random_data)
    random_data_thread.daemon = True
    random_data_thread.start()
    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)




