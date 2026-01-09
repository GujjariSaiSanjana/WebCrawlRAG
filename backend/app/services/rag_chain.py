from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.vector_store import get_vector_store
import os

def get_rag_chain():
    llm = Ollama(
        model="tinyllama",
        temperature=0.1
    )

    vector_db = get_vector_store()
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    template = """You are a helpful assistant that answers questions based ONLY on the provided context.
Do not describe the context, do not mention "the provided context", and do not explain your reasoning.
Just provide the direct answer in a natural way.

Context: {context}

Question: {question}

Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    return qa
