**.streamlit/config.toml:**
```toml
[theme]
primaryColor = "#F4C542"
backgroundColor = "#FAFAFA"
secondaryBackgroundColor = "#A7D7C5"
textColor = "#0B3D2E"

[server]
headless = true
port = 8501
```

**.streamlit/secrets.toml** (Streamlit Cloud dashboard):
```toml
GOOGLE_API_KEY = "your-gemini-key"
NREL_API_KEY = "your-nrel-key"
```

**.gitignore:**
pycache/
.pyc
venv/
.env
.streamlit/secrets.toml
.DS_Store
data/raw/.txt
---

## Dependencies Summary

### Core
- **Python:** 3.11+
- **Streamlit:** 1.32 (dashboard framework)
- **Pandas:** 2.2 (data manipulation)
- **Plotly:** 5.19 (interactive maps)

### Data Processing
- **NumPy:** 1.26 (numerical operations)
- **Scikit-learn:** 1.4 (DBSCAN clustering)
- **Requests:** 2.31 (NREL API calls)

### AI
- **google-generativeai:** 0.3.2 (Gemini API)

### Utilities
- **python-dotenv:** 1.0.1 (environment variables)

---

## File Structure
sunshield-ai/
├── src/
│   ├── data/                      # ETL scripts
│   │   ├── process_scripps_data.py
│   │   ├── enrich_solar_data.py
│   │   └── finalize_sites.py
│   ├── agent/                     # Analytics
│   │   ├── scoring.py
│   │   └── optimizer.py
│   └── frontend/                  # Streamlit app
│       └── app.py
├── data/
│   ├── raw/                       # Original Scripps data
│   ├── processed/                 # Intermediate CSVs
│   └── sample/                    # Final dataset
│       └── ucsd_sites_scored.csv
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml              # Gitignored
├── skills/                        # Documentation
│   ├── PRD.md
│   ├── Techstack.md
│   └── Workflow.md
├── .gitignore
├── requirements.txt
├── README.md
├── DATA_STORY.md
└── DEVPOST_SUBMISSION.md

---

## Performance

### Response Times
- Dashboard load: < 3 seconds
- Scoring 25 sites: < 1 second
- Budget optimization: < 500ms
- Gemini API call: 3-5 seconds
- Map render: < 2 seconds

### Data Pipeline
- Scripps clustering: ~10 seconds
- NREL enrichment: ~25 seconds (25 sites × 1 req/sec)
- Total ETL: ~40 seconds one-time

---

## Security & Configuration

### API Keys (Environment Variables)
```python
# Local development: .env file
GOOGLE_API_KEY=your-key-here
NREL_API_KEY=your-key-here

# Streamlit Cloud: secrets.toml in dashboard
# Never commit .env or secrets.toml to GitHub
```

### Data Privacy
- No PII collected
- GPS coordinates are public campus locations
- Temperature data aggregated, not individual

---

## Scalability Notes

**Current (MVP):**
- 25 sites (in-memory processing)
- Single-user, synchronous
- File-based data (CSV)

**Future Enhancements:**
- Multi-campus support (UC system: 10 campuses)
- Real-time sensor streaming
- Database storage (PostgreSQL)
- Caching layer (Redis for NREL API)

---

## Prize Alignment

### ZenPower ($125)
✅ Decision tool for solar placement
✅ ROI calculator (dual benefits)
✅ Helps sell to universities

### Google Build With AI ($1,000)
✅ Gemini 2.0 Flash integration
✅ Cloud deployment (Streamlit Cloud)
✅ AI-powered insights & justifications

### Best Use of Data ($1,500)
✅ 3 real-world data sources integrated
✅ Complete ETL pipeline documented
✅ Spatial optimization (DBSCAN)
✅ Government research data (Scripps + NREL)

---

## Known Limitations

**MVP Constraints:**
- Static dataset (not real-time sensors)
- Simplified cost model (not contractor quotes)
- Synthetic pedestrian data (not actual counters)
- Greedy optimization (not mathematical optimization)

**NOT Building:**
- ML models (rule-based sufficient)
- Multi-user authentication
- Mobile app
- Automated sensor integration

---

## Development Tools

- **Editor:** VS Code
- **Version Control:** Git + GitHub
- **Testing:** Manual (3x full demo runs)
- **API Testing:** Streamlit interactive mode

---

**Last Updated:** April 19, 2026
**Status:** Production-ready for demo
**Deployment:** GitHub + Streamlit Cloud
