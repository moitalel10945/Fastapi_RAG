import chromadb
import requests

# Connect to Chroma
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("property_manual")

# User's question
question = "How can I add a tenant?"

# Search Chroma
results = collection.query(
    query_texts=[question],
    n_results=3
)

# Get the retrieved chunks
chunks = results["documents"][0]

context = "\n\n".join(chunks)

# Build the prompt
prompt = f"""
You are a property management assistant.

Answer the user's question using only the information provided
in the context below.

Context:
{context}

Question:
{question}

Answer clearly and professionally.
"""

# Ask Ollama
response = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }
)

# Get Gemma's answer
answer = response.json()["response"]

print("\nQuestion:")
print(question)

print("\nRetrieved Context:")
print(context)

print("\nAnswer:")
print(answer)