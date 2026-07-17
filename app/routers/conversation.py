from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.conversation import Conversation
from app.schemas.question import ConversationCreate

router = APIRouter()

@router.get("/")
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()

@router.get("/{id}")
def get_conversation(id:int,db:Session=Depends(get_db)):
    conversation = (
            db.query(Conversation)
            .filter(Conversation.id == id)
            .first()
        )
    if conversation is None:
            return {  
                "error": "Conversation not found" 
                }
    return conversation



@router.post("/")
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):

    new_conversation = Conversation(
        question=conversation.question
    )

    db.add(new_conversation)

    db.commit()

    db.refresh(new_conversation)

    return new_conversation

@router.put("/{id}")
def update_conversation(
    id: int,
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):

    db_conversation = (
        db.query(Conversation)
        .filter(Conversation.id == id)
        .first()
    )

    if db_conversation is None:
        return {
            "error": "Conversation not found"
        }

    db_conversation.question = conversation.question

    db.commit()

    db.refresh(db_conversation)

    return db_conversation


@router.delete("/{id}")
def delete_conversation(
    id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == id)
        .first()
    )

    if conversation is None:
        return {
            "error": "Conversation not found"
        }

    db.delete(conversation)

    db.commit()

    return {
        "message": f"Conversation {id} deleted successfully"
    }