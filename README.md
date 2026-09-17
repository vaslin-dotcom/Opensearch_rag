# OpenSearch RAG

A Dockerized Retrieval-Augmented Generation (RAG) proof of concept. PDF files are split into chunks, embedded with `all-MiniLM-L6-v2`, and stored in OpenSearch. Questions use hybrid BM25 + kNN retrieval with reciprocal rank fusion (RRF), then the generation service uses the retrieved context to produce an answer through Groq.

## Architecture

```text
PDF files in ./data
        |
        v
indexing service :8001  --->  OpenSearch :9200  <---  generating service :8002
        |                         (text + vectors)             |
        +-- create index/pipeline, index PDFs       search chunks or generate answers
```

## Requirements

- Docker and Docker Compose
- A Groq API key for `/generate_answer`

## Run With Docker Compose

From the repository root:

```bash
cd rag_project
export GROQ_API_KEY="your-groq-api-key"
docker compose up --build
```

The services are available at:

| Service | URL | Purpose |
|---|---|---|
| OpenSearch | `http://localhost:9200` | Search and vector storage |
| Indexing API | `http://localhost:8001/docs` | Create indexes and ingest PDFs |
| Generating API | `http://localhost:8002/docs` | Search and answer questions |

`depends_on` starts OpenSearch before the application containers but does not wait for OpenSearch to become ready. Wait for `http://localhost:9200` to respond before calling the application APIs.

## Index Documents

Put PDF files in `rag_project/data/` for the Compose file as currently written. The repository also contains a top-level `data/` directory; to use that directory, change the volume in `rag_project/docker-compose.yml` from `./data:/data` to `../data:/data`.

Create the index and the RRF search pipeline once:

```bash
curl -X POST "http://localhost:8001/create_index"
curl -X POST "http://localhost:8001/create_rrf_pipeline"
```

Index all PDFs in `/data`:

```bash
curl -X POST "http://localhost:8001/index_pdf"
```

Optional query parameters are `chunk_size` (default `1000`), `overlap` (default `100`), `index_name` (default `rag_poc_index`), and `target_path` (default `/data`). Indexed filenames are recorded beside the PDFs as `.indexed_files.json`, so subsequent calls skip files already processed.

## Query Documents

Search for matching chunks:

```bash
curl --get "http://localhost:8002/search_chunks" \
  --data-urlencode "query=What is this document about?"
```

Generate an answer grounded in the retrieved chunks:

```bash
curl --get "http://localhost:8002/generate_answer" \
  --data-urlencode "query=What is this document about?"
```

The generation endpoint requires `GROQ_API_KEY` and uses the Groq OpenAI-compatible API. Search defaults are `k=5`, index `rag_poc_index`, and pipeline `rag_hybrid_pipeline`. The index and pipeline can be overridden with the `INDEX` and `pipeline_id` query parameters where supported.

## Project Structure

```text
.
├── data/                         # Repository-level data directory
├── README.md
├── scripts.md                    # Useful standalone Docker commands
└── rag_project/
    ├── docker-compose.yml        # OpenSearch and both FastAPI services
    ├── indexing/
    │   ├── app.py                # Indexing API
    │   ├── create_index.py       # OpenSearch knn_vector mapping
    │   ├── create_hybrid_pipeline.py
    │   ├── deleting_index.py
    │   ├── index_pdf.py          # PDF parsing, chunking, embedding, bulk indexing
    │   ├── opensearch_client.py
    │   ├── requirements.txt
    │   └── Dockerfile
    └── generating/
        ├── app.py                # Search and answer API
        ├── search.py             # Hybrid BM25 + kNN retrieval
        ├── generate_answer.py    # Groq-backed answer generation
        ├── opensearch_client.py
        ├── requirements.txt
        └── Dockerfile
```

## Data Model

The default index is `rag_poc_index`. Each indexed chunk contains:

- `chunk_text`: extracted PDF text
- `source_file`: original PDF filename
- `page_no`: source page number
- `chunk_embedding`: a 384-dimensional `all-MiniLM-L6-v2` vector

To remove the default index:

```bash
curl -X DELETE "http://localhost:8001/delete_index"
```

Stop the stack with `docker compose down`. Add `-v` only when you also want to remove the OpenSearch volume and all indexed data.
