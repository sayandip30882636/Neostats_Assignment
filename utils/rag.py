import logging
import os
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from models.embeddings import get_embeddings

from chromadb.config import Settings

logger = logging.getLogger(__name__)

DB_DIR = "chroma_db"

def initialize_vector_db():
    try:
        embeddings = get_embeddings()
        
        # Ensure the directory exists
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
            
        # Disable telemetry to prevent cloud-env crashes
        settings = Settings(
            anonymized_telemetry=False,
            is_persistent=True,
            persist_directory=DB_DIR
        )
            
        vectorstore = Chroma(
            persist_directory=DB_DIR, 
            embedding_function=embeddings,
            client_settings=settings
        )
        return vectorstore
    except Exception as e:
        logger.error(f"Error initializing Vector DB: {str(e)}")
        # Return none instead of raising to allow app to fall back to search
        return None

def retrieve_context(query, vectorstore, k=3):
    """
    Retrieves context from the vector database.
    """
    try:
        docs = vectorstore.similarity_search(query, k=k)
        context = "\n".join([doc.page_content for doc in docs])
        return context
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        return ""
