from src.helper import repo_ingestion, load_repo, text_splitter, load_embedding

from dotenv import load_dotenv
from langchain_chroma import Chroma
import os

load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# url="https://github.com/msiemens/tinydb"

# repo_ingestion(url)

documents=load_repo("repo/")
text_chunk=text_splitter(documents)

embedding=load_embedding()

vectordb = Chroma.from_documents(text_chunk, embedding=embedding, persist_directory='./db')




