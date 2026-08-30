import os
from git import Repo

# Document loaders & parsers
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

# Splitters & vectorstore
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Gemini LLM (still used for chat) + HuggingFace Embeddings (local, no quota)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# Chains & Memory
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationSummaryMemory






def repo_ingestion(repo_url):
    os.makedirs("repo", exist_ok=True)
    repo_path = "repo/"
    Repo.clone_from(repo_url, to_path=repo_path)


def load_repo(repo_path):
   loader = GenericLoader.from_filesystem(repo_path, glob = "**/*", suffixes=[".py"], parser = LanguageParser(language=Language.PYTHON, parser_threshold=500))
   documents=loader.load()
   return documents




def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, 
    chunk_size=1500, 
    chunk_overlap=150)
    text=documents_splitter.split_documents(documents)
    return text


def load_embedding():
    embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},        # change to 'cuda' if you have a GPU
    encode_kwargs={'normalize_embeddings': True} 
    ) 
    return embedding

