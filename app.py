import streamlit as st
import requests

st.set_page_config(page_title="SafeCity", page_icon="🚨", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #fff5f8;
}

/* Make all text black */
body, p, span, div {
    color: black !important;
}

/* Titles */
h1 {
    color: #ff2e88;
}

h2, h3 {
    color: #c2185b;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffe4ec;
}

/* Sidebar navigation label */
[data-testid="stSidebar"] label {
    color: black !important;
    font-weight: bold;
}

/* Buttons */
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

/* Input boxes */
input, textarea {
    background-color: #ffb6d9 !important;
    color: black !important;
    border-radius: 10px;
}

/* Select boxes */
div[data-baseweb="select"] {
    background-color: #ffb6d9 !important;
    border-radius: 10px;
}

/* Placeholder text */
::placeholder {
    color: #5a5a5a !important;
}

/* Card style */
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffeaf3;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.divider()

# ---------- SIDEBAR ----------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Report Incident", "Legal Chatbot"]
)

# ---------- HOME ----------
if menu == "Home":

    st.header("🏠 Welcome to SafeCity")

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
        <h3>🤖 Legal Assistance</h3>
        <p>Ask legal questions and get guidance on harassment laws and safety actions.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- REPORT INCIDENT ----------
elif menu == "Report Incident":

    st.header("📢 Report an Incident")

    incident_type = st.selectbox(
        "Incident Type",
        ["Harassment", "Stalking", "Verbal Abuse", "Other"]
    )

    location = st.text_input("Location")

    description = st.text_area("Describe the incident")

    if st.button("Submit Report"):

        data = {
            "incident_type": incident_type,
            "location": location,
            "description": description
        }

        try:
            requests.post("http://127.0.0.1:5000/report", json=data)
            st.success("✅ Report submitted successfully!")
        except:
            st.error("⚠ Backend not connected")

# ---------- CHATBOT ----------
elif menu == "Legal Chatbot":

    st.header("🤖 Legal Assistance Chatbot")

    question = st.text_input("Ask your legal question")

    if st.button("Ask"):

        try:
            response = requests.post(
                "http://127.0.0.1:5000/chatbot",
                json={"question": question}
            )

            answer = response.json()["response"]

            st.write("💬 Chatbot Response")
            st.info(answer)

        except:
            st.error("⚠ Chatbot backend not connected")
