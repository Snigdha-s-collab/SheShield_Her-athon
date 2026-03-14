# ============================================
# SheShield Backend - main.py (Updated for Ollama AI)
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)

# ---------- DATABASE SETUP ----------
def create_table():
    connection = sqlite3.connect('reports.db')
    cursor = connection.cursor()

    cursor.execute("""
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
    """)

    connection.commit()
    connection.close()

create_table()

# ---------- API 1: HOME ----------
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to SheShield Backend",
        "status": "Server running"
    })

# ---------- API 2: SUBMIT REPORT ----------
@app.route("/api/reports", methods=["POST"])
def submit_report():

    data = request.get_json()

    required_fields = [
        "incident_type",
        "description",
        "latitude",
        "longitude",
        "area_name",
        "severity"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    connection = sqlite3.connect("reports.db")
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    incident_date = data.get("incident_date", now)

    cursor.execute("""
        INSERT INTO reports
        (incident_type, description, latitude, longitude,
         area_name, severity, incident_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["incident_type"],
        data["description"],
        data["latitude"],
        data["longitude"],
        data["area_name"],
        data["severity"],
        incident_date,
        now
    ))

    connection.commit()
    report_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Report submitted successfully",
        "report_id": report_id
    }), 201

# ---------- API 3: GET REPORTS ----------
@app.route("/api/reports", methods=["GET"])
def get_reports():

    connection = sqlite3.connect("reports.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    rows = cursor.fetchall()
    connection.close()

    reports = []

    for row in rows:
        reports.append({
            "id": row[0],
            "incident_type": row[1],
            "description": row[2],
            "latitude": row[3],
            "longitude": row[4],
            "area_name": row[5],
            "severity": row[6],
            "incident_date": row[7],
            "created_at": row[8]
        })

    return jsonify({
        "total": len(reports),
        "reports": reports
    })

# ---------- API 4: MAP DATA ----------
@app.route("/api/reports/map", methods=["GET"])
def get_map_data():

    connection = sqlite3.connect("reports.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT latitude, longitude, area_name, severity, incident_type
        FROM reports
    """)

    rows = cursor.fetchall()
    connection.close()

    points = []

    for row in rows:
        points.append({
            "latitude": row[0],
            "longitude": row[1],
            "area_name": row[2],
            "severity": row[3],
            "incident_type": row[4]
        })

    return jsonify({
        "total": len(points),
        "points": points
    })

# ---------- API 5: STATS ----------
@app.route("/api/reports/stats", methods=["GET"])
def get_stats():

    connection = sqlite3.connect("reports.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity='high'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity='medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE severity='low'")
    low = cursor.fetchone()[0]

    connection.close()

    return jsonify({
        "total_reports": total,
        "by_severity": {
            "high": high,
            "medium": medium,
            "low": low
        }
    })

# ---------- API 6: AI LEGAL CHATBOT (Ollama Llama 3) ----------
@app.route("/chatbot", methods=["POST"])
def chatbot():

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Send question to Ollama AI (Llama 3)
        response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": f"""
You are an AI assistant helping women in India understand their legal rights and safety options.

When answering:
1. Explain the relevant law briefly (IPC section if applicable)
2. Provide clear steps the victim can take
3. Suggest safety actions
4. Include important helpline numbers

Important helplines in India:
• Police: 100
• Women Helpline: 1091
• Emergency: 112
• Domestic Violence Helpline: 181
• Cyber Crime Helpline: 1930

Keep the explanation simple and supportive.

Question: {question}
""",
        "stream": False,
        "options": {
            "num_predict": 150
        }
    }
)

        answer = response.json()["response"]

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({
            "response": f"AI service not running. Please start Ollama. Error: {str(e)}"
        })

# ---------- START SERVER ----------
if __name__ == "__main__":

    print("===================================")
    print("SheShield Backend is RUNNING")
    print("Open: http://localhost:5000")
    print("===================================")

    app.run(debug=True, port=5000)
