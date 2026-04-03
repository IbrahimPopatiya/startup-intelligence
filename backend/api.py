from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

# Import our backend modules
try:
    from . import database, analyzer, insights, orchestrator
except ImportError:
    import database, analyzer, insights, orchestrator

app = FastAPI(title="Startup Intelligence Engine API")

# API Endpoints
@app.get("/api/insights")
def get_insights():
    """
    Returns full intelligence metrics including top categories, 
    market opportunities, and recommendations.
    """
    try:
        startups = database.get_all_startup_details()
        if not startups:
            return JSONResponse(content={"error": "Database is empty. Please run a scrape first."}, status_code=404)
        
        metrics = analyzer.calculate_category_metrics(startups)
        opportunities = insights.find_opportunities(metrics)
        trends = insights.detect_trends(metrics)
        recommendation = insights.get_recommendation(opportunities, startups)
        
        return {
            "categories": metrics,
            "opportunities": opportunities,
            "trends": trends,
            "recommendation": recommendation
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/scrape")
def trigger_scrape():
    """
    Triggers a live multi-source intelligence scrape via the orchestrator.
    """
    try:
        results = orchestrator.run_scrape()
        if "error" in results:
            return JSONResponse(content=results, status_code=500)
        return results
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/startups")
def get_startups():
    """
    Returns a full list of verified startups with their latest MRR and categorical data.
    """
    try:
        startups = database.get_all_startup_details()
        sorted_startups = sorted(startups, key=lambda x: x['mrr'], reverse=True)
        return sorted_startups
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Serve Frontend Static Files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
