from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "chroma_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)

pipe = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_new_tokens=256
)

llm = HuggingFacePipeline(pipeline=pipe)


def ask_question(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an aerospace maintenance AI assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    citations = []

    for doc in docs:

        citations.append({
            "source": doc.metadata.get("source"),
            "ata": doc.metadata.get("ata_chapter"),
            "manual_type": doc.metadata.get("manual_type")
        })

    return {
        "answer": response,
        "citations": citations
    }
