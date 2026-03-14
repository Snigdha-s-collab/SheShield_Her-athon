# 🚨 SheShield — Women's Safety Platform

> **Community-powered safety intelligence for women in India.**  
> Report incidents. See danger zones. Get legal help. Find police — instantly.

---

## 🔥 Why SheShield?

Every **3 minutes**, a crime is committed against a woman in India. Most go unreported. Existing safety apps just provide helpline numbers — **SheShield goes further.**

We combine **community-reported incident data**, **AI-powered legal guidance**, and **real-time police station discovery** into one platform — all running **locally with zero cloud dependency**, keeping sensitive data private.

---

## ✨ Features

### 📢 Incident Reporting
- Report harassment, stalking, domestic violence, cybercrime & more
- **Live GPS auto-detection** or manual location entry
- Geopy converts place names to GPS coordinates
- All reports stored securely in SQLite

### 🗺️ Safety Heatmap
- Interactive Folium map of India
- Color-coded markers based on severity:
  - 🔴 **Red** = High Severity
  - 🟠 **Orange** = Medium Severity
  - 🟢 **Green** = Low Severity
- Click any marker to see incident details

### ⚖️ AI Legal Chatbot
- Powered by **Phi-3** via **Ollama** (runs 100% locally — no data leaves your machine)
- Explains relevant **IPC sections**, steps to take, and safety measures
- **Smart Advice Detection** — automatically detects topic and shows specific guidance:
  | Topic Detected | Shows |
  |---|---|
  | Stalking | IPC Section 354D + evidence tips |
  | Harassment | IPC Section 354A + safety steps |
  | Cybercrime | Cyber Crime Portal + screenshot advice |
- Displays **emergency helplines** after every response
- Includes **disclaimer** — responsible AI usage with checkbox agreement

### 👮 Nearby Police Stations
- **Live GPS** auto-detection + manual backup
- Searches within **10 km radius** using OpenStreetMap's Overpass API
- Shows **exact distance** using geodesic calculation
- **Google Maps navigation links** — one click to get directions
- Sorted **nearest first** with the closest station highlighted

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Flask (Python) |
| **Frontend** | Streamlit |
| **Database** | SQLite |
| **AI Model** | Ollama — Phi-3 (local) |
| **Maps** | Folium + streamlit-folium |
| **Geocoding** | Geopy (Nominatim) |
| **Live Location** | streamlit-geolocation |
| **Distance** | geopy.distance (geodesic) |
| **Police Data** | Overpass API (OpenStreetMap) |
| **API Security** | Flask-CORS |

---

## 📐 Architecture

```
┌─────────────────────────────────┐
│     User (Browser)              │
│     Streamlit Frontend          │
└──────────┬──────────────────────┘
           │
     ┌─────▼─────┐     ┌──────────────┐
     │  Flask     │────▶│  SQLite DB   │
     │  Backend   │     │  (reports.db)│
     └─────┬──────┘     └──────────────┘
           │
     ┌─────▼──────┐
     │  Ollama     │
     │  Phi-3 AI   │
     │  (local)    │
     └─────────────┘

     Streamlit ──────▶ Overpass API (police stations)
     Streamlit ──────▶ Browser GPS (live location)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com/) installed with Phi-3 model

### 1. Clone the repo
```bash
git clone https://github.com/Snigdha-s-collab/SheShield_Her-athon.git
cd SheShield_Her-athon
```

### 2. Install dependencies
```bash
pip install flask flask-cors streamlit requests geopy folium streamlit-folium streamlit-geolocation
```

### 3. Start Ollama AI
```bash
ollama run phi3
```

### 4. Seed the database (first time only)
```bash
python seed_data.py
```

### 5. Start the backend (Terminal 1)
```bash
python main.py
```

### 6. Start the frontend (Terminal 2)
```bash
streamlit run app.py
```

Open **http://localhost:8501** and you're live! 🎉

---

## 📂 Project Structure

```
SheShield_Her-athon/
├── main.py            # Flask backend — 6 REST APIs + AI chatbot
├── app.py             # Streamlit frontend — 5 pages with maps & chat
├── seed_data.py       # Populates database with 10 sample incidents
├── reports.db         # SQLite database (auto-created)
├── requirements.txt   # Python dependencies
└── README.md          # You are here!
```

---

## 🔒 Security & Privacy

- **SQL injection prevention** — parameterized queries with `?` placeholders
- **CORS protection** — only authorized origins can access the API
- **Input validation** — required field checks before database operations
- **100% local AI** — no data sent to external servers
- **Anonymous by design** — no personal information collected
- **AI disclaimer** — responsible usage with mandatory acknowledgment

---

## 📞 Emergency Helplines (India)

| Service | Number |
|---|---|
| 🚔 Police | **100** |
| 👩 Women Helpline | **1091** |
| 🆘 Emergency | **112** |
| 🏠 Domestic Violence | **181** |
| 💻 Cyber Crime | **1930** |
| 🏛️ National Commission for Women | **7827170170** |

---

## 🔮 Future Roadmap

- [ ] 🔴 **SOS Panic Button** — one-tap emergency alert with live tracking
- [ ] ✅ **Community Verification** — upvote/confirm reports for credibility
- [ ] 📊 **Area Safety Score** — 1-10 rating based on report density
- [ ] 🧠 **Context-Aware AI** — chatbot uses real database stats in responses
- [ ] 🌐 **Multi-language** — Hindi, Tamil, Telugu, Kannada support
- [ ] 📱 **Mobile App** — Flutter/React Native for always-on protection

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is built for the **Her-athon Hackathon**.

---

<p align="center">
  <b>Built with ❤️ for women's safety</b><br>
  <i>Because every woman deserves to feel safe.</i>
</p>