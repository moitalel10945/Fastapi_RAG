from app.database.database import Base, engine
from app.models.conversation import Conversation

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")