from pathlib import Path
from datetime import datetime

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.config import (
    CHROMA_PERSIST_DIRECTORY,
    COLLECTION_NAME,
)
from app.rag.embeddings import get_embeddings


def extract_record_metadata(file_path: Path) -> dict:
    """
    Extract metadata from filenames such as:

    2025-08-10_lab_report.txt
    2025-01-20_prescription.txt
    demographics.txt
    """

    filename = file_path.name
    patient_id = file_path.parent.name

    record_date = None
    document_type = "medical_record"

    # Dated medical record
    if len(filename) >= 10:
        possible_date = filename[:10]

        try:
            datetime.strptime(possible_date, "%Y-%m-%d")
            record_date = possible_date

            remainder = file_path.stem[11:]

            if remainder:
                document_type = remainder

        except ValueError:
            pass

    if filename == "demographics.txt":
        document_type = "demographics"

    metadata = {
        "patient_id": patient_id,
        "source": filename,
        "document_type": document_type,
    }

    # Chroma metadata values should not be None
    if record_date:
        metadata["record_date"] = record_date

    return metadata


def load_documents(data_directory: str):
    documents = []

    data_path = Path(data_directory)

    for file_path in data_path.rglob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        metadata = extract_record_metadata(
            file_path
        )

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return documents


def create_vector_database(data_directory: str):

    documents = load_documents(
        data_directory
    )

    if not documents:
        raise ValueError(
            "No medical records found."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(
        documents
    )

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
    )

    print(
        f"Indexed {len(chunks)} chunks "
        f"from {len(documents)} documents."
    )

    return vectorstore


if __name__ == "__main__":

    create_vector_database(
        "./data/patient_records"
    )

    print(
        "Patient records successfully indexed."
    )