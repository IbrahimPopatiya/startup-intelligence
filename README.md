# 🚀 Startup Intelligence Engine

> **Automatically scrape, track, analyze, and visualize MRR data from indie startups — powered by Python, FastAPI, and SQLite.**

A self-contained intelligence system that collects data from **TrustMRR**, **Product Hunt**, and **Reddit**, detects new and growing startups, categorizes them, and surfaces actionable insights through a web dashboard.

---

## 📸 Dashboard Preview

The web dashboard runs locally at `http://localhost:8000` and provides:
- 📊 Category-based market breakdowns
- 🔍 Global startup search
- 📈 Trend detection & opportunity insights
- ▶️ One-click "Run Intelligence Scrape" button

---

## 🧠 How It Works

```
[TrustMRR + ProductHunt + Reddit]
          ↓ Scrape
      Orchestrator
          ↓ Merge & Categorize
       SQLite DB
          ↓ Analyze
    Insights Engine
          ↓ Serve
  FastAPI + Web Dashboard
```

---

## ⚙️ Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Language    | Python 3.10+                        |
| Backend API | FastAPI + Uvicorn                   |
| Scraping    | Requests + BeautifulSoup4           |
| Database    | SQLite (via stdlib `sqlite3`)       |
| Frontend    | HTML + Vanilla CSS + JavaScript     |
| Automation  | Windows Task Scheduler / cron       |

---

## 📁 Project Structure

```
startup-intelligence/
│
├── main.py                    # ← Entry point (dashboard + scrape CLI)
├── requirements.txt           # ← Python dependencies
├── data.db                    # ← SQLite database (auto-created)
├── output.txt                 # ← Last scrape report (auto-generated)
│
├── backend/
│   ├── __init__.py
│   ├── api.py                 # FastAPI routes (/api/insights, /api/startups, /api/scrape)
│   ├── database.py            # SQLite CRUD operations
│   ├── analyzer.py            # Category classification & MRR metrics
│   ├── insights.py            # Opportunity detection & recommendations
│   ├── orchestrator.py        # Scraping pipeline coordinator
│   ├── tracker.py             # New startup & MRR growth detection
│   │
│   └── scrapers/
│       ├── __init__.py
│       ├── trustmrr.py        # TrustMRR.com scraper
│       ├── producthunt.py     # Product Hunt scraper
│       └── reddit.py          # Reddit (r/SaaS, r/startups) scraper
│
├── frontend/
│   └── index.html             # Single-page web dashboard
│
└── app-docs/
    ├── phase2_startup_intelligence.md
    ├── phase3_startup_intelligence.md
    ├── phase4_startup_intelligence.md
    └── phase5_startup_intelligence.md
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/IbrahimPopatiya/startup-intelligence.git
cd startup-intelligence
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### ▶️ Start the Web Dashboard

```bash
python main.py
```

- Dashboard: [http://localhost:8000](http://localhost:8000)
- API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

> The database is automatically initialized on first run.

---

### 🔄 Run an Intelligence Scrape (CLI)

```bash
python main.py --scrape
```

This will:
1. Scrape TrustMRR, Product Hunt, and Reddit
2. Detect new and growing startups
3. Store all data to `data.db`
4. Save a summary report to `output.txt`

---

## 🌐 API Endpoints

| Method | Endpoint         | Description                                      |
|--------|------------------|--------------------------------------------------|
| `GET`  | `/api/startups`  | Returns all startups sorted by MRR (desc)        |
| `GET`  | `/api/insights`  | Returns category metrics, opportunities, trends  |
| `POST` | `/api/scrape`    | Triggers a live multi-source scrape              |
| `GET`  | `/docs`          | Interactive Swagger UI                           |

---

## ⚡ Automate Daily Scraping

### Windows Task Scheduler

1. Open **Task Scheduler** → Create Basic Task
2. Set trigger: **Daily**
3. Set action: `python C:\path\to\startup-intelligence\main.py --scrape`
4. Set **Start In** to: `C:\path\to\startup-intelligence`

### Linux / Mac (cron)

```bash
# Run every day at 8:00 AM
0 8 * * * cd /path/to/startup-intelligence && .venv/bin/python main.py --scrape
```

---

## 📊 Sample Output (`output.txt`)

```
Scrape complete at 2026-04-02 08:00:00
Total Updated: 47
New Startups: 5
Growing Startups: 3
```

---

## 📖 Build Documentation

See [BUILD_JOURNEY.md](./BUILD_JOURNEY.md) for the full chronological breakdown of how this system was designed and built from Phase 1 to Phase 5.

---

## 📄 License

MIT — free to use, fork, and build upon.
