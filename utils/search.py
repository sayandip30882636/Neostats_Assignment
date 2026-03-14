import logging
import logging
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

logger = logging.getLogger(__name__)

def perform_web_search(query):
    """
    Performs a stable web search using Wikipedia. 
    This is more reliable on cloud environments than real-time search engines.
    """
    try:
        api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=2000)
        search = WikipediaQueryRun(api_wrapper=api_wrapper)
        result = search.invoke(query)
        return result
    except Exception as e:
        logger.error(f"Stable search error: {str(e)}")
        return ""
