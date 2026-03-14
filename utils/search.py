import logging
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

def perform_web_search(query):
    """
    Performs a live web search using DuckDuckGo directly.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                # Combine snippets from results
                return "\n\n".join([f"Source: {r.get('href')}\nContent: {r.get('body')}" for r in results])
            return ""
    except Exception as e:
        logger.error(f"Critical search error: {str(e)}")
        return f"Error: {str(e)}"
