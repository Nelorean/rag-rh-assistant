import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

#contexto
def load_pdf():
    py_pdf_loader = PyPDFLoader("politica_rh.pdf")
    text = py_pdf_loader.load()
    return text

def split_into_chunks(documents):
    spliter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    block_list = spliter.split_documents(documents)
    return block_list

@st.cache_resource
def build_vector_storage() -> FAISS:
    documents = load_pdf()
    chunks = split_into_chunks(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    return FAISS.from_documents(chunks, embeddings)

vector_storage = build_vector_storage()

#agente
def create_chain_agent(vector_storage: FAISS):
    prompt_template = ChatPromptTemplate.from_template(
        """Você é um assistente de RH que responde perguntas sobre políticas internas da empresa.
    Use APENAS as informações do contexto abaixo para responder.
    Se não encontrar a resposta, diga claramente que não sabe responder.
    Responda em português do Brasil, de forma clara e objetiva.
    Contexto: {context}
    A pergunta: {question}
    Resposta:""")

    context_catcher = vector_storage.as_retriever()
        
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
    
    chain = ({"context": context_catcher, "question": RunnablePassthrough()} 
             | prompt_template 
             | llm 
             | StrOutputParser())
    
    return chain


#interface
st.title("Assistente - Políticas Internas")

chain = create_chain_agent(vector_storage)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt= st.chat_input("Pergunte sobre as políticas da empresa...")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando..."):
            answer = chain.invoke(prompt)
            st.write(answer)

    st.session_state["messages"].append({"role":"assistant","content": answer})