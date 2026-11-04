
from app.rag.search import search_documents
from app.rag.llm import generate_answer

MAX_DISTANCE = 0.5


def ask_question(question: str):
    results = search_documents(question)

    relevant_results = [
        result
        for result in results
        if result["distance"] <= MAX_DISTANCE
    ]

    if not relevant_results:
        return {
            "question": question,
            "answer": (
                "I don't have enough information in the "
                "knowledge base to answer that question."
            ),
            "sources": []
        }

    documents = [
        result["document"]
        for result in relevant_results
    ]

    context = "\n\n".join(documents)

    answer = generate_answer(question, context)

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
