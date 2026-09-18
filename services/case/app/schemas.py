from pydantic import BaseModel, Field


class CreateCaseRequest(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    summary: str = Field(min_length=10, max_length=5000)


class ApproveCaseRequest(BaseModel):
    note: str = Field(default="Approved", max_length=1000)
