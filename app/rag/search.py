import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Get the existing collection
collection = client.get_collection("property_manual")

# Ask a question
question = "How can I add a tenant?"

# Convert question into an embedding
query_embedding = model.encode(question).tolist()

# Search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print("\nQuestion:")
print(question)

print("\nMost relevant chunks:\n")

for document in results["documents"][0]:
    print("=" * 60)
    print(document)