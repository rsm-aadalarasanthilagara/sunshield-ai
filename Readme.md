# SunShield AI

**Your Campus Solar Planning Co-Pilot**

Turn urban heat into renewable energy with AI-powered site optimization.

[![DataHacks 2026](https://img.shields.io/badge/DataHacks-2026-green)](https://datahacks2026.devpost.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

---

## The Vision — Solar Shade Station

![AI-Generated Solar Shade Concept](AIGenSunShadeIdea.png)

**What it is:** Solar-powered public shade for extreme heat zones.

| Feature | Benefit |
|---|---|
| Solar roof | Powers lights and phone charging ports |
| Low-energy fans | Active cooling for pedestrians |
| Bamboo side shades | Passive cooling, sustainable materials |
| Seating area | Rest and recovery in high-traffic zones |

**Impact:**
- Reduces heat exposure in high-risk campus zones
- Increases comfort for pedestrians and outdoor workers
- Converts underutilized space into cooling infrastructure

This is designed for urban planners, but it directly serves pedestrians, outdoor workers, and vulnerable populations who are most affected by extreme heat.

---

## Problem

Campus planners waste **2-3 weeks** manually analyzing where to install solar shade structures. No tools integrate:
- Heat risk data
- Solar generation potential
- Budget optimization
- Stakeholder justification

**Result:** Suboptimal placement, wasted budgets, unprotected students.

---

## Solution

**SunShield AI** is a data-driven decision co-pilot that recommends optimal solar shade sites in 30 seconds.

**Key Innovation:** Dual-Benefit Score combining heat protection and renewable energy generation.

---

## How It Works

### 1. Set Your Budget

Use the interactive slider to define your planning budget. The optimizer instantly calculates which sites maximize impact per dollar.

![Budget Slider](1-Budget%20slider.png)

![ZenPower Industry Validation](zenpower_int.png)

- Decision tool for solar customer acquisition
- Data-driven ROI calculator
- Helps sell to universities
  
Integrated Sullivan Solar dataset with 6,192 real installation records (2012-2023). Analysis shows 4,996 California installations (80.7%) with 1,794 specifically in San Diego - providing strong local market validation for UCSD recommendations. Our live validation display proves our synthetic cost model ($27k-$45k) aligns with actual Sullivan Solar installation patterns. This grounds our recommendations in real-world pricing, making our tool credible for ZenPower's customer acquisition with educational institutions. Implementation includes interactive dashboard section showing real-time statistics from ZenPower dataset.

### 2. View Results and Export

Summary metrics update in real time. Export all sites or only the selected ones as CSV or GeoJSON for use in ArcGIS, QGIS, or Google Earth.

![Result Export](2-ResultExport.png)

### 3. Explore Selected Sites

Each recommended site shows a full breakdown: heat risk, solar potential, foot traffic, and feasibility score.

![Selected Sites](3-Selectedsites.png)

### 4. Compare All Candidates

The interactive map displays every candidate site color-coded by score, with selected sites highlighted.

![Other Sites on Map](4-OtherSites.png)

### 5. Campus Temperature Heat Map

Live sensor data from bike and walk traversals across UCSD campus is plotted as a color-coded temperature map.

![Campus Heatmap](5-CampusHeatmap.png)

### 6. AI-Powered Recommendations

The top recommended sites include AI-generated justification text ready to copy into grant proposals.

![Recommended Sites](6-RecommendedSites.png)

### 7. What-If Scenarios

Instantly see what changes if the budget increases or if the top site is skipped.

![What-If Scenario](7-WhatifScenario.png)

---

## Features

### Core Functionality
- **Heat Risk Analysis** - Real Scripps Institution sensor data
- **Solar Potential** - NREL government API integration
- **Public Impact** - Pedestrian traffic optimization
- **Budget Optimizer** - Greedy algorithm maximizes impact per dollar

### AI-Powered
- **Gemini Insights** - AI explains why each site was selected
- **Grant Generator** - Auto-generate justification text for proposals

### Professional Integration
- **GIS Export** - CSV and GeoJSON for ArcGIS, QGIS, Google Earth
- **Interactive Map** - Campus visualization with score overlays
- **Real-time Updates** - Adjust budget, see instant recommendations

---

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd SunShieldAI

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .env
cp .env.example .env

# Run the app
streamlit run src/frontend/app.py
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI | Gemini 2.0 Flash |
| Maps | Plotly Scattermap |
| Data | Scripps IOC, NREL PVWatts |
| Export | GeoJSON, CSV |
| Language | Python 3.11 |

---

*By Prompt Pioneer — DataHacks 2026*
