
from fastapi import APIRouter, Depends
from scripts.create_index import create_index
from scripts.create_hybrid_pipeline import create_hybrid_pipeline
from scripts.index_pdf import index_pdf
from scripts.deleting_index import delete_index
from opensearch_client import get_opensearch_client

router = APIRouter()
@router.post("/create")
def create_index_endpoint(index_name: str, client=Depends(get_opensearch_client)):
    return create_index(client, index_name)

@router.post("/pipeline")
def create_pipeline_endpoint(client=Depends(get_opensearch_client),pipeline_id='rag_hybrid_pipeline'):
    return create_hybrid_pipeline(client, pipeline_id=pipeline_id)

@router.post("/index_pdf")
def index_pdf_endpoint(client=Depends(get_opensearch_client),index_name: str='rag_poc_index', chunk_size: int = 500, overlap: int = 50):
    return index_pdf(
    client,
    chunk_size=chunk_size,
    overlap=overlap,
    index_name=index_name,
)

@router.delete("/{index_name}")
def delete_index_endpoint(index_name: str, client=Depends(get_opensearch_client)):
    return delete_index(client, index_name)