# 🏛 Mumbai Jan Seva — Citizen Grievance Redressal Portal

A full-stack civic complaint management system that allows citizens of Mumbai & Navi Mumbai to submit development requests and complaints directly to government officials in their respective wards.

## 🌟 Features

- **Citizen Registration & Login** — secure user accounts
- **Submit Complaints** — categorized complaints with live map pin-drop for location
- **Ward-based Routing** — complaints automatically routed to the correct regional official
- **Track by Ticket** — real-time status tracking with a visual progress timeline
- **Interactive Map** — live map showing all complaints across the city by status
- **Admin Dashboard** — government officials can view, filter, and update complaint statuses
- **Fully Responsive** — works on mobile and desktop

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, Flask |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Maps | Leaflet.js + OpenStreetMap |
| Fonts | Google Fonts (IBM Plex Sans) |

## 📁 Project Structure

```
mumbai-jan-seva/
├── app.py               # Flask app — routes, DB logic
├── requirements.txt     # Python dependencies
├── database.db          # Auto-created on first run
├── templates/
│   ├── base.html        # Shared nav/footer layout
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # Citizen complaint dashboard
│   ├── submit.html      # Submit complaint + map
│   ├── track.html       # Track by ticket number
│   ├── map.html         # Full city complaint map
│   └── admin.html       # Admin management dashboard
└── static/
    └── style.css        # All styles
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/mumbai-jan-seva.git
cd mumbai-jan-seva
pip install -r requirements.txt
python app.py
```

Open your browser at **http://127.0.0.1:5000**

### Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Citizen | Register a new account | — |
| Admin | admin@janseva.gov.in | admin123 |

## 📸 Screenshots

> *(Add screenshots here)*

## 🔮 Planned Improvements

- [ ] Email/SMS notifications on status updates
- [ ] Photo upload with complaints
- [ ] OTP-based mobile login
- [ ] Analytics dashboard with ward-wise heatmaps
- [ ] REST API for mobile app integration

## 👤 Author

**Satyabrata Nayak**  
B.Tech CSE, Ramrao Adik Institute of Technology  
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)

---

> Built to bridge the gap between citizens and local government in Mumbai.
