**Component 1: Heat Risk (40%)** - Health priority
**Component 2: Solar Potential (30%)** - Financial sustainability
**Component 3: Public Impact (20%)** - Equity consideration
**Component 4: Feasibility (10%)** - Practical constraints

**Score Distribution:**
- Range: 65.4 - 87.4
- Mean: 74.8
- Std Dev: 5.2

### Budget Optimization Algorithm

**Greedy Selection:**
1. Sort by dual_benefit_score (descending)
2. Select highest until budget exhausted
3. Result: 98.2% budget utilization

**Example ($150k budget):**
- Selected 4 sites
- Total cost: $147,291
- Protected: 1,692 people daily
- Generated: 67,488 kWh/year

---

## Key Insights

### Finding 1: Parking Structures Concentrate Heat
- Top 3 sites all parking-related
- Hypothesis: Concrete amplifies urban heat island
- Impact: 60% of recommendations are parking structures

### Finding 2: Solar Varies by Microclimate
- Added site modifiers increased variance 26%
- Tree-lined walkways: -10-15% solar ROI
- Result: More realistic, credible recommendations

### Finding 3: Equity vs Efficiency Trade-off
- High-traffic sites serve 400+ people
- Remote areas serve <200 people
- Our approach: 80/20 rule (impact + equity)

---

## Data Visualization

**Interactive Dashboard:**
- Geo-spatial campus map (Plotly)
- Score breakdown charts
- Real-time budget adjustment
- What-if scenario analysis

**Export Integration:**
- CSV for Excel/analysis
- GeoJSON for ArcGIS/QGIS
- Direct integration with professional tools

---

## Technical Challenges Overcome

1. **API Rate Limiting:** Added throttling (1 req/sec)
2. **Flat Solar Scores:** Researched & applied shading factors
3. **Missing Data:** Evidence-based estimation with validation
4. **Edge Cases:** Graceful handling of budget constraints

---

## Impact

**Time Saved:** 2-3 weeks → 30 seconds
**Data Sources Integrated:** 3 (research + government + infrastructure)
**Decision Quality:** Quantified, defensible, reproducible
**Scalability:** Works for any campus with heat data

---

## Data Quality & Limitations

**Strengths:**
- Real research-grade sensors (Scripps)
- Validated government data (NREL)
- Transparent calculations

**Limitations:**
- Pedestrian estimates (not sensor-measured)
- Solar modifiers (approximations)
- Cost formulas (industry averages)

**Recommended Validation:**
- 2-week pedestrian counter pilot
- Detailed shade analysis surveys
- Actual contractor quotes

---

## Conclusion

We demonstrated that messy, fragmented climate data can be transformed into clear, actionable urban planning recommendations through thoughtful data engineering, validated analytics, and user-centered design.

**From sensors to decisions. That's data analytics.**

---

**Files:** 3 ETL scripts | 2 analytics modules | 1 interactive dashboard
**Pipeline:** 1,247 readings → 25 enriched sites → 4 optimized selections
**Result:** Decision co-pilot for urban planners
