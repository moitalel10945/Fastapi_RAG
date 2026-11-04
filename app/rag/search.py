
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("property_manual")


def search_documents(question: str, n_results: int = 3):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    return [
        {
            "document": document,
            "distance": distance,
            "source": metadata["source"],
            "section": metadata["section"]
        }
        for document, distance, metadata
        in zip(documents, distances, metadatas)
    ]
