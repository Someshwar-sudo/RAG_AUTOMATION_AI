import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
import google.genai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import traceback

load_dotenv()

app = FastAPI(
    title="RAG AI Automation ",
    description="Backend routing layer tracking and querying local corporate vector stores."
)

# 
API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = API_KEY  # Required for the LangChain embedding connector
ai_client = genai.Client(api_key=API_KEY)

# Initialize and connect to your existing local database folder
embedding_engine = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_db = Chroma(
    persist_directory="./chroma_db_storage", 
    embedding_function=embedding_engine
)
# Data Validation Contract schema
class ChatRequest(BaseModel):
    session_id: str
    user_message: str

@app.post("/api/chat")
def handle_chat(payload: ChatRequest):  # Synchronous to match Google's native network thread loop
    sid = payload.session_id
    message_text = payload.user_message

    try:
        # 1. Search ChromaDB for the top 3 closest matching policy paragraphs
        print(f" Searching local store for context matching: '{message_text}'")
        relevant_docs = vector_db.similarity_search(message_text, k=3)
        retrieved_context = "\n\n".join(
        [doc.page_content for doc in relevant_docs]
                    )

        print("Documents found:", len(relevant_docs))

        for i, doc in enumerate(relevant_docs):
            print(f"\n--- DOC {i+1} ---")
            print(doc.page_content[:300])

        # 2. Construct a strict System Prompt to prevent AI hallucinations
        rag_prompt = f""" You are a highly precise, fact-based AI assistant. Your only goal is to answer the user's query using STRICTLY the provided retrieved context.
                    Follow these rules to the letter:
                    1. GROUNDING: Base your answer entirely on the provided Context. Do NOT use any outside knowledge, assume unmentioned facts, or extrapolate.
                    2. CITATION: You must cite the exact source or document chunk used for your answer.
                    3. ADMISSION: If the provided Context does not contain the information required to answer the query, state exactly: "I do not have enough information in the retrieved context to answer this question." Do not attempt to guess or invent information.
                    4. REASONING: Before answering, break down the facts in the Context logically. Verify that the context explicitly supports your claim.
            

        VERIFIED MANUAL CONTEXT:
        {retrieved_context}

        EMPLOYEE QUESTION:
        {message_text}
        
        Answer Process:
        1. Identify relevant text from the Context.
        2. Draft the answer ensuring every sentence is supported by the Context.
        3. Provide the final answer with citations.
        """

        # 3. Request text generation from Gemini
        print("Routing context block to Gemini model layers...")
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=rag_prompt
        )

        # Return clean JSON back to Streamlit
        return {
            "status": "success",
            "session_id": sid,
            "response": response.text
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
        status_code=500,
        detail=str(e)
    )
