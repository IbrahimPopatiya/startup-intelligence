def classify_startup(description):
    """
    Simple keyword-based classifier to group startups into market categories.
    """
    if not description or description == "N/A":
        return "Utility/Other"
        
    desc = description.lower()
    
    # Simple Rule-Based Logic
    if any(k in desc for k in ["ai", "artificial intelligence", "gpt", "llm", "bot"]):
        return "AI Tools"
    if any(k in desc for k in ["finance", "fintech", "payment", "invoice", "bank", "tax"]):
        return "Finance"
    if any(k in desc for k in ["marketing", "seo", "ads", "social", "content", "outreach"]):
        return "Marketing"
    if any(k in desc for k in ["e-commerce", "shopify", "store", "product", "shipping"]):
        return "E-commerce"
    if any(k in desc for k in ["dev", "code", "developer", "api", "database"]):
        return "Dev Tools"
    if any(k in desc for k in ["saas", "software", "platform", "subscription"]):
        return "SaaS"
        
    return "Utility/Other"

def calculate_category_metrics(startups):
    """
    Aggregates metrics for each category.
    Returns a dictionary of category data points.
    """
    metrics = {}
    
    for startup in startups:
        category = classify_startup(startup["description"])
        mrr = startup["mrr"]
        
        if category not in metrics:
            metrics[category] = {
                "count": 0, 
                "total_mrr": 0, 
                "max_mrr": 0,
                "top_performer": ""
            }
        
        data = metrics[category]
        data["count"] += 1
        data["total_mrr"] += mrr
        
        if mrr >= data["max_mrr"]:
            data["max_mrr"] = mrr
            data["top_performer"] = startup["name"]
            
    # Finalize averages
    for category, data in metrics.items():
        data["avg_mrr"] = int(data["total_mrr"] / data["count"])
        
    return metrics
