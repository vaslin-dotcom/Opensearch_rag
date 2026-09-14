OpenSearch RAG — Microservices with FastAPI

A Retrieval-Augmented Generation (RAG) system built on OpenSearch, exposed as a set of FastAPI microservices for document indexing and question answering.

PDF documents are chunked, embedded, and indexed into OpenSearch with hybrid search (BM25 + kNN, combined via an RRF pipeline). Queries are answered by retrieving the most relevant chunks and passing them to an LLM for grounded answer generation.

Overview

This project demonstrates an end-to-end RAG pipeline built directly on top of OpenSearch as the vector + text search engine, with the retrieval and generation logic split into independent, composable FastAPI services rather than a single monolithic script.

Core capabilities:

Ingest PDFs and index them into OpenSearch as chunked, embedded documents
Hybrid search combining lexical (BM25) and semantic (kNN) retrieval, fused with an RRF search pipeline
Question answering via retrieval + LLM generation (Groq-hosted model)
Clean service boundaries: indexing and querying are separate FastAPI routers, each with their own scripts
Architecture
                     ┌──────────────────────┐
                     │      FastAPI App      │
                     └──────────┬───────────┘
                                │
                ┌───────────────┴───────────────┐
                │                                │
       ┌────────▼────────┐             ┌─────────▼─────────┐
       │  Indexing Router │             │  Querying Router   │
       │   /index/...     │             │   /query/...       │
       └────────┬────────┘             └─────────┬─────────┘
                │                                │
       ┌────────▼────────┐             ┌─────────▼─────────┐
       │  index_pdf.py    │             │  search.py          │
       │  (chunk + embed  │             │  generate_answer.py │
       │   + bulk index)  │             │  (hybrid retrieval  │
       │                  │             │   + LLM generation) │
       └────────┬────────┘             └─────────┬─────────┘
                │                                │
                └───────────────┬───────────────┘
                                │
                       ┌────────▼────────┐
                       │   OpenSearch     │
                       │  (knn_vector +   │
                       │  RRF pipeline)   │
                       └──────────────────┘
Stack
Layer	Technology
API framework	FastAPI
Search / vector store	OpenSearch (knn_vector, hybrid RRF search pipeline)
Embeddings	sentence-transformers — all-MiniLM-L6-v2 (384-dim)
LLM generation	Groq-hosted model via langchain_openai.ChatOpenAI
PDF parsing	pypdf
Project Structure
rag_project/app/
├── main.py                     # FastAPI app entrypoint
├── opensearch_client.py        # shared OpenSearch client (injected via Depends())
├── routers/
│   ├── indexing.py             # indexing microservice endpoints
│   └── querying.py             # search / QA microservice endpoints
└── scripts/
    ├── create_index.py         # creates the OpenSearch index with knn_vector mapping
    ├── create_hybrid_pipeline.py  # sets up the RRF hybrid search pipeline
    ├── deleting_index.py       # index cleanup utility
    ├── index_pdf.py            # PDF chunking, embedding, and bulk indexing
    ├── search.py                # hybrid retrieval logic
    └── generate_answer.py       # retrieval + LLM answer generation
Setup
Have an OpenSearch instance running and reachable (default: localhost:9200).
Install dependencies:
bash
   pip install fastapi uvicorn opensearch-py sentence-transformers pypdf langchain-openai
Create the index and hybrid search pipeline:
bash
   python scripts/create_index.py
   python scripts/create_hybrid_pipeline.py
Run the app:
bash
   uvicorn main:app --reload
Open /docs for the interactive Swagger UI.
API
POST /index/index_pdf

Chunks a PDF (or a folder of PDFs), embeds each chunk, and bulk-indexes into OpenSearch. Tracks already-indexed files so re-runs only pick up new documents.

Params: index_name, chunk_size, overlap

POST /query/search

Runs hybrid search (BM25 + kNN, fused via RRF) against an index and returns the matching chunks.

Body: question, top_k, index_name

POST /query/ask

Retrieves relevant chunks and generates a grounded answer using the LLM.

Body: question, top_k, index_name

Design Notes
Microservice split by concern: indexing and querying live in separate routers and scripts, so each piece — chunking/embedding, hybrid retrieval, and generation — can be developed, tested, and scaled independently.
Dependency injection for shared resources: the OpenSearch client is created once and injected into routes via FastAPI's Depends(), rather than instantiated per-request.
Hybrid search over pure vector search: combining BM25 with kNN via an RRF pipeline gives better retrieval quality than either lexical or semantic search alone, especially for exact-term matches (names, codes, etc.) that pure embeddings can miss.
Roadmap
 Add automated tests for router and retrieval logic
 Add support for other document formats beyond PDF
 Add reranking step before answer generation
 Containerize with Docker Compose (app + OpenSearch)
