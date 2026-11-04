
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma3:1b"


def generate_answer(question: str, context: str):

    prompt = f"""
You are a reliable property management assistant.

Your job is to answer questions using the provided documentation.

STRICT RULES:

1. Use ONLY the information provided in the context.
2. Do not invent, assume, or add instructions.
3. Preserve the original meaning of every instruction.
4. Do not replace words with different actions.
5. When explaining a procedure, preserve the original step order.
6. Use simple, clear and professional English.
7. Use numbered lists for procedures.
8. If the context does not contain the answer, say:
   "I don't have enough information in the knowledge base to answer that question."
9. Do not include unrelated information.
10. Do not make up additional steps.

DOCUMENTATION:
{context}

USER QUESTION:
{question}

INSTRUCTIONS FOR YOUR RESPONSE:

Answer the user's question directly.

If the documentation contains a procedure, reproduce its steps
accurately and in their original order.

Do not change the meaning of any step.

ANSWER:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "num_predict": 300
                }
            },
            timeout=120
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise RuntimeError("AI service is currently unavailable.")

    except requests.exceptions.Timeout:
        raise RuntimeError("AI service took too long to respond.")

    return response.json()["response"].strip()