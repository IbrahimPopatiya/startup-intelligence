import requests

def scrape():
    """
    Scrapes new startup mentions and side projects from Reddit.
    Targets r/SaaS and r/SideProject using public .json endpoints.
    
    Returns: list of dicts with name, mrr, description, and source.
    """
    subreddits = ["SaaS", "SideProject"]
    startups = []
    
    # User-Agent is mandatory for Reddit API access
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) StartupIntelligence/1.0"
    }

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=30"
        print(f"Fetching latest from r/{sub}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            children = data.get("data", {}).get("children", [])
            for post in children:
                p = post.get("data", {})
                
                title = p.get("title", "Unnamed Reddit Project")
                # Use subtext or title as the description for categorization
                description = p.get("selftext", "") or title
                
                # Small helper: Check if MRR is mentioned in the post
                # Example: "I hit $500 MRR"
                mrr_val = 0
                if "mrr" in description.lower():
                    # Very basic fallback for now - Phase 4 keeps it simple
                    import re
                    match = re.search(r'\$(\d+(?:,\d+)?k?)', description.lower())
                    if match:
                        from .trustmrr import clean_mrr
                        mrr_val = clean_mrr(match.group(1))

                # Extract post URL for deep-linking
                permalink = p.get("permalink", "")
                link = f"https://www.reddit.com{permalink}" if permalink else f"https://www.reddit.com/r/{sub}/new"

                startups.append({
                    "name": title[:80], # Limit name length
                    "mrr": mrr_val,
                    "description": description[:500], # Limit description length
                    "source": f"Reddit (r/{sub})",
                    "url": link
                })
        except Exception as e:
            print(f"Error scraping Reddit r/{sub}: {e}")
            
    return startups
