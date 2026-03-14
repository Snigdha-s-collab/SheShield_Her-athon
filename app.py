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
    ["Home", "Report Incident", "Safety Map", "AI Legal Chatbot"]
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

    question = st.text_area("Ask a legal question")

    if st.button("Ask AI"):

        try:
            response = requests.post(
                "http://127.0.0.1:5000/chatbot",
                json={"question": question}
            )

            data = response.json()

            if "response" in data:
                st.markdown(data["response"])
            else:
                st.error("Error getting response")

        except:
            st.error("Backend server not running")
