import os
from datetime import datetime
try:
    from . import database, tracker, analyzer
    from .scrapers import trustmrr, reddit, producthunt
except ImportError:
    import database, tracker, analyzer
    from scrapers import trustmrr, reddit, producthunt

def run_scrape():
    """
    Orchestrates the multi-source scraping, categorization, and growth tracking logic.
    Returns: dict with summary of the run.
    """
    # 1. Initialize DB
    database.create_table()
    db_history = database.get_latest_startups()

    # 2. Collect Data
    all_raw_data = []
    print("\n[1/3] Scraping TrustMRR...")
    all_raw_data.extend(trustmrr.scrape())
    print("\n[2/3] Scraping Reddit...")
    all_raw_data.extend(reddit.scrape())
    print("\n[3/3] Scraping Product Hunt...")
    all_raw_data.extend(producthunt.scrape())

    if not all_raw_data:
        return {"error": "No data collected from any source."}

    # 3. Categorize and Enrich
    for s in all_raw_data:
        s["category"] = analyzer.classify_startup(s.get("description", ""))
    
    # 4. Track Changes (MRR growth / New startups)
    new_startups, growing_startups = tracker.track_changes(all_raw_data, db_history)

    # 5. Insert into Database
    for s in all_raw_data:
        database.insert_startup(
            s["name"], 
            s["description"], 
            s["mrr"], 
            s.get("source", "Unknown"), 
            s.get("url", "N/A"),
            s.get("category", "Utility/Other")
        )

    return {
        "total_updated": len(all_raw_data),
        "new_count": len(new_startups),
        "growing_count": len(growing_startups),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
