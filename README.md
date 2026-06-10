# RAG_AUTOMATION_AI
An enterprise-grade Generative AI assistant powered by RAG, ChromaDB vector search, and Google Gemini, delivering accurate context-aware responses.

**Architecture Flow**
User Interaction → User enters a query through the Streamlit chat interface.
FastAPI Backend → Receives the request and manages the RAG pipeline.
ChromaDB → Performs semantic similarity search and retrieves the most relevant document chunks.
Prompt Engineering → Retrieved context is combined with a strict prompt.
Google Gemini 2.5 Flash → Generates a context-aware response using the retrieved knowledge.
Response Delivery → The answer is returned to FastAPI and displayed in the Streamlit frontend.

## System Architecture
                    CortexAI System Architecture

                    [ User Browser Window ]
                              │
                 User Query / Chat Interaction
                              │
                              ▼
 ┌──────────────────────────────────────────┐
 │           Streamlit Frontend              │
 │      User Interface & Response Display    │
 │       (Runs on #http://localhost:8501)     │
 └───────────────────┬──────────────────────┘
                     │ HTTP POST Request
                     ▼
 ┌──────────────────────────────────────────┐
 │             FastAPI Backend               │
 │       API Layer & RAG Processing          │
 │       (Runs on #http://localhost:8000)     │
 └───────────────────┬──────────────────────┘
                     │
                     │ Semantic Similarity Search
                     ▼
 ┌──────────────────────────────────────────┐
 │          ChromaDB Vector Store            │
 │  Stores Document Embeddings & Retrieves   │
 │          Relevant Context Chunks          │
 └───────────────────┬──────────────────────┘
                     │
                     │ Context + Strict Prompt
                     ▼
 ┌──────────────────────────────────────────┐
 │            Google Gemini 2.5 Flash        │
 │     LLM Reasoning & Response Generation   │
 └──────────────────────────────────────────┘
                     │
                     ▼
              AI Generated Response
                     │
                     ▼
              Displayed in Streamlit UI

