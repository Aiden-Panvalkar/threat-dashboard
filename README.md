# 🛡️ AI-Powered Threat Intelligence Dashboard

A real-time cybersecurity threat intelligence dashboard that automatically 
aggregates threat data from multiple industry feeds and uses Google Gemini AI 
to generate plain-English threat summaries for security teams.

Built as part of a Cybersecurity internship at EY.

---

## 📋 Project Overview

Security teams today are overwhelmed by threat data arriving from dozens of 
sources in different formats. This dashboard solves that by:

- Automatically fetching live threat data from **AlienVault OTX** and **AbuseIPDB**
- Normalizing data from both sources into a unified format
- Storing everything in a **SQLite database**
- Displaying interactive charts, maps, and tables on a **Streamlit dashboard**
- Using **Google Gemini AI** to generate plain-English threat summaries on demand
- Running a **scheduler** that automatically refreshes data every 4 hours

---

## 🏗️ Project Architecture

```
threat-dashboard/
├── app/
│   ├── ai/
│   │   └── summarizer.py      # Gemini AI threat summarization
│   ├── db/
│   │   ├── database.py        # SQLite connection & initialization
│   │   └── models.py          # Threat data model
│   ├── feeds/
│   │   ├── otx.py             # AlienVault OTX feed fetcher
│   │   └── abuseipdb.py       # AbuseIPDB feed fetcher
│   ├── utils/
│   │   └── normalizer.py      # Data normalization across feeds
│   └── main.py                # Streamlit dashboard
├── scheduler.py               # Automated data fetching scheduler
├── requirements.txt           # Python dependencies
├── .env                       # API keys (never commit this)
└── .gitignore                 # Git ignore rules
```

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| Dashboard | Streamlit |
| Data Processing | Python, Pandas |
| Database | SQLite |
| AI Layer | Google Gemini 2.5 Flash |
| Threat Feeds | AlienVault OTX, AbuseIPDB |
| Scheduler | Python Schedule |
| Visualization | Plotly |

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd threat-dashboard
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root folder:

OTX_API_KEY=your_otx_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
GEMINI_API_KEY=your_gemini_key_here

Get your free API keys from:
- AlienVault OTX: https://otx.alienvault.com
- AbuseIPDB: https://www.abuseipdb.com
- Google Gemini: https://aistudio.google.com

### 5. Initialize the database
```bash
python app/db/database.py
```

### 6. Fetch initial threat data
```bash
python -m app.feeds.otx
python -m app.feeds.abuseipdb
```

### 7. Run the dashboard
```bash
python -m streamlit run app/main.py
```

### 8. (Optional) Run the scheduler
```bash
python scheduler.py
```
This will fetch fresh data every 4 hours automatically and clean up records 
older than 7 days.

---

## 📊 Features

- **Live Threat Metrics** — Total threats, high severity count, per-source breakdown
- **AI Summary** — One-click Gemini-powered plain English threat analysis
- **Threats by Source** — Donut chart showing OTX vs AbuseIPDB distribution
- **Severity Breakdown** — Bar chart of high/medium/low severity threats
- **Top Countries** — Geographic distribution of threat origins
- **Threat Explorer** — Filterable, searchable table of all IOCs

---

## 🔒 Security Notes

- Never commit your `.env` file — it is listed in `.gitignore`
- API keys are loaded at runtime using `python-dotenv`
- The SQLite database file is also excluded from Git via `.gitignore`

---

## 👤 Author

**Aiden Panvalkar**
