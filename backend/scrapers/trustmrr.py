import requests
from bs4 import BeautifulSoup

def clean_mrr(mrr_text):
    """
    Utility to convert human-readable MRR (e.g. '$2.6k', '$3,590,668') 
    into clean integers for database storage and analysis.
    """
    if not mrr_text or mrr_text == "N/A":
        return 0
    
    clean = mrr_text.replace("$", "").replace(",", "").strip().lower()
    
    multiplier = 1
    if "k" in clean:
        multiplier = 1000
        clean = clean.replace("k", "").strip()
    elif "m" in clean:
        multiplier = 1000000
        clean = clean.replace("m", "").strip()
    
    try:
        return int(float(clean) * multiplier)
    except (ValueError, TypeError):
        return 0

def scrape():
    """
    Scrapes verified startup revenue data from TrustMRR.
    Returns: list of dicts with name, mrr, description, source, and url.
    """
    base_url = "https://trustmrr.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching TrustMRR: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    startups = []

    # Strategy 1: Table listings (Leaderboard)
    rows = soup.find_all("tr", class_="group")
    for row in rows:
        name_el = row.select_one("div.font-medium.truncate")
        desc_el = row.select_one("div.text-xs.text-muted-foreground.truncate")
        mrr_el = row.select_one("td.text-right.font-mono.font-semibold")

        if name_el:
            name = name_el.get_text(strip=True)
            description = desc_el.get_text(strip=True) if desc_el else "N/A"
            mrr_val = mrr_el.get_text(strip=True) if mrr_el else "N/A"
            
            # Extract URL from the parent or nearby <a> tag
            url_tag = row.find_parent("a") or row.select_one("a") or row.find("a")
            link = url_tag["href"] if url_tag and url_tag.has_attr("href") else "/"
            if link.startswith("/"):
                link = base_url + link
            
            startups.append({
                "name": name,
                "mrr": clean_mrr(mrr_val),
                "description": description,
                "source": "TrustMRR",
                "url": link
            })

    # Strategy 2: Card listings (Recently listed)
    if len(startups) < 10:
        cards = soup.select("a.flex.flex-col.border")
        for card in cards:
            name_el = card.find("h3")
            desc_el = card.select_one("p.text-\[10px\]") or card.select_one("p.text-muted-foreground")
            mrr_el = card.select_one("p.font-mono.font-bold")

            if name_el:
                name = name_el.get_text(strip=True)
                if any(s["name"] == name for s in startups):
                    continue
                
                description = desc_el.get_text(strip=True) if desc_el else "N/A"
                mrr_val = mrr_el.get_text(strip=True) if mrr_el else "N/A"
                
                link = card["href"] if card.has_attr("href") else "/"
                if link.startswith("/"):
                    link = base_url + link
                
                startups.append({
                    "name": name,
                    "mrr": clean_mrr(mrr_val),
                    "description": description,
                    "source": "TrustMRR",
                    "url": link
                })

    return startups
