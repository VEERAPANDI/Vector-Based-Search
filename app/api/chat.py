from fastapi import APIRouter
from pydantic import BaseModel
from app.vector.search import vector_search

router = APIRouter()

class Query(BaseModel):
    question: str

@router.post("/search")
def search(req: Query):
    result = vector_search(req.question)
    return result
