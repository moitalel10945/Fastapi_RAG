# from fastapi import FastAPI
import requests
from app.schemas.question import Question, AnswerResponse
from app.routers import conversation
from app.rag.rag_service import ask_question
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Knowledge Assistant API",
    description="Our First AI Backend",
    version='1.0.0'
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    conversation.router,
    prefix="/conversations",
    tags=["Conversations"]
)

@app.get("/")
def home():
    return{
        "message":"Welcome To fastapi framework"
    }

@app.get("/about")
def about():
    return{
        "message":"Hello FastApi",
        "version":"1.00",
        "developer":"Captain Morgan"
    }


@app.get("/health")
def health():
    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )
        response.raise_for_status()

        ai_status = "Connected"

    except requests.exceptions.RequestException:
        ai_status = "Unavailable"

    return {
        "status": "Healthy" if ai_status == "Connected" else "Degraded",
        "api": "Running",
        "ai_service": "Ollama",
        "ai_status": ai_status,
        "ai_model": "gemma3:1b"
    }



@app.get("/users/{id}")
def get_user(id:int):
    return{
        "user_id":id,
        "message":f"User {id} returned successfully"
    }

@app.post("/ask", response_model=AnswerResponse)
def ask(question: Question):
    try:
        return ask_question(question.question)

    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your question."
        )
    
@app.get("/search")
def search(q: str, limit:int):
    return {
        "search_term": q,
        "limit":limit
    }