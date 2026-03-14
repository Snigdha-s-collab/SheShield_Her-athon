import streamlit as st
import requests
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

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
    ["Home", "Report Incident", "Safety Map", "AI Legal Chatbot" ,"Nearby Police Stations"]
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

    location = st.text_input("Location")
    description = st.text_area("Describe the incident")

    severity = st.selectbox(
        "Severity",
        ["low", "medium", "high"]
    )

    if st.button("Submit Report"):

        if location == "" or description == "":
            st.warning("Please fill all fields")
        else:

            geolocator = Nominatim(user_agent="sheshield")
            location_data = geolocator.geocode(location)

            if location_data is None:
                st.error("Location not found.")
            else:

                latitude = location_data.latitude
                longitude = location_data.longitude

                data = {
                    "incident_type": incident_type,
                    "description": description,
                    "latitude": latitude,
                    "longitude": longitude,
                    "area_name": location,
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

    agree = st.checkbox("I understand that this chatbot provides general information and not legal advice.")

    if agree:

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        question = st.chat_input("Ask a legal question about women's safety laws")

        if question:

            # show user message
            st.session_state.chat_history.append(("user", question))

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chatbot",
                    json={"question": question}
                )

                data = response.json()

                answer = data.get("response", "Sorry, I could not generate a response.")

                st.session_state.chat_history.append(("bot", answer))

            except:
                st.error("Backend server not running")

        # display chat messages
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
               """)

        st.markdown("""
💡 **What you should do in most situations:**
• Stay in a safe place and avoid confrontation  
• Save evidence (messages, screenshots, photos)  
• Inform a trusted friend or family member  
• Report the incident to the nearest police station or cybercrime portal  
• Use the helpline numbers above if you feel unsafe
""")
        
# ---------- NEARBY POLICE STATIONS ----------
elif menu == "Nearby Police Stations":

    st.header("👮 Find Nearby Police Stations")

    if "map_data" not in st.session_state:
        st.session_state.map_data = None
        st.session_state.stations = []

    location = st.text_input("Enter your city or area")

    if st.button("Search Police Stations"):

        geolocator = Nominatim(user_agent="sheshield")
        location_data = geolocator.geocode(location)

        if location_data:

            lat = location_data.latitude
            lon = location_data.longitude

            st.success(f"Location found: {location}")

            m = folium.Map(location=[lat, lon], zoom_start=13)

            folium.Marker(
                [lat, lon],
                popup="Your Location",
                icon=folium.Icon(color="blue")
            ).add_to(m)

            overpass_url = "https://overpass-api.de/api/interpreter"

            query = f"""
            [out:json];
            node["amenity"="police"](around:5000,{lat},{lon});
            out;
            """

            response = requests.get(overpass_url, params={'data': query})
            data = response.json()

            stations = []

            if "elements" in data:

                for element in data["elements"]:

                    plat = element["lat"]
                    plon = element["lon"]

                    name = element.get("tags", {}).get("name", "Police Station")

                    stations.append(name)

                    folium.Marker(
                        [plat, plon],
                        popup=name,
                        icon=folium.Icon(color="red")
                    ).add_to(m)

            # SAVE MAP
            st.session_state.map_data = m
            st.session_state.stations = stations

        else:
            st.error("Location not found")

    # SHOW MAP AFTER BUTTON PRESS
    if st.session_state.map_data:
        map_container = st.container()
        with map_container:
         st_folium(
         st.session_state.map_data,
         width=900,
         height=500,
         key="police_map",
         returned_objects=[]
    )

    # SHOW LIST
    if st.session_state.stations:

        st.subheader("📍 Nearby Police Stations")

        for i, station in enumerate(st.session_state.stations, start=1):
            st.write(f"{i}. {station}")
