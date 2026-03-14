import logging
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

logger = logging.getLogger(__name__)

def get_llm(model_name="llama-3.1-8b-instant", temperature=0.7):
    """
    Initializes and returns the Groq LLM.
    """
    try:
        # Check API key before instantiation
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing or invalid.")
        return ChatGroq(model_name=model_name, temperature=temperature, groq_api_key=GROQ_API_KEY)
            
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise e
