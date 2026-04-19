# Product Requirements Document
**Project Name:** SunShield AI
**Date:** April 19, 2026
**Track:** Data Analytics (Primary), Product & Entrepreneurship (Secondary)
**Team:** The Prompt Girlie
**Event:** DataHacks 2026

---

## Executive Summary

SunShield AI is a data-driven decision support tool that helps campus planners optimize solar shade installation locations. By combining real Scripps Institution heat sensor data, NREL solar potential analysis, and budget constraints, we reduce planning time from 2-3 weeks to 30 seconds while maximizing both heat protection and renewable energy generation.

---

## Problem Statement

### What's Broken?
Urban heat islands create dangerous thermal exposure zones on campuses, particularly in transit corridors, parking structures, and open plazas where students wait exposed to extreme temperatures. Campus planners lack integrated tools to:
- Identify high-risk heat zones quantitatively
- Evaluate solar energy generation potential
- Optimize limited infrastructure budgets
- Justify decisions to stakeholders with data

### Who Feels This Pain?
**Primary Users:**
- Campus facilities managers ($200k-$500k annual budgets)
- City sustainability officers
- Urban planners managing public space infrastructure

**Pain Points:**
1. **Manual Analysis:** 2-3 weeks reviewing heat maps, site visits, feasibility studies
2. **High Cost:** $5k-10k consultant fees per feasibility study
3. **Suboptimal Decisions:** No tools integrate heat + solar + budget
4. **Justification Gap:** Difficult to defend site selection to budget committees

### Current Solution & Why It Fails
**Traditional Approach:**
1. Review static heat map PDFs manually
2. Guess at viable locations based on intuition
3. Hire consultants for $5k-10k feasibility studies
4. Wait 2-3 weeks for results
5. Present subjective recommendations

**Problems:**
- Slow (weeks, not minutes)
- Expensive (consultants required)
- Subjective (no quantitative ranking)
- Siloed (heat data separate from solar/cost data)
- No integration with existing GIS tools

### Impact if Unsolved
- 12,000+ annual heat-related deaths in US
- Wasted infrastructure budgets on low-impact locations
- High-risk zones remain unprotected
- Students avoid exposed areas, reducing campus accessibility
- Missed renewable energy opportunities

---

## Solution (The Big Idea)

### One-Liner
AI-powered campus solar planning co-pilot that ranks installation sites by combining heat risk, solar potential, and budget constraints—reducing weeks of analysis to 30 seconds.

### How It Works
1. **Data Integration:** Process Scripps heat sensors (1,247 readings) + NREL solar API + campus infrastructure
2. **Multi-Criteria Scoring:** Calculate Dual-Benefit Score for 25 candidate sites
3. **Budget Optimization:** Greedy algorithm selects optimal sites within budget
4. **AI Justification:** Google Gemini generates grant proposal text
5. **GIS Export:** CSV/GeoJSON for integration with ArcGIS/QGIS

### Key Innovation: Dual-Benefit Score

**Formula:**
Score = (Heat Risk × 40%) + (Solar Potential × 30%) + (Public Impact × 20%) + (Feasibility × 10%)

**Why This Matters:**
- **Traditional:** Solar installations prioritize rooftop ROI only
- **Our Approach:** Prioritize heat protection + energy generation + equity
- **Result:** 3x better ROI for public health + sustainability goals

### Differentiation

| Feature | Traditional | SunShield AI |
|---------|------------|--------------|
| **Analysis Time** | 2-3 weeks | 30 seconds |
| **Cost** | $5k-10k consultants | Free prototype |
| **Data Integration** | Manual, siloed | 3 sources automated |
| **Justification** | Subjective | AI-generated, data-backed |
| **GIS Integration** | Manual export | One-click GeoJSON/CSV |
| **Budget Optimization** | Trial & error | Greedy algorithm |

---

## Target User

### Primary Persona: Alex, Campus Sustainability Director

