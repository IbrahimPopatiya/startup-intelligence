# 📄 Phase 3 — Insight Engine (Startup Intelligence Engine)

## 🎯 Objective

Convert stored startup data into actionable insights:
- Identify high-performing categories
- Detect trends
- Recommend what to build

---

# 🧠 What We Are Building (Phase 3 Scope)

```text
Database → Analyzer → Insight Engine → Console Output
```

---

# ⚙️ Tech Stack (Minimal & Practical)

| Component | Tool | Why |
|----------|------|-----|
| Language | Python | Continue same stack |
| Database | SQLite | Already built |
| Data Handling | sqlite3 + basic Python | Simple |
| AI (Optional) | OpenAI / Ollama | For better insights |
| Output | Console | Keep simple |

---

# 🏗️ Architecture

```text
database.py → analyzer.py → insights.py → main.py
```

---

# 📁 Project Structure

```text
startup-intelligence/
│
├── scraper.py
├── database.py
├── tracker.py
├── analyzer.py
├── insights.py
├── main.py
└── data.db
```

---

# 🔧 Implementation Plan

## Step 1: Fetch Data from Database

From database:
- name
- mrr
- description

---

## Step 2: Category Classification

### Option 1 (Simple Rule-Based)

```python
def get_category(desc):
    if "AI" in desc:
        return "AI Tool"
    elif "finance" in desc:
        return "Finance"
    return "Other"
```

---

### Option 2 (AI-Based — Optional)

Prompt:
Classify startup into one category using name + description.

---

## Step 3: Group Data

Group startups by category:

Example:
AI Tools → [5000, 8000, 2000]
Finance → [12000, 9000]

---

## Step 4: Calculate Metrics

For each category:
- Count of startups
- Average MRR
- Max MRR

---

## Step 5: Generate Insights

Logic:

- High avg MRR + low count → opportunity
- High count + growing MRR → trend

---

# 📊 Example Output

```text
TOP CATEGORIES:
1. Finance → Avg MRR: $12,000 (3 startups)
2. AI Tools → Avg MRR: $8,000 (10 startups)

OPPORTUNITY:
→ Finance SaaS (high revenue, low competition)

TREND:
→ AI Tools growing fast

RECOMMENDATION:
→ Build simple invoicing SaaS for freelancers
```

---

# 🚀 Execution Flow

```text
1. Fetch data from DB
2. Assign category
3. Group data
4. Calculate metrics
5. Print insights
```

---

# 🎯 Success Criteria (Phase 3 Done When)

✅ Categories generated  
✅ Data grouped correctly  
✅ Average MRR calculated  
✅ Insights printed clearly  
✅ At least 1 recommendation generated  

---

# ⚠️ Rules

- No complex ML
- No heavy AI dependency
- Keep logic simple
- Focus on usable insights

---

# 🤖 PROMPT FOR AGENT (PHASE 3)

You are a senior Python developer.

Build Phase 3 of a startup intelligence system.

Requirements:

1. Fetch startup data from SQLite
2. Classify into categories
3. Group by category
4. Calculate:
   - count
   - average MRR
   - max MRR
5. Generate insights:
   - best opportunity
   - trending category
6. Print clean output

Constraints:
- No frameworks
- Keep logic simple
- Use functions only

Goal:
Turn raw startup data into actionable insights.
