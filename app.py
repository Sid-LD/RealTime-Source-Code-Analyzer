from langchain_chroma import Chroma
from src.helper import load_embedding, repo_ingestion
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationSummaryMemory

app=Flask(__name__)

load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embedding=load_embedding()
persist_directory='db'

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

llm=ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
)

memory=ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)

retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8})
qa = ConversationalRetrievalChain.from_llm(llm,retriever=retriever , memory=memory)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        repo_ingestion(user_input)
        os.system("python store_index.py")

    return jsonify({"response": str(user_input) })




@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)

    if input == "clear":
        os.system("rm -rf repo")

    result = qa(input)
    print(result['answer'])
    return str(result["answer"])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)