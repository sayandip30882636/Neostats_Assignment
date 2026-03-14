import logging
from langchain_community.tools import DuckDuckGoSearchRun

logger = logging.getLogger(__name__)

def perform_web_search(query):
    """
    Performs a live web search using DuckDuckGo.
    """
    try:
        search = DuckDuckGoSearchRun()
        result = search.invoke(query)
        return result
    except Exception as e:
        logger.error(f"Error performing web search: {str(e)}")
        return "Web search is currently unavailable."
