from fastapi import FastAPI
from app.schemas.question import Question
from app.routers import conversation

app = FastAPI(
    title="Knowledge Assistant API",
    description="Our First AI Backend",
    version='1.0.0'
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
    return{
        "status": "Healthy",
        "server": "Running",
        "database": "Not Connected Yet"
    }

@app.get("/users/{id}")
def get_user(id:int):
    return{
        "user_id":id,
        "message":f"User {id} returned successfully"
    }

@app.post("/ask")
def ask(question: Question):

        if question.question.lower()=="what is fastapi":
             answer="FastApi is a modern Python framework for calling endpoints"
        elif question.question.lower()=="what is laravel":
             answer="laravel is a modern php backend framework"
        elif question.question.lower()=="hello":
             answer="Hello Captain Morgan"
        else:
             answer="I dont Know the answer for this bruhh"
        return{"answer":answer}

@app.get("/search")
def search(q: str, limit:int):
    return {
        "search_term": q,
        "limit":limit
    }