import uvicorn
import os
import sys
from datetime import datetime

# Import backend modules from the new structure
try:
    from backend import api, database, orchestrator
except ImportError:
    # Fallback for local execution without packages
    import backend.api as api
    import backend.database as database
    import backend.orchestrator as orchestrator

def run_intelligence_scrape():
    """
    Orchestrates the multi-source scraping and growth tracking logic.
    Uses the centralized orchestrator for consistency.
    """
    report_file = "output.txt"
    print(f"--- Startup Intelligence Engine (Automated Scrape) ---")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    results = orchestrator.run_scrape()
    
    if "error" in results:
        print(f"Error: {results['error']}")
        return

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"Scrape complete at {results['timestamp']}\n")
        f.write(f"Total Updated: {results['total_updated']}\n")
        f.write(f"New Startups: {results['new_count']}\n")
        f.write(f"Growing Startups: {results['growing_count']}\n")

    print(f"\nScrape complete. Updated {results['total_updated']} records.")

def start_dashboard():
    """
    Launches the FastAPI web server to host the Product Dashboard.
    """
    print("\n" + "="*60)
    print("🚀 STARTUP INTELLIGENCE ENGINE IS ONLINE")
    print("Dashboard: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    # Run FastAPI app
    uvicorn.run(api.app, host="localhost", port=8000, log_level="info")

if __name__ == "__main__":
    # Check for command line flags
    if "--scrape" in sys.argv:
        run_intelligence_scrape()
    else:
        # Default: Start the web dashboard
        # First, ensure the database exists
        database.create_table()
        start_dashboard()
