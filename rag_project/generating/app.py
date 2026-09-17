from fastapi import FastAPI,Depends
from generating.opensearch_client import get_opensearch_client
from generating.search import search
from generating.generate_answer import generate_answer

app=FastAPI(title='Generating')

@app.get("/")
def root():
    return {"message": "Welcome to the Generate Answer Service"}

@app.get('/search_chunks')
def search_endpoint(query,client=Depends(get_opensearch_client),k=5,INDEX='rag_poc_index',pipeline_id='rag_hybrid_pipeline'):
    return search(client,query,k,INDEX,pipeline_id)

@app.get('/generate_answer')
def generate_answer_endpoint(query:str,client=Depends(get_opensearch_client),INDEX="rag_poc_index"):
    return generate_answer( client, query, INDEX)