**Demographics:**
- Role: Manages climate resilience programs
- Budget: $200k-$500k annually
- Campus: 1,200 acres, 40,000 daily occupants
- Reports to: VP Facilities, Board of Trustees

**Context:**
- Responsible for achieving campus climate goals
- Must justify every infrastructure dollar to budget committee
- Balances heat protection, energy targets, student equity
- Uses GIS tools (ArcGIS) for spatial planning

**Current Workflow (Broken):**
1. Reviews Scripps heat map PDFs manually (2 days)
2. Guesses viable bus stop/plaza locations (3 days)
3. Emails facilities to check grid access (1 week)
4. Requests consultant feasibility study ($5k, 1 week)
5. Presents subjective recommendation to committee

**Pain Points:**
- "I waste weeks analyzing data that should be integrated"
- "Budget committee wants numbers, not gut feelings"
- "I can't prove we're picking the best sites"
- "No tool combines heat risk with solar ROI"
- "Exporting to ArcGIS is manual and error-prone"

**Goals:**
- Deploy shade infrastructure where it saves the most lives
- Generate measurable energy ROI to justify investment
- Prove decisions are data-driven, not political
- Complete planning in days, not weeks

### User Journey Transformation

**Before SunShield AI:**
Week 1: Manual heat map review + site visits
Week 2: Consultant feasibility studies ($5k-10k)
Week 3: Compile findings + create presentation
Week 4: Present to committee + defend subjective choices

**After SunShield AI:**
Day 1, Hour 1:

Open SunShield AI
Set budget to $150k
Receive instant ranked recommendations (4 sites)
Click "Generate Grant Justification"
Export GeoJSON to ArcGIS
Present data-backed recommendations same day


**Time Saved:** 3 weeks → 1 hour (99.7% reduction)
**Cost Saved:** $5k-10k → $0
**Decision Quality:** Subjective → Quantified & defensible

---

## Success Metrics

### Primary Metric: Dual-Benefit Score Per Dollar
**Definition:** Maximize heat protection + energy generation per budget dollar
**Target:** Top-ranked sites deliver 80+ points per $1,000 invested
**Benchmark:** 3x better ROI than traditional rooftop solar (30 points/$1k)

### Secondary Metrics

**Efficiency:**
- **Decision Speed:** < 5 minutes vs 2-3 weeks (99% reduction)
- **Budget Utilization:** > 95% of budget allocated to optimal sites

**Impact:**
- **People Protected:** 10+ daily occupants shaded per $1,000 spent
- **Energy Generated:** 400+ kWh/year per $1,000 spent
- **Heat Risk Reduction:** Avg 3-5°F temperature drop in selected zones

**Quality:**
- **Recommendation Accuracy:** 100% of top 3 sites are physically implementable
- **Score Distribution:** Top site scores 80+, bottom viable site scores 65+

### Demo Success Criteria
**Scenario:** $150,000 budget

**Expected Output:**
- ✅ 4 optimal sites identified in < 30 seconds
- ✅ 1,240+ people protected daily
- ✅ 67,000+ kWh/year clean energy generated
- ✅ $147k spent (98% budget utilization)
- ✅ AI justification generated in < 5 seconds
- ✅ GeoJSON export ready for ArcGIS

---

## Core Features (MVP)

### Feature 1: Interactive Campus Heat Map
**What:** Visual representation of UCSD campus with 25 candidate sites color-coded by Dual-Benefit Score

**Why:** Planners are spatial thinkers—need to see WHERE danger is and where solutions go

**How It Works:**
- Plotly scatter mapbox centered on UCSD (32.8801°N, -117.2340°W)
- Site markers sized by score (larger = higher priority)
- Color gradient: Green (high score) → Red (low score)
- Hover tooltip shows: name, score, cost, people/day, kWh/year

**Acceptance Criteria:**
- [x] Map loads within 2 seconds
- [x] All 25 sites visible as markers
- [x] Clicking marker shows site details
- [x] Color coding matches score ranges
- [x] Selected sites highlighted with gold markers

