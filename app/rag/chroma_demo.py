from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Embedding model
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collection
collection = client.get_or_create_collection(
    name="property_manual",
    embedding_function=embedding_function
)
    

# Read document
document_path = Path("documents/tenant_manual.txt")
text = document_path.read_text()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

# Store chunks
for index, chunk in enumerate(chunks):

    collection.add(
        ids=[str(index)],
        documents=[chunk]
    )

print(f"Stored {len(chunks)} chunks successfully!")