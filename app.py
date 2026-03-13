# ============================================
# SheShield Backend - app.py
# This is the main file of your backend.
# It creates a server that can receive and send data.
# ============================================

# ---------- STEP 1: Import tools ----------
# These are like "importing ingredients" before cooking

from flask import Flask, request, jsonify  # Flask = the tool to make our server
from flask_cors import CORS               # CORS = allows frontend to talk to us
import sqlite3                             # sqlite3 = our database (comes with Python, no install needed!)
from datetime import datetime              # datetime = to record when a report is submitted

# ---------- STEP 2: Create the app ----------
# This one line creates your entire server!

app = Flask(__name__)
CORS(app)  # This allows Member 1's frontend to connect to our backend

# ---------- STEP 3: Database Setup ----------
# Think of a database like an Excel spreadsheet.
# This function creates the "spreadsheet" if it doesn't exist yet.

def create_table():
    # "connect" = open the Excel file (reports.db is the file name)
    connection = sqlite3.connect('reports.db')

    # "cursor" = your pen to write on the spreadsheet
    cursor = connection.cursor()

    # This creates a table (like a sheet in Excel) called "reports"
    # Each report will have these columns:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            description TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            area_name TEXT NOT NULL,
            severity TEXT NOT NULL,
            incident_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Save the changes
    connection.commit()

    # Close the file (always close when done!)
    connection.close()

# Run this function immediately when the app starts
create_table()


# ============================================
# STEP 4: CREATE THE APIs (Routes)
# An API is just a URL that does something.
# Like: if someone visits /api/reports, we send them data.
# ============================================


# ---------- API 1: Home Page ----------
# Just to check if your server is running

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to SheShield Backend!',
        'status': 'Server is running'
    })


# ---------- API 2: Submit a Report ----------
# When a user fills the form and clicks "Submit",
# the frontend sends the data HERE, and we save it.

@app.route('/api/reports', methods=['POST'])
def submit_report():

    # Get the data that the frontend sent us
    data = request.get_json()

    # Check: did they send all the required fields?
    required_fields = ['incident_type', 'description', 'latitude',
                       'longitude', 'area_name', 'severity']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Check: is the severity valid?
    if data['severity'] not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Severity must be: low, medium, or high'}), 400

    # Check: is the incident type valid?
    valid_types = ['stalking', 'harassment', 'domestic_violence',
                   'eve_teasing', 'cybercrime', 'other']

    if data['incident_type'] not in valid_types:
        return jsonify({'error': f'Invalid type. Must be one of: {valid_types}'}), 400

    # If everything is good, save it to the database!
    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    # Get the current date and time
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Use incident_date from data, or use current date if not provided
    incident_date = data.get('incident_date', now)

    # Insert the report into the database (like adding a row in Excel)
    cursor.execute('''
        INSERT INTO reports (incident_type, description, latitude, longitude,
                            area_name, severity, incident_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['incident_type'],
        data['description'],
        data['latitude'],
        data['longitude'],
        data['area_name'],
        data['severity'],
        incident_date,
        now
    ))

    connection.commit()

    # Get the ID of the report we just saved
    report_id = cursor.lastrowid

    connection.close()

    # Send back a success message
    return jsonify({
        'message': 'Report submitted successfully!',
        'report_id': report_id
    }), 201


# ---------- API 3: Get All Reports ----------
# Returns all the reports from the database.
# The frontend can use this to show a list of incidents.

@app.route('/api/reports', methods=['GET'])
def get_reports():

    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    # Start building the query
    query = 'SELECT * FROM reports WHERE 1=1'
    params = []

    # --- FILTERS (optional) ---
    # The frontend can add ?severity=high to the URL to filter

    severity = request.args.get('severity')
    if severity:
        query += ' AND severity = ?'
        params.append(severity)

    incident_type = request.args.get('incident_type')
    if incident_type:
        query += ' AND incident_type = ?'
        params.append(incident_type)

    # Always show newest reports first
    query += ' ORDER BY created_at DESC'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

    # Convert database rows into a list of dictionaries
    # (dictionaries are like labelled boxes - easier to read)
    reports = []
    for row in rows:
        reports.append({
            'id': row[0],
            'incident_type': row[1],
            'description': row[2],
            'latitude': row[3],
            'longitude': row[4],
            'area_name': row[5],
            'severity': row[6],
            'incident_date': row[7],
            'created_at': row[8]
        })

    return jsonify({
        'total': len(reports),
        'reports': reports
    })


# ---------- API 4: Map Data ----------
# This is specifically for Member 3 (Map person).
# Returns ONLY the location + severity (no descriptions).
# This makes the map load faster.

@app.route('/api/reports/map', methods=['GET'])
def get_map_data():

    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT latitude, longitude, area_name, severity, incident_type
        FROM reports
    ''')

    rows = cursor.fetchall()
    connection.close()

    map_points = []
    for row in rows:
        map_points.append({
            'latitude': row[0],
            'longitude': row[1],
            'area_name': row[2],
            'severity': row[3],
            'incident_type': row[4]
        })

    return jsonify({
        'total': len(map_points),
        'points': map_points
    })


# ---------- API 5: Stats / Dashboard ----------
# Returns counts and summaries.
# Useful for showing "50 reports filed" on the homepage.

@app.route('/api/reports/stats', methods=['GET'])
def get_stats():

    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    # Total number of reports
    cursor.execute('SELECT COUNT(*) FROM reports')
    total = cursor.fetchone()[0]

    # Count by severity
    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'high'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'low'")
    low = cursor.fetchone()[0]

    # Count by incident type
    cursor.execute('''
        SELECT incident_type, COUNT(*) as count
        FROM reports
        GROUP BY incident_type
        ORDER BY count DESC
    ''')
    type_counts = {}
    for row in cursor.fetchall():
        type_counts[row[0]] = row[1]

    connection.close()

    return jsonify({
        'total_reports': total,
        'by_severity': {
            'high': high,
            'medium': medium,
            'low': low
        },
        'by_type': type_counts
    })


# ---------- STEP 5: Start the Server ----------
# This is the "ON switch" for your backend.

if __name__ == '__main__':
    print('============================================')
    print('  SheShield Backend is RUNNING!')
    print('  Open: http://localhost:5000')
    print('============================================')
    app.run(debug=True, port=5000)
