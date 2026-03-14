import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.config import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

def get_embeddings():
    """
    Initializes and returns the HuggingFace embedding model for local RAG functionality.
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings: {str(e)}")
        raise e
