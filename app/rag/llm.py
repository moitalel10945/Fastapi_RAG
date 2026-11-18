
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma3:1b"


def generate_answer(question: str, context: str):

    prompt = f"""
You are Morgan's personal AI knowledge assistant.

Your job is to answer questions about Morgan using only
the information in the provided knowledge base context.

IMPORTANT RULES:

1. Answer using only information explicitly supported
   by the supplied context.

2. Answer the user's actual question directly.

3. Identify the exact category, attribute or relationship
   requested in the question.

4. Match the requested information to the correct record
   in the context.

5. Treat each person, school, project, technology,
   achievement and experience as a separate record.
   Do not interchange their attributes or details.

6. Respect explicit labels and descriptions in the context.
   For example:
   - SECONDARY SCHOOL EDUCATION means high school.
   - PRIMARY SCHOOL EDUCATION means primary school.
   - Do not confuse the two education levels.

7. When multiple related records appear, identify which
   record directly answers the question. Do not select
   another record simply because it contains related words.

8. Use relevant facts from the context even when the
   question uses different wording.

9. Do not invent, assume, guess or infer personal details.

10. Do not confuse related information with confirmed facts.

11. If the requested information is genuinely missing
    from the context, respond exactly:
    "I don't have enough information in the knowledge base to answer that question."

12. Use simple, natural and professional English.

13. Do not include unrelated information.

14. If the context contains conflicting information,
    do not silently choose one version. Explain that
    the information is conflicting.

CONTEXT:
{context}

QUESTION:
{question}

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
                    "temperature": 0,
                    "top_p": 0.8,
                    "num_predict": 200
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
