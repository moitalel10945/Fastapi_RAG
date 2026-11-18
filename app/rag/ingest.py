
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
    name="morgan_personal",
    embedding_function=embedding_function
)


# Load your personal knowledge document
document_path = Path("documents/morgan_personal.md")
text = document_path.read_text(encoding="utf-8")


# Identify Markdown headings
section_pattern = re.compile(
    r"(?m)^#{1,3}\s+(.+?)\s*$"
)

matches = list(section_pattern.finditer(text))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunk_ids = []
chunk_documents = []
chunk_metadatas = []

# Process each section
for index, match in enumerate(matches):
    section = match.group(1).strip()

    start = match.end()
    end = (
        matches[index + 1].start()
        if index + 1 < len(matches)
        else len(text)
    )

    section_text = text[start:end].strip()

    # Keep the section heading with its content
    section_content = f"{section}\n{section_text}"

    chunks = text_splitter.split_text(section_content)

    for chunk_index, chunk in enumerate(chunks):
        chunk_ids.append(
            f"personal_{index}_{chunk_index}"
        )

        chunk_documents.append(chunk)

        chunk_metadatas.append({
            "source": document_path.name,
            "section": section
        })


# Replace previously ingested personal information
if collection.count() > 0:
    existing_ids = collection.get()["ids"]
    collection.delete(ids=existing_ids)


# Store the new chunks
if chunk_ids:
    collection.add(
        ids=chunk_ids,
        documents=chunk_documents,
        metadatas=chunk_metadatas
    )

print(f"Stored {len(chunk_ids)} personal knowledge chunks!")

for section in dict.fromkeys(
    metadata["section"] for metadata in chunk_metadatas
):
    print(f"- {section}")
