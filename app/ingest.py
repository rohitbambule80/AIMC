import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

CHROMA_PATH = "chroma_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    filename = os.path.basename(pdf_path)

    for doc in documents:

        doc.metadata["source"] = filename
        doc.metadata["manual_type"] = "AMM"
        doc.metadata["ata_chapter"] = "32"
        doc.metadata["aircraft"] = "A320"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=12
    )

    chunks = splitter.split_documents(documents)

    db = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=CHROMA_PATH
    )

    db.persist()

    print("PDF ingested successfully")