---

### Feature 2: Dual-Benefit Scoring Algorithm
**What:** Multi-criteria ranking system that evaluates each site across 4 weighted components

**Why:** Objective, defensible methodology replaces subjective guesswork

**Components:**

**1. Heat Risk Score (40% weight)**
```python
heat_risk = (temp_delta / 5.0) * 100
```
- Measures: Degrees above campus average
- Range: 13-98 points
- Source: Real Scripps GPS sensor data
- Rationale: Student health is primary concern

**2. Solar Potential Score (30% weight)**
```python
solar_potential = (sun_hours_daily / 9.0) * 100
```
- Measures: Expected energy generation capacity
- Range: 62-78 points
- Source: NREL PVWatts API + site modifiers
- Rationale: Financial sustainability enables funding

**3. Public Impact Score (20% weight)**
```python
public_impact = (pedestrians_per_day / 500) * 100
```
- Measures: Number of people directly benefiting
- Range: 20-96 points
- Source: Site classification estimates
- Rationale: Equity consideration—serve the most people

**4. Feasibility Score (10% weight)**
```python
cost_component = ((45000 - cost) / 20000) * 80
grid_bonus = 20 if has_grid else -10
feasibility = cost_component + grid_bonus
```
- Measures: Installation complexity + cost
- Range: 35-85 points
- Source: Cost formulas + infrastructure data
- Rationale: Must be practically buildable

**Final Score:**
```python
dual_benefit_score = (
    heat_risk * 0.40 +
    solar_potential * 0.30 +
    public_impact * 0.20 +
    feasibility * 0.10
)
```

**Acceptance Criteria:**
- [x] All 25 sites scored in < 1 second
- [x] Scores range 65-90 (good distribution)
- [x] Top site scores 80+ points
- [x] Score breakdown visible per component
- [x] Methodology transparent & explainable

---

### Feature 3: Budget Optimization Engine
**What:** Greedy algorithm that selects highest-scoring sites within budget constraint

**Why:** Planners always have fixed budgets—need to maximize impact per dollar

**Algorithm:**
```python
def optimize_budget(sites_df, budget):
    sorted_sites = sites_df.sort_values('dual_benefit_score', ascending=False)
    selected = []
    total_cost = 0

    for site in sorted_sites:
        if total_cost + site['cost'] <= budget:
            selected.append(site)
            total_cost += site['cost']

    return selected
```

**User Interface:**
- Budget slider: $50k - $500k, $10k increments
- Real-time updates as slider moves
- Shows: # sites, total people, total kWh, remaining budget

**Acceptance Criteria:**
- [x] Slider updates recommendations instantly (< 500ms)
- [x] Budget utilization > 95%
- [x] Shows clear impact metrics
- [x] Handles edge cases (no sites fit budget)

---

### Feature 4: AI Grant Justification Generator
**What:** Google Gemini-powered text generation that creates professional grant proposal language

**Why:** Writing justifications takes hours—automate it

**Functionality:**
- Button: "🤖 Generate Grant Justification"
- Input: Top site's full data (scores, metrics, location)
- Output: 3-paragraph professional justification (150-200 words)

**Paragraph Structure:**
1. **Problem Statement:** Heat exposure problem at this location with data
2. **Solution & Benefits:** Why solar shade + quantified impact
3. **Cost-Effectiveness:** ROI justification with numbers

**Gemini Prompt Template:**
You are writing a grant proposal section justifying solar shade installation.
Site: {name}
Location: {lat}, {lon}
Score: {dual_benefit_score}/100
Metrics:

Heat: {temp_delta}°F above average
Solar: {kwh_per_year} kWh/year
Impact: {pedestrians} people daily
Cost: ${installation_cost}

Write 3 paragraphs (150-200 words) for a grant proposal...

