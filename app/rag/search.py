
import chromadb
import re

from rank_bm25 import BM25Okapi
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from app.rag.query_expansion import expand_query


# 1. Connect to ChromaDB

client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_collection(
    name="morgan_personal",
    embedding_function=embedding_function
)


# 2. Load all knowledge chunks and their unique IDs

stored_data = collection.get(
    include=["documents", "metadatas"]
)

documents = stored_data["documents"]
metadatas = stored_data["metadatas"]
document_ids = stored_data["ids"]

id_to_index = {
    document_id: index
    for index, document_id in enumerate(document_ids)
}


# 3. Prepare BM25

def tokenize(text: str):
    return re.findall(r"\b\w+\b", text.lower())


tokenized_documents = [
    tokenize(document)
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)


# 4. Hybrid search

def search_documents(question: str, n_results: int = 5):

    candidate_count = min(n_results * 3, len(documents))

    # Expand the original question
    expanded_terms = expand_query(question)

    # Semantic search uses the original question
    semantic_results = collection.query(
        query_texts=[question],
        n_results=candidate_count,
        include=["distances"]
    )

    semantic_ids = semantic_results["ids"][0]

    # BM25 searches using original and expanded terms
    search_text = " ".join(expanded_terms)
    query_tokens = tokenize(search_text)

    bm25_scores = bm25.get_scores(query_tokens)

    keyword_indices = [
        index
        for index in range(len(bm25_scores))
        if bm25_scores[index] > 0
    ]

    keyword_indices.sort(
        key=lambda index: bm25_scores[index],
        reverse=True
    )

    keyword_indices = keyword_indices[:candidate_count]


    # 5. Weighted Reciprocal Rank Fusion

    combined_scores = {}

    BM25_WEIGHT = 0.7
    SEMANTIC_WEIGHT = 0.3
    RRF_CONSTANT = 60

    # Add semantic rankings
    for rank, document_id in enumerate(semantic_ids, start=1):

        index = id_to_index.get(document_id)

        if index is not None:
            combined_scores[index] = (
                combined_scores.get(index, 0)
                + SEMANTIC_WEIGHT / (RRF_CONSTANT + rank)
            )

    # Add BM25 rankings
    for rank, index in enumerate(keyword_indices, start=1):

        combined_scores[index] = (
            combined_scores.get(index, 0)
            + BM25_WEIGHT / (RRF_CONSTANT + rank)
        )

    # Sort combined results
    ranked_indices = sorted(
        combined_scores,
        key=lambda index: combined_scores[index],
        reverse=True
    )[:n_results]
    return [
        {
            "document": documents[index],
            "distance": None,
            "source": metadatas[index].get("source", "Unknown"),
            "section": metadatas[index].get("section", "Unknown"),
            "hybrid_score": combined_scores[index]
        }
        for index in ranked_indices
    ]

# 6. BM25-only search for comparison

def search_documents_bm25(question: str, n_results: int = 5):

    expanded_terms = expand_query(question)

    search_text = " ".join(expanded_terms)

    query_tokens = tokenize(search_text)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )

    # Keep only documents with actual keyword matches.
    ranked_indices = [
        index
        for index in ranked_indices
        if scores[index] > 0
    ][:n_results]

    return [
        {
            "document": documents[index],
            "distance": None,
            "source": metadatas[index].get("source", "Unknown"),
            "section": metadatas[index].get("section", "Unknown"),
            "hybrid_score": float(scores[index])
        }
        for index in ranked_indices
    ]
