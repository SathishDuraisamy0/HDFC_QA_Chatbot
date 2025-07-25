import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.load_local(
        "vector_store/hdfc_faiss",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

@st.cache_resource
def create_qa_chain():
    retriever = load_vectorstore()
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
        temperature=0
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

def main():
    st.title("💳 HDFC Credit Card Q&A Chatbot")

    # Stop Chat Button
    if st.button("🛑 Stop Chat"):
        st.write("Chat has been stopped. Thank you!")
        st.stop()

    # Input box
    query = st.text_input("Ask a question about HDFC Cards:")

    # Process input
    if query:
        qa_chain = create_qa_chain()
        answer = qa_chain.invoke(query) 
        st.markdown("### 🤖 Latest Response")
        st.write("You:", query)
        st.write("Bot:", answer)
        st.markdown("---")

if __name__ == "__main__":
    main()
