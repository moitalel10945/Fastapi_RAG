from xxlimited import new

# from pydantic import BaseModel


from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question cannot be empty or spaces.")
        return value


class ConversationCreate(BaseModel):
    question: str


# class AnswerResponse(BaseModel):
#     question: str
#     answer: str
#     sources: list[str]

# new additions

class Source(BaseModel):
    document: str
    section: str


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
