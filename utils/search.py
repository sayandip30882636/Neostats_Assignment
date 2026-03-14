import logging
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

logger = logging.getLogger(__name__)

def perform_web_search(query):
    """
    Performs a live web search using Wikipedia as a reliable fallback.
    """
    try:
        api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
        search = WikipediaQueryRun(api_wrapper=api_wrapper)
        result = search.invoke(query)
        return result
    except Exception as e:
        logger.error(f"Error performing web search: {str(e)}")
        return "Web search is currently unavailable."
