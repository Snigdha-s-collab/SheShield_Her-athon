import streamlit as st
import requests
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic

st.set_page_config(page_title="SheShield", page_icon="🚨", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>

.stApp {
    background-color: #fff5f8;
}

body, p, span, div {
    color: black !important;
}

h1 {
    color: #ff2e88;
}

h2, h3 {
    color: #c2185b;
}

[data-testid="stSidebar"] {
    background-color: #ffe4ec;
}

[data-testid="stSidebar"] label {
    color: black !important;
    font-weight: bold;
}

.stButton>button {
    background: linear-gradient(90deg,#ff4da6,#ff2e88);
    color: white;
    border-radius: 12px;
    border: none;
    height: 45px;
    font-size: 16px;
}

.stButton>button:hover {
    background: linear-gradient(90deg,#ff2e88,#ff0066);
}

input, textarea {
    background-color: #ffb6d9 !important;
    color: black !important;
    border-radius: 10px;
}

div[data-baseweb="select"] {
    background-color: #ffb6d9 !important;
    border-radius: 10px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffeaf3;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Report Incident", "Safety Map", "AI Legal Chatbot", "Nearby Police Stations"]
)





# ---------- HOME ----------
if menu == "Home":

    st.title("🚨 SheShield")
    st.write("A platform for reporting incidents and accessing safety information.")

    col1, col2 = st.columns(2)

    with col1:
      st.markdown("""
      <div class="card">
      <h3>📢 Report Incident</h3>
      <p>Submit harassment reports to help identify unsafe areas and protect the community.</p>
      </div>
      """, unsafe_allow_html=True)

    with col2:
      st.markdown("""
      <div class="card">
      <h3>🗺 Safety Map</h3>
      <p>View reported unsafe areas on an interactive safety map.</p>
      </div>
      """, unsafe_allow_html=True)

      st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
      st.markdown("""
      <div class="card">
      <h3>⚖ AI Legal Chatbot</h3>
      <p>Ask legal questions and get instant guidance about women's safety laws.</p>
      </div>
      """, unsafe_allow_html=True)

    with col4:
      st.markdown("""
      <div class="card">
      <h3>👮 Nearby Police Stations</h3>
      <p>Find nearby police stations quickly for emergency assistance.</p>
      </div>
      """, unsafe_allow_html=True)

# ---------- REPORT INCIDENT ----------
elif menu == "Report Incident":

    st.header("📢 Report an Incident")

    incident_type = st.selectbox(
        "Incident Type",
        ["stalking", "harassment", "domestic_violence", "eve_teasing", "cybercrime", "other"]
    )

    description = st.text_area("Describe the incident")

    severity = st.selectbox(
        "Severity",
        ["low", "medium", "high"]
    )

    st.markdown("### 📍 Provide Location")

    location_method = st.radio(
        "Choose how to provide location",
        ["Use Live Location", "Enter Location Manually"]
    )

    lat = None
    lon = None
    area_name = ""

    # Live GPS location
    if location_method == "Use Live Location":

        location = streamlit_geolocation()

        if location:

            lat = location["latitude"]
            lon = location["longitude"]
            area_name = "Live Location"

            st.success("Live location detected")

    # Manual location backup
    elif location_method == "Enter Location Manually":

        location_input = st.text_input("Enter location")

        if location_input:

            geolocator = Nominatim(user_agent="sheshield")
            location_data = geolocator.geocode(location_input)

            if location_data:

                lat = location_data.latitude
                lon = location_data.longitude
                area_name = location_input

            else:
                st.error("Location not found")

    if st.button("Submit Report"):

        if lat is None or lon is None or description == "":
            st.warning("Please provide description and location")

        else:

            data = {
                "incident_type": incident_type,
                "description": description,
                "latitude": lat,
                "longitude": lon,
                "area_name": area_name,
                "severity": severity
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/api/reports",
                    json=data
                )

                if response.status_code == 201:
                    st.success("Report submitted successfully")
                else:
                    st.error("Failed to submit report")

            except:
                st.error("Backend server not running")


# ---------- SAFETY MAP ----------
elif menu == "Safety Map":

    st.header("🗺 Safety Map")

    try:
        response = requests.get("http://127.0.0.1:5000/api/reports/map")
        data = response.json()

        m = folium.Map(location=[22.5937, 78.9629], zoom_start=5)

        for point in data["points"]:

            severity = point["severity"]

            if severity == "high":
                color = "red"
            elif severity == "medium":
                color = "orange"
            else:
                color = "green"

            folium.Marker(
                location=[point["latitude"], point["longitude"]],
                popup=f"{point['area_name']} - {point['incident_type']} ({severity})",
                icon=folium.Icon(color=color)
            ).add_to(m)

        st_folium(m, width=900, height=500)

    except Exception as e:
        st.error(f"Unable to load map: {e}")


# ---------- AI LEGAL CHATBOT ----------
elif menu == "AI Legal Chatbot":

    st.header("⚖ AI Legal Chatbot")

    st.warning("""
⚠️ **Disclaimer**

This AI Legal Chatbot provides general legal information related to women's safety laws in India.  
The responses are generated using an AI model and may not always be fully accurate or up-to-date.

This tool **does not provide official legal advice**.  
For verified information, please consult a legal professional or relevant authorities.
""")

    agree = st.checkbox(
        "I understand that this chatbot provides general information and not legal advice."
    )

    if agree:

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        question = st.chat_input("Ask a legal question about women's safety laws")

        if question:

            # store user question
            st.session_state.chat_history.append(("user", question))

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chatbot",
                    json={"question": question}
                )

                data = response.json()
                answer = data.get(
                    "response",
                    "Sorry, I could not generate a response at the moment."
                )

                st.session_state.chat_history.append(("bot", answer))

            except:
                st.error("Backend server not running")

        # display chat history
        for role, message in st.session_state.chat_history:

            if role == "user":
                with st.chat_message("user"):
                    st.write(message)

            else:
                with st.chat_message("assistant"):

                    st.write(message)

                    st.markdown("### 🚨 Emergency Helplines")

                    st.info("""
📞 **Police:** 100  
📞 **Women Helpline:** 1091  
📞 **Domestic Violence:** 181  
📞 **Cyber Crime:** 1930  
📞 **Emergency:** 112  
📞 **National Commission for Women:** 7827170170
""")

                    # Smart advice detection
                    last_question = st.session_state.chat_history[-1][1].lower()

                    if "stalk" in last_question:

                        st.markdown("""
💡 **If you are facing stalking:**
• Avoid responding to the person  
• Save messages or evidence  
• Inform trusted friends or family  
• File a complaint under **IPC Section 354D (Stalking)**  
""")

                    elif "harass" in last_question:

                        st.markdown("""
💡 **If you are facing harassment:**
• Move to a safe place immediately  
• Record details of the incident  
• Seek help from nearby people  
• Report under **IPC Section 354A**
""")

                    elif "cyber" in last_question or "online" in last_question:

                        st.markdown("""
💡 **If you are facing cybercrime:**
• Take screenshots of messages or posts  
• Block the offender  
• Report on the **National Cyber Crime Portal**  
• Call the **Cyber Crime Helpline: 1930**
""")

                    else:

                        st.markdown("""
💡 **General Safety Advice:**
• Stay calm and move to a safe area  
• Inform someone you trust  
• Collect evidence if possible  
• Report the issue to the nearest police station  
""")
        
# ---------- NEARBY POLICE STATIONS ----------
elif menu == "Nearby Police Stations":

    st.header("👮 Find Nearby Police Stations")

    st.markdown("📍 Detecting your live location...")

    location_data = streamlit_geolocation()

    lat = None
    lon = None

    # ---------- LIVE LOCATION ----------
    if location_data and location_data.get("latitude"):

        lat = location_data["latitude"]
        lon = location_data["longitude"]

        st.success("Live location detected")

    # ---------- MANUAL LOCATION ----------
    st.markdown("### Or enter location manually")

    manual_location = st.text_input("Enter your city or area")

    if manual_location:

        geolocator = Nominatim(user_agent="sheshield")

        location = geolocator.geocode(manual_location)

        if location:
            lat = location.latitude
            lon = location.longitude
            st.success(f"Location found: {manual_location}")
        else:
            st.error("Location not found")

    # ---------- SEARCH POLICE STATIONS ----------
    if lat and lon:

        m = folium.Map(location=[lat, lon], zoom_start=14)

        # User marker
        folium.Marker(
            [lat, lon],
            popup="Your Location",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        node["amenity"="police"](around:10000,{lat},{lon});
        out;
        """

        try:

            response = requests.get(
                overpass_url,
                params={'data': query},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
            else:
                st.error("Unable to fetch police station data")
                data = {}

        except:
            st.error("Map server busy. Please try again.")
            data = {}

        stations = []

        if "elements" in data:

            from geopy.distance import geodesic

            for element in data["elements"]:

                if "lat" in element:

                    plat = element["lat"]
                    plon = element["lon"]

                    name = element.get("tags", {}).get(
                        "name", "Police Station"
                    )

                    distance = geodesic((lat, lon), (plat, plon)).km

                    stations.append({
                        "name": name,
                        "lat": plat,
                        "lon": plon,
                        "distance": distance
                    })

        # ---------- SORT BY DISTANCE ----------
        stations = sorted(stations, key=lambda x: x["distance"])

        # ---------- ADD MAP MARKERS ----------
        for station in stations:

            folium.Marker(
                [station["lat"], station["lon"]],
                popup=f"{station['name']} ({station['distance']:.2f} km)",
                icon=folium.Icon(color="red")
            ).add_to(m)

        # ---------- SHOW MAP ----------
        st_folium(
            m,
            width=900,
            height=500,
            key="police_map",
            returned_objects=[]
        )

        # ---------- SHOW LIST ----------
        if stations:

            st.subheader("📍 Police Stations (Nearest First)")

            for i, station in enumerate(stations[:10], start=1):

                google_maps_link = f"https://www.google.com/maps?q={station['lat']},{station['lon']}"

                st.markdown(
                    f"""
**{i}. {station['name']}**  
📏 Distance: {station['distance']:.2f} km  

🔗 [Open in Google Maps]({google_maps_link})
"""
                )

        else:
            st.warning("No police stations found nearby")
