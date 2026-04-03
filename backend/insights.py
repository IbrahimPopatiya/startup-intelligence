def find_opportunities(metrics_dict):
    """
    Logic: Identify categories with high Average MRR but low Startup Count.
    These are 'underserved' markets with high revenue potential.
    """
    if not metrics_dict:
        return []

    # Get baseline averages across all categories
    avg_counts = [m["count"] for m in metrics_dict.values()]
    avg_mrr_vals = [m["avg_mrr"] for m in metrics_dict.values()]
    
    threshold_count = sum(avg_counts) / len(avg_counts)
    threshold_mrr = sum(avg_mrr_vals) / len(avg_mrr_vals)

    opportunities = []
    for category, data in metrics_dict.items():
        # High revenue, single-digit counts are ideal
        if data["avg_mrr"] > threshold_mrr and data["count"] <= threshold_count:
            opportunities.append({
                "category": category,
                "avg_mrr": data["avg_mrr"],
                "count": data["count"]
            })
    
    # Sort by MRR potential
    return sorted(opportunities, key=lambda x: x["avg_mrr"], reverse=True)

def detect_trends(metrics_dict):
    """
    Identify 'Hot' categories with high market density.
    """
    trends = []
    for category, data in metrics_dict.items():
        if data["count"] >= 10:
            trends.append(f"{category} is very active right now ({data['count']} startups listed).")
    
    return trends

def get_recommendation(opportunity_list, all_startups):
    """
    Generates a detailed 'Strategic Recommendation' with specific startup references.
    Prioritizes growth-based logic by looking at high-performing examples.
    """
    if not opportunity_list:
        return "The market is currently saturated with general tools. **Recommendation:** Build a micro-SaaS connecting AI models to legacy ERP systems. Focus on high-retention enterprise niches."

    # Take the top opportunity
    opt = opportunity_list[0]
    cat = opt["category"]
    
    # Find examples in this category to reference
    examples = [s["name"] for s in all_startups if s["mrr"] > 1000] # Simple heuristic for "successful"
    category_examples = [s for s in all_startups if cat.lower() in s["description"].lower() or cat.lower() in s["name"].lower()]
    category_examples = sorted(category_examples, key=lambda x: x["mrr"], reverse=True)[:2]
    
    ref_names = ", ".join([s["name"] for s in category_examples]) if category_examples else "market leaders"

    if cat == "Finance":
        return f"**Build a specialized automated billing tool for the Creator Economy.** With an average MRR of ${opt['avg_mrr']:,} in this space, there is massive room for niche players. Look at the success of **{ref_names}**—they prove that targeted financial workflows are highly profitable right now."
    
    elif cat == "Marketing":
        return f"**Launch a platform-specific analytics wrapper (e.g., for TikTok or Beehiiv).** Marketing tools are seeing a surge in 'Proof-of-Work' features. Follow the blueprint of **{ref_names}**, but focus on a younger, faster-moving demographic where competition is still low."
    
    elif cat == "E-commerce":
        return f"**Develop a 'Last-Mile' optimizer for boutique Shopify brands.** E-commerce density is low but revenue per startup is staggering (${opt['avg_mrr']:,}). Successful entries like **{ref_names}** show that brands are willing to pay a premium for tools that directly impact their conversion rates."

    elif cat == "AI Tools":
        return f"**Pivot from 'General AI' to 'Vertical AI' for legal or medical transcription.** While active, most players are generic. Referencing **{ref_names}**, you can see that specialized context-aware tools command 3x the subscription price of general wrappers."

    return f"**Focus on building a simplified, niche workflow tool in the {cat} sector.** Market data shows a high revenue floor with few competitors. Modeled after the growth patterns of **{ref_names}**, your first version should solve a single, painful data-entry problem for this specific audience."
