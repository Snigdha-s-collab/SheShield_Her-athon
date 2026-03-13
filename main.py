# ============================================
# SheShield Backend - main.py
# This is the main file of your backend.
# It creates a server that can receive and send data.
# ============================================

# ---------- STEP 1: Import tools ----------
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

# ---------- STEP 2: Create the app ----------
app = Flask(__name__)
CORS(app)

# ---------- STEP 3: Database Setup ----------
def create_table():
    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()
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
    connection.commit()
    connection.close()

create_table()


# ---------- API 1: Home Page ----------
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to SheShield Backend!',
        'status': 'Server is running'
    })


# ---------- API 2: Submit a Report ----------
@app.route('/api/reports', methods=['POST'])
def submit_report():
    data = request.get_json()

    required_fields = ['incident_type', 'description', 'latitude',
                       'longitude', 'area_name', 'severity']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    if data['severity'] not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Severity must be: low, medium, or high'}), 400

    valid_types = ['stalking', 'harassment', 'domestic_violence',
                   'eve_teasing', 'cybercrime', 'other']

    if data['incident_type'] not in valid_types:
        return jsonify({'error': f'Invalid type. Must be one of: {valid_types}'}), 400

    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    incident_date = data.get('incident_date', now)

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
    report_id = cursor.lastrowid
    connection.close()

    return jsonify({
        'message': 'Report submitted successfully!',
        'report_id': report_id
    }), 201


# ---------- API 3: Get All Reports ----------
@app.route('/api/reports', methods=['GET'])
def get_reports():
    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    query = 'SELECT * FROM reports WHERE 1=1'
    params = []

    severity = request.args.get('severity')
    if severity:
        query += ' AND severity = ?'
        params.append(severity)

    incident_type = request.args.get('incident_type')
    if incident_type:
        query += ' AND incident_type = ?'
        params.append(incident_type)

    query += ' ORDER BY created_at DESC'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

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
@app.route('/api/reports/stats', methods=['GET'])
def get_stats():
    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM reports')
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'high'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity = 'low'")
    low = cursor.fetchone()[0]

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
if __name__ == '__main__':
    print('============================================')
    print('  SheShield Backend is RUNNING!')
    print('  Open: http://localhost:5000')
    print('============================================')
    app.run(debug=True, port=5000)

