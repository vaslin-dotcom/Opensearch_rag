
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from scripts.search import search
from scripts.generate_answer import generate_answer
from opensearch_client import get_opensearch_client


router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    index_name:str='rag_poc_index'

@router.post("/search")
def search_endpoint(req: QueryRequest, client=Depends(get_opensearch_client)):
    return search(client, req.question, k=req.top_k, INDEX=req.index_name)

@router.post("/ask")
def ask_endpoint(req: QueryRequest, client=Depends(get_opensearch_client)):
    return generate_answer(client, req.question, INDEX=req.index_name)