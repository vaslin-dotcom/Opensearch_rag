from fastapi import FastAPI,Depends
from indexing.opensearch_client import get_opensearch_client
from indexing.create_index import create_index
from indexing.create_hybrid_pipeline import create_hybrid_pipeline
from indexing.index_pdf import index_pdf
from indexing.deleting_index import delete_index

app=FastAPI(title='Indexing')

@app.get("/")
def root():
    return {"message": "Welcome to the Index service"}

@app.post('/create_index')
def create_index_endpoint(client=Depends(get_opensearch_client), index_name: str = 'rag_poc_index'):
    return create_index(client, index_name)

@app.post('/create_rrf_pipeline')
def create_pipeline_endpoint(client=Depends(get_opensearch_client), pipeline_id='rag_hybrid_pipeline'):
    return create_hybrid_pipeline(client, pipeline_id)

@app.post('/index_pdf')
def create_index_endpoint(client=Depends(get_opensearch_client), chunk_size:int = 1000,
    overlap:int = 100,
    index_name: str = "rag_poc_index",
    target_path: str = '/data'):
    return index_pdf(client,chunk_size,overlap,index_name,target_path )

@app.delete('/delete_index')
def delete_index_endpoint(client=Depends(get_opensearch_client), index_name='rag_poc_index'):
    return delete_index(client, index_name)
