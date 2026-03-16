# 🌍 Financed Emissions & Climate Risk Advisor

A premium, RAG-powered (Retrieval-Augmented Generation) chatbot designed to assist financial institutions in navigating **PCAF (Partnership for Carbon Accounting Financials)** and **GHG Protocol** standards.

Live Link - https://neostatsassignment-dtfmcedp8pv542jwimg5ql.streamlit.app/

## 🚀 Key Features

- **Domain-Specific RAG**: Expertly tuned for financed emissions and climate risk documents.
- **Hybrid Search Fallback**: Automatically falls back to **Wikipedia** search when local PDF context is insufficient.
- **Premium Glassmorphic UI**: High-end aesthetic built with Streamlit, featuring custom typography and micro-animations.
- **Dual Response Modes**: Toggle between **Concise** summaries and **Detailed** technical explanations.
- **Fast Inference**: Powered by **Groq (Llama 3.1 8B)** for near-instant responses.

## 🛠️ Tech Stack

- **Frontend**: Streamlit (with custom CSS injection)
- **Orchestration**: LangChain
- **Vector Database**: ChromaDB (with local persistence)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **LLM**: Groq (Llama-3.1-8b-instant)
- **Search Fallback**: Wikipedia API

## 📁 Project Structure

```text
├── app.py                # Main Streamlit application
├── config/
│   └── config.py         # App configuration & environment loading
├── models/
│   ├── embeddings.py     # Local embedding model initialization
│   └── llm.py            # Groq LLM integration
├── utils/
│   ├── rag.py            # Vector DB & retrieval logic
│   └── search.py         # Wikipedia fallback search logic
├── chroma_db/            # Local vector database storage
├── documents/            # (Drop your PCAF/GHG PDFs here)
└── requirements.txt      # Python dependencies
```

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/financed-emissions-advisor.git
   cd financed-emissions-advisor
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🧪 Testing the Fallback Logic

To verify the "Hybrid Search" feature:
1. Ask a technical question about PCAF (e.g., "What is PCAF data quality score?").
2. Ask an unrelated question (e.g., "History of the Olympic Games").
3. Observe the `🔎 Searching the web...` toast message appearing for the latter.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ for sustainable finance and climate accountability.*
