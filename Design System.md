# 🌱 SunShield AI

**Your Campus Solar Planning Co-Pilot**

Turn urban heat into renewable energy with AI-powered site optimization.

[![DataHacks 2026](https://img.shields.io/badge/DataHacks-2026-green)](https://datahacks2026.devpost.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

---

## 🎯 Problem

Campus planners waste **2-3 weeks** manually analyzing where to install solar shade structures. No tools integrate:
- Heat risk data
- Solar generation potential
- Budget optimization
- Stakeholder justification

**Result:** Suboptimal placement, wasted budgets, unprotected students.

---

## 💡 Solution

**SunShield AI** = Data-driven decision co-pilot that recommends optimal solar shade sites in 30 seconds.

**Key Innovation:** Dual-Benefit Score combining heat protection + renewable energy generation.

---

## ✨ Features

### Core Functionality
- 🔥 **Heat Risk Analysis** - Real Scripps Institution sensor data
- ☀️ **Solar Potential** - NREL government API integration
- 👥 **Public Impact** - Pedestrian traffic optimization
- 💰 **Budget Optimizer** - Greedy algorithm maximizes impact per dollar

### AI-Powered
- 🤖 **Gemini Insights** - AI explains why each site was selected
- 📝 **Grant Generator** - Auto-generate justification text for proposals

### Professional Integration
- 📥 **GIS Export** - CSV & GeoJSON for ArcGIS, QGIS, Google Earth
- 🗺️ **Interactive Map** - Campus visualization with score overlays
- 📊 **Real-time Updates** - Adjust budget, see instant recommendations

---

## 📊 Demo Results

**Example: $150,000 Budget**
✅ 4 Sites Selected
👥 1,692 People Protected Daily
⚡ 67,488 kWh/Year Generated
💵 $147,099 Spent (98% utilization)
**Top Site:** Hopkins Parking Structure 8
- Score: 87.4/100
- Heat: 4.9°F above average
- Impact: 481 people/day
- Energy: 16,872 kWh/year
- Cost: $37,628

---

## 🏗️ Architecture

### Data Pipeline
Scripps GPS Data (1,247 readings)
↓ DBSCAN Clustering
25 Campus Hot Spots
↓ NREL API Enrichment
Solar Potential Added
↓ Feature Engineering
Complete Site Dataset
↓ Multi-Criteria Scoring
Ranked Recommendations
### Dual-Benefit Score Formula
Score = (Heat Risk × 40%) +
(Solar Potential × 30%) +
(Public Impact × 20%) +
(Feasibility × 10%)
### Tech Stack
- **Data:** Python, Pandas, Scikit-learn (DBSCAN)
- **Analytics:** Custom scoring algorithm
- **Frontend:** Streamlit, Plotly
- **AI:** Google Gemini 2.0 Flash
- **APIs:** NREL PVWatts, Scripps Heat Data

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- NREL API key ([get free](https://developer.nrel.gov/signup/))
- Google API key (for Gemini)

### Installation

```bash
# Clone repo
git clone https://github.com/YOUR-USERNAME/sunshield-ai.git
cd sunshield-ai

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env and add your keys

# Run app
streamlit run src/frontend/app.py
```

App opens at `http://localhost:8501`

---

## 📁 Project Structure
sunshield-ai/
├── src/
│   ├── data/                  # ETL pipeline
│   │   ├── process_scripps_data.py
│   │   ├── enrich_solar_data.py
│   │   └── finalize_sites.py
│   ├── agent/                 # Scoring & optimization
│   │   ├── scoring.py
│   │   └── optimizer.py
│   └── frontend/              # Streamlit dashboard
│       └── app.py
├── data/
│   ├── raw/                   # Original Scripps data
│   ├── processed/             # Intermediate CSVs
│   └── sample/                # Final scored dataset
├── screenshots/               # Demo screenshots
├── DATA_STORY.md             # Analytics documentation
├── requirements.txt
└── README.md
---

## 🎓 DataHacks 2026

### Tracks
- **Data Analytics** (Primary)
- Product & Entrepreneurship

### Challenges
- 💰 ZenPower Challenge ($125)
- ☁️ Google Build With AI ($1,000)
- 🏆 Best Use of Data ($1,500)

### Team
**The Prompt Girlie**

---

## 📈 Key Insights

### Finding 1: Parking Structures Concentrate Heat
Top 3 sites all parking-related. Concrete amplifies urban heat island effect.

### Finding 2: Solar Varies by Microclimate
Applied site-specific shading modifiers (trees, buildings) → 26% score variance

### Finding 3: Equity vs Efficiency Trade-off
High-traffic sites (400+ people) vs remote areas (<200). Balanced with 80/20 rule.

---

## 🔮 What's Next

- **Pilot:** UCSD facilities team validation
- **Validation:** 2-week pedestrian counter study
- **Extension:** Solar trash compactors, bus shelters, charging stations
- **Scale:** Multi-campus support (UC system: 10 campuses)
- **Partnership:** Integrate with ZenPower sales workflow

---

## 📄 Documentation

- **[DATA_STORY.md](DATA_STORY.md)** - Complete data analytics methodology
- **[PRD.md](skills/PRD.md)** - Product requirements
- **[Techstack.md](skills/Techstack.md)** - Technical architecture
- **[Workflow.md](skills/Workflow.md)** - User journey

---

## 🤝 Contributing

This project was built during DataHacks 2026. Future contributions welcome!

**Areas for improvement:**
- Real-time sensor integration
- ML-based pedestrian prediction
- Mobile app for field assessment
- Multi-campus dashboard

---

## 📜 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- **Scripps Institution of Oceanography** - Heat sensor data
- **NREL (US Dept of Energy)** - Solar radiation API
- **ZenPower** - Challenge inspiration
- **DataHacks 2026** - Event organizers
- **Google Cloud** - Infrastructure support

---

## 📧 Contact

**Team:** The Prompt Girlie
**Event:** DataHacks 2026
**Email:** [your-email]
**Demo:** [Streamlit Cloud URL when deployed]

---

*From weeks of guesswork to minutes of clarity.*
