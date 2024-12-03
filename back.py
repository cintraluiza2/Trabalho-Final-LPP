from flask import Flask, request, jsonify
from langchain import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from flask_cors import CORS
import os

# Inicialização do Flask
app = Flask(__name__)
CORS(app)

# Configurar LLM com LangChain
llm = OpenAI(
    temperature=0,
    openai_api_key="...",
    model_name="gpt-3.5-turbo-instruct"
)

# Carregar base de dados de entrevistas
data_dir = "dados_entrevistas/"  # Diretório onde estão os arquivos de texto
documents = []
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    if file_name.endswith(".txt"):
        loader = TextLoader(file_path)
        documents.extend(text_splitter.split_documents(loader.load()))

# Criar embeddings e vetorizar com FAISS
embeddings = OpenAIEmbeddings(openai_api_key="...")
vectorstore = FAISS.from_documents(documents, embeddings)

# Configurar memória para o histórico de conversa
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Criar cadeia de perguntas e respostas
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
qa_chain = load_qa_chain(llm, chain_type="stuff")  # Cadeia padrão para gerar respostas

# Função para busca no RAG com fallback
def answer_with_fallback(question):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    
    if docs:
        # Se encontrar documentos relevantes, usa o QA chain para gerar resposta
        response = qa_chain.run(input_documents=docs, question=question)
        return response
    else:
        # Fallback: usa apenas o modelo LLM para gerar uma resposta geral
        return llm.predict(question)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    position = data.get('position', 'General Position')  # Posição padrão
    query = f"Position: {position}. Question: {user_input}"

    # Recuperar documentos relevantes
    retrieved_docs = retriever.get_relevant_documents(query)

    # Gerar resposta com QA Chain
    response = qa_chain.run(input_documents=retrieved_docs, question=query)

    # Atualizar histórico de memória manualmente
    memory.save_context({"input": query}, {"output": response})
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='...', port=..., debug=True)
