from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from app.services.vector_store import get_vector_store


def get_rag_chain():
    llm = ChatOllama(
    model="tinyllama",
    temperature=0,
    num_ctx=512,
    system="Answer clearly in short paragraphs. Avoid unnecessary code unless asked."
)

    vector_db = get_vector_store()
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})  # fewer docs

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    return qa
