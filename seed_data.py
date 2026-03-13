# ============================================
# SheShield - seed_data.py
# This file fills your database with SAMPLE reports.
# Run this ONCE to add fake data for testing/demo.
# ============================================

import sqlite3
from datetime import datetime

# Connect to the same database that app.py uses
connection = sqlite3.connect('reports.db')
cursor = connection.cursor()

# ---------- Sample Reports ----------
# These are FAKE reports with real Indian city locations
# so your map will show pins on actual places.

sample_reports = [
    {
        'incident_type': 'stalking',
        'description': 'A man followed me from the bus stop to my home for 3 days continuously.',
        'latitude': 28.6139,
        'longitude': 77.2090,
        'area_name': 'Connaught Place, Delhi',
        'severity': 'high',
        'incident_date': '2026-03-10 18:30:00'
    },
    {
        'incident_type': 'harassment',
        'description': 'Group of men passed inappropriate comments near college gate.',
        'latitude': 19.0760,
        'longitude': 72.8777,
        'area_name': 'Andheri, Mumbai',
        'severity': 'medium',
        'incident_date': '2026-03-09 08:15:00'
    },
    {
        'incident_type': 'eve_teasing',
        'description': 'Continuous catcalling near the market area during evening hours.',
        'latitude': 12.9716,
        'longitude': 77.5946,
        'area_name': 'MG Road, Bangalore',
        'severity': 'medium',
        'incident_date': '2026-03-11 19:00:00'
    },
    {
        'incident_type': 'domestic_violence',
        'description': 'Neighbour heard screaming and sounds of beating from next door.',
        'latitude': 22.5726,
        'longitude': 88.3639,
        'area_name': 'Salt Lake, Kolkata',
        'severity': 'high',
        'incident_date': '2026-03-08 23:00:00'
    },
    {
        'incident_type': 'cybercrime',
        'description': 'Received threatening messages and morphed photos on social media.',
        'latitude': 17.3850,
        'longitude': 78.4867,
        'area_name': 'Hitech City, Hyderabad',
        'severity': 'high',
        'incident_date': '2026-03-12 14:00:00'
    },
    {
        'incident_type': 'stalking',
        'description': 'An auto driver kept circling around while I was walking alone.',
        'latitude': 26.9124,
        'longitude': 75.7873,
        'area_name': 'MI Road, Jaipur',
        'severity': 'medium',
        'incident_date': '2026-03-07 20:45:00'
    },
    {
        'incident_type': 'harassment',
        'description': 'Inappropriate touching in crowded local bus during rush hour.',
        'latitude': 13.0827,
        'longitude': 80.2707,
        'area_name': 'T Nagar, Chennai',
        'severity': 'high',
        'incident_date': '2026-03-06 09:00:00'
    },
    {
        'incident_type': 'eve_teasing',
        'description': 'Two men on a bike slowed down and made vulgar gestures.',
        'latitude': 18.5204,
        'longitude': 73.8567,
        'area_name': 'FC Road, Pune',
        'severity': 'low',
        'incident_date': '2026-03-11 17:30:00'
    },
    {
        'incident_type': 'other',
        'description': 'Poorly lit street with no CCTV near women hostel. Feels unsafe at night.',
        'latitude': 23.0225,
        'longitude': 72.5714,
        'area_name': 'Navrangpura, Ahmedabad',
        'severity': 'low',
        'incident_date': '2026-03-10 21:00:00'
    },
    {
        'incident_type': 'harassment',
        'description': 'Landlord made inappropriate advances when I went to pay rent alone.',
        'latitude': 28.4595,
        'longitude': 77.0266,
        'area_name': 'Sector 29, Gurgaon',
        'severity': 'high',
        'incident_date': '2026-03-05 11:00:00'
    }
]

# ---------- Insert all reports into database ----------

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for report in sample_reports:
    cursor.execute('''
        INSERT INTO reports (incident_type, description, latitude, longitude,
                            area_name, severity, incident_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        report['incident_type'],
        report['description'],
        report['latitude'],
        report['longitude'],
        report['area_name'],
        report['severity'],
        report['incident_date'],
        now
    ))

# Save everything
connection.commit()
connection.close()

print('============================================')
print('  10 sample reports added to database!')
print('  You can now run: python app.py')
print('============================================')
