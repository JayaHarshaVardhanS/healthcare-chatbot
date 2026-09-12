from pathlib import Path

from langchain_chroma import Chroma

from app.config import (
    CHROMA_PERSIST_DIRECTORY,
    COLLECTION_NAME,
)

from app.rag.embeddings import get_embeddings
from app.rag.ingestion import create_vector_database


DATA_DIRECTORY = "data/patient_records"


def ensure_vectorstore_initialized():
    """
    Ensure the Chroma vector database exists and contains data.

    This is useful for cloud deployments where the local
    chroma_db directory is not committed to GitHub.
    """

    persist_path = Path(
        CHROMA_PERSIST_DIRECTORY
    )

    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
    )

    try:
        count = vectorstore._collection.count()
    except Exception:
        count = 0

    if count > 0:
        return vectorstore

    print(
        "\nChroma database is empty or missing."
    )

    print(
        "Creating vector database from patient records..."
    )

    create_vector_database(
        DATA_DIRECTORY
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
    )

    count = vectorstore._collection.count()

    print(
        f"Chroma initialization completed. "
        f"Indexed chunks: {count}"
    )

    return vectorstore


def get_vectorstore():

    return ensure_vectorstore_initialized()


def retrieve_documents(
    patient_id: str,
    query: str,
    k: int = 10,
):

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k,
        filter={
            "patient_id": patient_id
        },
    )

    return results