import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

# Cache the vector store
@st.cache_resource
def load_vectorstore():
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = FAISS.load_local(
            "vector_store/hdfc_faiss",
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore.as_retriever(search_kwargs={"k": 20})
    except Exception as e:
        st.error(f"Error loading vector store: {e}")
        return None

# Cache the QA chain
@st.cache_resource
def create_qa_chain():
    retriever = load_vectorstore()
    if retriever is None:
        return None
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192",
            temperature=0
        )
        return RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever
        )
    except Exception as e:
        st.error(f"Error initializing QA chain: {e}")
        return None

# Main App
def main():
    st.set_page_config(page_title="HDFC Credit Card Chatbot 💳", layout="centered")
    st.title("💳 HDFC Credit Card Q&A Chatbot")

    # Initialize session state for chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Stop Chat Button
    if st.button("🛑 Stop Chat"):
        st.write("Chat has been stopped. Thank you!")
        st.stop()

    # Input from user
    query = st.text_input("Ask a question about HDFC Credit Cards:")

    if query:
        qa_chain = create_qa_chain()
        if qa_chain:
            try:
                with st.spinner("Generating answer..."):
                    response = qa_chain.invoke(query)
                    answer = response.get("result", "Sorry, I couldn't find an answer.")
            except Exception as e:
                answer = f"Error during query: {e}"

            # Save to session history
            st.session_state.history.append((query, answer))

    # Display chat history
    if st.session_state.history:
        st.markdown("### 🤖 Chat History")
        for i, (q, a) in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.write("You:", q)
            st.write("Bot:", a)
            st.markdown("---")

if __name__ == "__main__":
    main()

