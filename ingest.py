import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

def process_and_store_pdf(file_path: str):
    print(f"Loading PDF file: {file_path}")
    
    # 1. Load the raw PDF pages into memory
    loader = PyPDFLoader(file_path)
    raw_pages = loader.load()
    print(f"Extracted {len(raw_pages)} pages from the document.")

    # 2. Slice text using a recursive character text splitter
    print("Chunking text into overlapping paragraphs...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(raw_pages)
    print(f"Successfully split document into {len(doc_chunks)} chunks.")

    # 3. Initialize the Google GenAI Text Embedding framework
    print("Generating mathematical vector embeddings...")
    embedding_engine = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # 4. Save chunks locally into your ChromaDB directory
    print("Writing database down to local 'chroma_db_storage' folder...")
    vector_db = Chroma.from_documents(
        documents=doc_chunks,
        embedding=embedding_engine,
        persist_directory="./chroma_db_storage"
    )
    
    print("Success! Your company manual is fully indexed and saved locally.")

if __name__ == "__main__":
    TARGET_FILE = "company_manual.pdf"
    if os.path.exists(TARGET_FILE):
        process_and_store_pdf(TARGET_FILE)
    else:
        print(f" Error: Please place your file named '{TARGET_FILE}' inside this folder first!")
