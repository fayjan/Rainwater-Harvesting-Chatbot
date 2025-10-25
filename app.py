# app.py

# app.py
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA



# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please set it in .env file.")

# --- Continue as before ---
DATA_PATH = "data"
DB_PATH = "vectorstore"

# Load documents from data directory
def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

# Create or load vectorstore
def create_vectorstore():
    docs = load_documents()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectordb = Chroma.from_documents(splits, embedding=embeddings, persist_directory=DB_PATH)
    vectordb.persist()
    return vectordb

# Get or create vectorstore
def get_vectorstore():
    if os.path.exists(DB_PATH):
        return Chroma(persist_directory=DB_PATH, embedding_function=OpenAIEmbeddings(openai_api_key=api_key))
    else:
        return create_vectorstore()

# Build the QA chain
def build_qa_chain():
    vectordb = get_vectorstore()
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3, openai_api_key=api_key)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain

# Example utility function for rainwater harvesting calculations
def cost_savings(area_sqft, rainfall_mm, cost_per_litre=1.0):
    water_collected_litres = area_sqft * rainfall_mm * 0.001
    savings = water_collected_litres * cost_per_litre
    return savings

# End of app.py