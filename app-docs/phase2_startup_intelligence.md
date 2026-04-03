# 📄 Phase 2 — Storage & Tracking (Startup Intelligence Engine)

## 🎯 Objective

Extend Phase 1 scraper to:
- Store startup data persistently
- Track changes over time
- Identify new and growing startups

---

# 🧠 What We Are Building (Phase 2 Scope)

```text
Scraper → Database → Change Detection → Console Output
```

---

# ⚙️ Tech Stack (Minimal & Practical)

| Component | Tool | Why |
|----------|------|-----|
| Language | Python | Already used |
| Database | SQLite | Built-in, no setup |
| DB Access | sqlite3 | Native Python module |
| Output | Console | Keep simple |

---

# 🏗️ Architecture

```text
scraper.py → database.py → tracker.py → main.py
```

---

# 📁 Project Structure

```text
startup-intelligence/
│
├── scraper.py
├── database.py
├── tracker.py
├── main.py
├── data.db
└── requirements.txt
```

---

# 🗄️ Database Design

## Table: startups

```sql
CREATE TABLE startups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    mrr INTEGER,
    date_added TEXT
);
```

---

# 🔧 Implementation Plan

## Step 1: Create database.py

Functions:
- create_table()
- insert_startup(data)
- get_all_startups()

---

## Step 2: Modify scraper output

Return list of dict:
```python
{
  "name": "...",
  "description": "...",
  "mrr": 5000
}
```

---

## Step 3: Store Data

For each scraped startup:
- Check if exists (by name)
- If not → insert
- If exists → compare MRR

---

## Step 4: Tracking Logic (tracker.py)

Detect:

### New Startup
- Not present in DB

### MRR Growth
- Existing name
- New MRR > old MRR

---

## Step 5: Output

```text
NEW STARTUPS:
- Product A ($2K)

GROWING STARTUPS:
- Product B (+$500)
```

---

# 🚀 Execution Flow

```text
1. Run scraper
2. Fetch data
3. Compare with DB
4. Insert/update
5. Print insights
```

---

# 🎯 Success Criteria (Phase 2 Done When)

✅ Database created  
✅ Data stored correctly  
✅ Duplicate entries avoided  
✅ New startups detected  
✅ MRR growth detected  
✅ Clean console output  

---

# ⚠️ Rules

- No ORM
- No frameworks
- Keep functions simple
- Focus on working logic

---

# 🤖 PROMPT FOR AGENT (PHASE 2)

You are a senior Python developer.

Build Phase 2 of a startup intelligence system.

Requirements:

1. Use SQLite (sqlite3)
2. Create table: startups
3. Store scraped data
4. Detect:
   - new startups
   - MRR growth
5. Print output in console

Constraints:
- No frameworks
- No ORM
- Keep code simple
- Use functions only

Goal:
Track startup data and detect changes over time.
