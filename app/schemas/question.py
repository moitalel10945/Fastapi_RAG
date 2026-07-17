from pydantic import BaseModel
class Question(BaseModel):
    question:str

class ConversationCreate(BaseModel):
    question: str