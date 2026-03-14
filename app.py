import streamlit as st
import logging

from config.config import PAGE_TITLE, PAGE_ICON
from models.llm import get_llm
from utils.rag import initialize_vector_db, retrieve_context
from utils.search import perform_web_search
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Must be the first Streamlit command
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Custom CSS for Premium Full-Stack Look
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* App Background Base */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
            color: #e2e8f0;
            font-family: 'Outfit', sans-serif;
            background-attachment: fixed;
        }

        /* Abstract Background Glows */
        .stApp::before {
            content: '';
            position: fixed;
            top: -10%; left: -10%;
            width: 50vw; height: 50vw;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 60%);
            z-index: 0; pointer-events: none;
        }
        .stApp::after {
            content: '';
            position: fixed;
            bottom: -10%; right: -10%;
            width: 40vw; height: 40vw;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.06) 0%, transparent 60%);
            z-index: 0; pointer-events: none;
        }

        /* Chat Message Area */
        .stChatMessage {
            background-color: transparent !important;
            padding: 0.5rem 0;
        }
        
        /* User Message Bubble */
        [data-testid="stChatMessage"]:nth-child(odd) {
            background: rgba(30, 41, 59, 0.5) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px 16px 4px 16px !important;
            padding: 1.25rem !important;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease;
        }
        [data-testid="stChatMessage"]:nth-child(odd):hover {
            border-color: rgba(56, 189, 248, 0.3) !important;
            transform: translateY(-2px);
        }
        
        /* Assistant Message Bubble */
        [data-testid="stChatMessage"]:nth-child(even) {
            background: rgba(15, 23, 42, 0.7) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(16, 185, 129, 0.15) !important;
            border-left: 4px solid #10b981 !important;
            border-radius: 16px 16px 16px 4px !important;
            padding: 1.25rem !important;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease;
        }
        
        /* Sidebar Styling (Glassmorphic) */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.65) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Inputs & Dropdowns */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background: rgba(30, 41, 59, 0.6) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px;
            font-family: 'Space Grotesk', sans-serif;
            transition: all 0.2s ease;
        }
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
        }

        /* Buttons Structure */
        .stButton button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        }
        .stButton button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        }

        /* Main Headers Styling */
        .main-title {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #38bdf8 !important;   /* Bright Blue Override */
            font-size: 3rem !important;
            font-weight: 800 !important;
            letter-spacing: -1px !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .sub-title {
            text-align: center;
            color: #94a3b8;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        /* Toggles */
        .st-emotion-cache-1jmwvnc {
            background-color: #10b981 !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vectorstore" not in st.session_state:
        try:
            st.session_state.vectorstore = initialize_vector_db()
        except Exception as e:
            st.error(f"Failed to initialize Vector DB: {str(e)}")
            st.session_state.vectorstore = None

def main():
    try:
        load_css()
        initialize_session_state()

        # Sidebar Configuration
        with st.sidebar:
            st.title(f"{PAGE_ICON} {PAGE_TITLE}")
            st.markdown("### Settings")
            
            st.info("Currently powered by Groq (llama-3.1-8b-instant)")
                
            response_mode = st.radio("Response Mode", ["Concise", "Detailed"])
            
            enable_search = st.toggle("Enable Live Web Search Fallback", value=True)
            
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()

        # Main Chat Area
        st.markdown(f"<h1 class='main-title'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Advising on PCAF and GHG Protocol standards.</p>", unsafe_allow_html=True)

        # Display Chat History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle User Input
        if prompt := st.chat_input("Ask about financed emissions or climate risk..."):
            # Append User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate Assistant Response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing climate data..."):
                    try:
                        # 1. RAG Retrieval
                        context = ""
                        if st.session_state.vectorstore:
                            context = retrieve_context(prompt, st.session_state.vectorstore)
                        
                        # 2. Web Search Fallback Check
                        search_results = ""
                        if enable_search and (not context or len(context.strip()) < 50):
                            st.toast("🔎 Searching the web for real-time info...", icon="🌐")
                            logger.info("Context insufficient, falling back to web search.")
                            search_results = perform_web_search(prompt + " PCAF GHG Protocol climate risk")
                            if search_results:
                                context += f"\\n\\nWeb Search Results:\\n{search_results}"

                        # 3. Formulate Prompt
                        system_prompt = (
                            "You are an expert Financed Emissions & Climate Risk Advisor. "
                            "You specialize in PCAF (Partnership for Carbon Accounting Financials) and GHG Protocol standards. "
                        )
                        
                        if response_mode == "Concise":
                            system_prompt += "Provide short, summarized, and direct answers. Be concise."
                        else:
                            system_prompt += "Provide in-depth, detailed, and comprehensive answers with clear structuring. Use markdown for better readability."
                            
                        if context or search_results:
                            system_prompt += f"\\n\\nUse the following retrieved context to answer the question:\\n{context}"

                        # 4. Initialize LLM & Get Response
                        llm = get_llm()
                        
                        messages = [
                            SystemMessage(content=system_prompt),
                            HumanMessage(content=prompt)
                        ]
                        
                        response = llm.invoke(messages)
                        answer = response.content

                        # Display and Save Response
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})

                    except ValueError as ve:
                        error_msg = f"Configuration Error: {str(ve)}. Please check your API keys."
                        st.error(error_msg)
                        logger.error(error_msg)
                    except Exception as e:
                        error_msg = f"An unexpected error occurred during generation: {str(e)}"
                        st.error(error_msg)
                        logger.error(error_msg)
                        
    except Exception as e:
        st.error(f"Critical App Failure: {str(e)}")
        logger.critical(f"App crashed: {str(e)}")

if __name__ == "__main__":
    main()
