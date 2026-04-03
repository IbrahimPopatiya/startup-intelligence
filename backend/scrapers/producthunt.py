import requests
from bs4 import BeautifulSoup

def scrape():
    """
    Scrapes the daily list of products from Product Hunt.
    Returns: list of dicts with name, mrr, description, and source.
    """
    url = "https://www.producthunt.com/"
    startups = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com/"
    }
    
    print("Fetching from Product Hunt daily launches...")
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Select items from the homepage feed
        # Product Hunt changes their CSS often, so we look for 'post-item' data attributes
        posts = soup.select('div[data-test^="post-item-"]')
        
        for post in posts:
            # Extract basic data
            name_el = post.find('a', {'data-test': 'post-name'}) or post.find('h3')
            desc_el = post.find('p') or post.find('a', {'data-test': 'post-tagline'})
            
            # Extract Link
            link = "/"
            if name_el and name_el.has_attr("href"):
                link = name_el["href"]
            elif post.find("a"):
                link = post.find("a")["href"]
            
            if not link.startswith("http"):
                link = f"https://www.producthunt.com{link}"

            if name_el:
                name = name_el.get_text(strip=True)
                description = desc_el.get_text(strip=True) if desc_el else "New Product Launch"
                
                startups.append({
                    "name": name,
                    "mrr": 0,
                    "description": description,
                    "source": "Product Hunt",
                    "url": link
                })
        
        # Fallback for structured cards if 'all' page is restricted
        if not startups:
            titles = soup.find_all('a', {'data-test': 'post-item-title'})
            for title in titles:
                name = title.get_text(strip=True)
                link = title["href"] if title.has_attr("href") else "/"
                if not link.startswith("http"):
                    link = f"https://www.producthunt.com{link}"

                startups.append({
                    "name": name,
                    "mrr": 0,
                    "description": "Product Hunt Launch",
                    "source": "Product Hunt",
                    "url": link
                })

    except Exception as e:
        print(f"Error scraping Product Hunt: {e}")
            
    return startups
