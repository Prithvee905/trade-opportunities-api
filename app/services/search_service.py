import logging
from duckduckgo_search import DDGS
from typing import List, Dict

logger = logging.getLogger(__name__)

def search_sector_news(sector: str) -> List[Dict[str, str]]:
    """
    Search latest Indian market data about the given sector using DuckDuckGo search.
    Returns 5-8 results. Each result includes title, summary, and url.
    """
    try:
        query = f"{sector} sector Indian market latest news OR trade opportunities"
        logger.info(f"Searching DuckDuckGo with query: {query}")
        
        results = []
        with DDGS() as ddgs:
            # Getting max 8 results
            search_results = ddgs.text(query, max_results=8)
            
            for index, res in enumerate(search_results):
                # Ensure we have at least 5 results and cap at 8
                if index >= 8:
                    break
                    
                results.append({
                    "title": res.get("title", "No Title"),
                    "summary": res.get("body", "No Summary"),
                    "url": res.get("href", "No URL")
                })
                
        return results

    except Exception as e:
        logger.error(f"Failed to search news for sector {sector}. Error: {e}")
        # Raising an exception here so that the route handler can manage the error properly
        raise Exception(f"Failed to fetch market data: {str(e)}")
