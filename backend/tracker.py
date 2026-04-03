def track_changes(scraped_startups, db_startups):
    """
    Compare current scrape results with the database to identify:
    1. New Startups (not in database)
    2. Growing Startups (current MRR > last stored MRR)
    
    Args:
        scraped_startups (list): Top current data from the scraper.
        db_startups (dict): Mapping of {name: last_mrr} from the database.
        
    Returns:
        tuple: (new_startups, growing_startups)
    """
    new_startups = []
    growing_startups = []

    for startup in scraped_startups:
        name = startup["name"]
        mrr = startup["mrr"]
        
        # Case 1: Detect New Startups
        if name not in db_startups:
            new_startups.append(startup)
        
        # Case 2: Detect MRR Growth
        else:
            old_mrr = db_startups[name]
            if mrr > old_mrr:
                # Store the growth value for display
                growth_delta = mrr - old_mrr
                startup["growth"] = growth_delta
                growing_startups.append(startup)
    
    return new_startups, growing_startups
