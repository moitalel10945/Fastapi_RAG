
from app.rag.search import search_documents_bm25
from app.rag.llm import generate_answer


MIN_BM25_SCORE = 1.0


def ask_question(question: str):

    # 1. Retrieve relevant documents using BM25
    results = search_documents_bm25(question, n_results=5)

    # 2. Filter out weak keyword matches
    relevant_results = [
        result
        for result in results
        if result["hybrid_score"] >= MIN_BM25_SCORE
    ]

    # 3. Handle questions with no relevant information
    if not relevant_results:
        return {
            "question": question,
            "answer": (
                "I don't have enough information in the "
                "knowledge base to answer that question."
            ),
            "sources": []
        }

    # 4. Prepare context for the LLM
    documents = [
        result["document"]
        for result in relevant_results
    ]

    context = "\n\n".join(documents)

    # 5. Generate an answer
    answer = generate_answer(question, context)

    # 6. Collect unique sources
    sources = []
    seen_sources = set()

    for result in relevant_results:

        source_key = (
            result["source"],
            result["section"]
        )

        if source_key not in seen_sources:
            sources.append({
                "document": result["source"],
                "section": result["section"]
            })

            seen_sources.add(source_key)

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
