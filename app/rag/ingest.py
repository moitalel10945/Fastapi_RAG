
import re
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Connect to Chroma
client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="property_manual",
    embedding_function=embedding_function
)


# Load the manual
document_path = Path("documents/tenant_manual.txt")
text = document_path.read_text(encoding="utf-8")


# Split the manual into named sections
section_pattern = re.compile(
    r"(?m)^(TENANT REGISTRATION|RENT PAYMENTS|REPORTS)\s*$"
)

matches = list(section_pattern.finditer(text))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunk_ids = []
chunk_documents = []
chunk_metadatas = []

for index, match in enumerate(matches):
    section = match.group(1)

    start = match.end()
    end = (
        matches[index + 1].start()
        if index + 1 < len(matches)
        else len(text)
    )

    section_text = text[start:end].strip()
    chunks = text_splitter.split_text(section_text)

    for chunk in chunks:
        chunk_ids.append(f"{section.lower().replace(' ', '_')}_{len(chunk_ids)}")
        chunk_documents.append(chunk)
        chunk_metadatas.append({
            "source": document_path.name,
            "section": section
        })


# Replace the existing collection contents with the newly ingested chunks
if collection.count() > 0:
    existing_ids = collection.get()["ids"]
    collection.delete(ids=existing_ids)

if chunk_ids:
    collection.add(
        ids=chunk_ids,
        documents=chunk_documents,
        metadatas=chunk_metadatas
    )

print(f"Stored {len(chunk_ids)} chunks successfully!")

for section in dict.fromkeys(
    metadata["section"] for metadata in chunk_metadatas
):
    print(f"- {section}")
