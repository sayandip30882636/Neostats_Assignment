import logging
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

logger = logging.getLogger(__name__)

def perform_web_search(query):
    """
    Performs a live web search using DuckDuckGo.
    """
    try:
        wrapper = DuckDuckGoSearchAPIWrapper(region="wt-wt", time="y", max_results=3)
        result = wrapper.run(query)
        return result
    except Exception as e:
        logger.error(f"Error performing web search: {str(e)}")
        return "Web search results are temporarily unavailable (possible rate limit)."