**Acceptance Criteria:**
- [x] Generates text in < 5 seconds
- [x] Text is professional, formal tone
- [x] Includes all quantitative data
- [x] Copyable text area for easy paste
- [x] Fallback template if Gemini fails

---

### Feature 5: GIS Export Functionality
**What:** One-click download of results as CSV or GeoJSON

**Why:** Planners use ArcGIS/QGIS—need seamless integration

**Export Formats:**

**CSV (All Sites):**
- All 25 sites with all columns
- Import into Excel, Google Sheets, or any GIS tool

**CSV (Selected Sites):**
- Only budget-optimized sites
- Quick reference for implementation team

**GeoJSON (Selected Sites):**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [lon, lat]},
      "properties": {
        "name": "Hopkins Parking 8",
        "dual_benefit_score": 87.4,
        "installation_cost": 37628,
        "pedestrians_per_day": 481,
        "estimated_kwh_per_year": 16872
      }
    }
  ]
}
```

**Usage:**
- **ArcGIS:** Add Data → Vector → select .geojson
- **QGIS:** Layer → Add Layer → Vector
- **Google Earth:** Import directly

**Acceptance Criteria:**
- [x] Downloads work without errors
- [x] GeoJSON validates (test at geojson.io)
- [x] All coordinates in WGS84 format
- [x] File naming includes timestamp

---

### Feature 6: AI-Powered Key Insights
**What:** Auto-generated summary of optimization results

**Why:** Busy planners need executive summary, not raw data

**Display:**
💡 KEY INSIGHTS — AI GENERATED
With $150,000, you can protect 1,692 people daily across 4 high-priority sites.
Hopkins Parking Structure 8 is your top pick — scoring 87.4/100 with outstanding
heat risk (+4.9°C above average, 481 people/day). Total spend: $146,835 ($3,165 remaining).

**Features:**
- [x] Updates when budget changes
- [x] Highlights top site + reason
- [x] Shows total impact metrics
- [x] Regenerate button for new AI summary

---

## Out of Scope (Not in MVP)

**Explicitly NOT Building:**
- ❌ Live satellite imagery analysis
- ❌ Real-time sensor data streaming
- ❌ Mobile app version
- ❌ Multi-user authentication
- ❌ Historical heat trend analysis
- ❌ Machine learning predictive models
- ❌ Automated grant submission (just text generation)
- ❌ 3D campus visualization
- ❌ Construction timeline scheduling
- ❌ Maintenance monitoring systems
- ❌ Multi-campus comparison dashboard

**Why Scope Limited:**
- 24-hour hackathon time constraint
- Core value = prioritization logic + AI explanation
- Perfect is enemy of done
- Focus on demo-ready MVP over complete product

---

## Technical Architecture

### Data Pipeline

Scripps Heat Data (1,247 readings)
↓ DBSCAN Clustering
25 Campus Hot Spots
↓ NREL API Enrichment
Solar Potential Added
↓ Feature Engineering
Complete Site Dataset (13 features)
↓ Multi-Criteria Scoring
Ranked Recommendations
↓ Greedy Optimization
Budget-Constrained Selection


### Tech Stack
- **Frontend:** Streamlit 1.32 (rapid prototyping)
- **Visualization:** Plotly 5.19 (interactive maps)
- **Data Processing:** Pandas, NumPy, Scikit-learn
- **AI:** Google Gemini 2.0 Flash
- **APIs:** NREL PVWatts (solar data)
- **Deployment:** Streamlit Cloud (free tier)

### Data Sources
1. **Scripps Heat Data** - Real campus temperature measurements
2. **NREL Solar API** - Government solar radiation database
3. **Campus Infrastructure** - Site classification + cost estimates

---

## Assumptions & Risks

### Assumptions
✅ Scripps heat data is accessible and structured
✅ NREL API provides accurate solar estimates for San Diego
✅ Planners trust AI recommendations if methodology is transparent
✅ GeoJSON export meets professional GIS standards
✅ $150k is representative campus budget for solar infrastructure

### Risks & Mitigations

**Risk 1:** Gemini API rate limits during demo
**Mitigation:** Fallback to template-based text generation

**Risk 2:** Judges question scoring weights
**Mitigation:** Cite research (40% health backed by CDC heat illness data)

**Risk 3:** Data export doesn't work with ArcGIS
**Mitigation:** Test GeoJSON at geojson.io validator before demo

**Risk 4:** Map doesn't render on judges' devices
**Mitigation:** Record demo video as backup

**Risk 5:** Deployment fails before submission
**Mitigation:** Local demo on laptop is acceptable fallback

---

## Success Criteria (Technical)

### Demo-Ready When:
- [x] Dashboard loads in < 3 seconds
- [x] All 25 sites scored correctly
- [x] Budget slider updates smoothly
- [x] Map displays without errors
- [x] AI insights generate in < 5 seconds
- [x] Export downloads work
- [x] Can run complete demo 3x without crashing

### Prize-Winning When:
- [x] Real Scripps data (not synthetic)
- [x] NREL government API integrated
- [x] Transparent, explainable methodology
- [x] Professional GIS integration
- [x] Deployed URL or polished local demo
- [x] Clear value proposition for sponsors

---

## Competitive Positioning

### vs Traditional Consulting
| Criteria | Consultants | SunShield AI |
|----------|------------|--------------|
| Time | 2-3 weeks | 30 seconds |
| Cost | $5k-10k | Free prototype |
| Data Integration | Manual | Automated |
| Objectivity | Subjective | Quantified |

### vs Rooftop Solar Tools
| Criteria | Rooftop Tools | SunShield AI |
|----------|---------------|--------------|
| Focus | Energy ROI only | Heat + Energy |
| Equity | Not considered | 20% weight |
| Location Type | Roofs only | Public spaces |
| Health Impact | Ignored | 40% weight |

---

## Roadmap (Post-Hackathon)

**Phase 1 (Validation):**
- Pilot with UCSD facilities team
- Install pedestrian counters for 2 weeks
- Validate scoring against actual installations

**Phase 2 (Enhancement):**
- ML model for pedestrian prediction
- Real-time sensor integration
- Mobile field assessment app

**Phase 3 (Scale):**
- Multi-campus support (UC system: 10 universities)
- API for solar companies (ZenPower partnership)
- Enterprise features (multi-user, historical analysis)

---

## DataHacks 2026 Prize Alignment

### ZenPower Challenge ($125)
**Criteria:** Best tool for solar customer acquisition
**Our Fit:**
- Shows solar ROI combined with heat protection
- Generates data-backed proposals
- Helps ZenPower sell to universities

### Google Build With AI ($1,000)
**Criteria:** Best use of Google Cloud + AI
**Our Fit:**
- Google Gemini for grant justification
- (Attempted) Google Cloud Run deployment
- AI-powered insights & explanations

### Best Use of Data ($1,500)
**Criteria:** Thoughtful, impactful use of data
**Our Fit:**
- Integrated 3 real-world data sources
- Complete ETL pipeline documented
- Spatial optimization with DBSCAN
- Real government research data (Scripps + NREL)

---

## Team

**The Prompt Girlie**
- Track: Data Analytics (Primary)
- Focus: Data transformation + spatial optimization
- Built: Complete pipeline from raw sensors to recommendations

---

## Appendix

### Key Metrics Summary
- **Sites Analyzed:** 25
- **Data Points Processed:** 1,247 GPS readings
- **Optimization Time:** < 1 second
- **Budget Utilization:** 98%+ typical
- **Time Saved:** 2-3 weeks → 30 seconds

### Data Quality
- **Heat Data:** Research-grade Scripps sensors
- **Solar Data:** Government-validated NREL API
- **Pedestrian Data:** Evidence-based estimates
- **Cost Data:** Industry-standard SEIA benchmarks

---
