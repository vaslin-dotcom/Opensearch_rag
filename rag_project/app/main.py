from fastapi import FastAPI
from routers import indexing, querying

app = FastAPI(title="OpenSearch RAG API")
app.include_router(indexing.router, prefix="/index", tags=["indexing"])
app.include_router(querying.router, prefix="/query", tags=["query"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to the OpenSearch RAG API"}