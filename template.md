# OpenSearch Reusable Templates

## 1. Create an index (fill in your own field names)
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "<your_text_field>": { "type": "text" },
      "<your_metadata_field>": { "type": "keyword" },
      "<your_vector_field>": {
        "type": "knn_vector",
        "dimension": <match_your_embedding_model>,
        "method": {
          "name": "hnsw",
          "space_type": "cosinesimil",
          "engine": "faiss"
        }
      }
    }
  }
}
# Change: field names, dimension (must match your embedding model's output size)

## 2. Insert one document (Python)
client.index(
    index="<index_name>",
    id=<some_id>,
    body={
        "<your_text_field>": "...",
        "<your_metadata_field>": "...",
        "<your_vector_field>": [ ... ]
    }
)
# Use this for single/occasional inserts. For many docs, use bulk (below) — much faster.

## 3. Bulk insert many documents (Python)
actions = [
    {
        "_index": "<index_name>",
        "_id": i,
        "_source": { ... your fields ... }
    }
    for i, item in enumerate(your_data)
]
helpers.bulk(client, actions)
# _index/_id/_source are OpenSearch's fixed metadata keys — don't rename these.
# Everything inside _source is your own custom field names.

## 4. Create a search pipeline (Python, one-time setup — needed before hybrid search works)
pipeline_body = {
    "description": "<describe what this pipeline does>",
    "phase_results_processors": [
        {
            "score-ranker-processor": {
                "combination": {
                    "technique": "rrf",
                    "rank_constant": 60
                }
            }
        }
    ]
}

client.transport.perform_request(
    method="PUT",
    url="/_search/pipeline/<pipeline_name>",
    body=pipeline_body
)
# "technique": "rrf" = rank-based fusion (recommended default).
# Alternative: "technique": "min_max" style normalization + weighted average (needs different processor — see notes below).
# rank_constant: higher = softer effect of top ranks. 60 is OpenSearch's common default.
# Run this ONCE per pipeline name. If you change settings, you must re-PUT it (overwrites).

## 5. Hybrid search query (fill in query text + vector)
{
  "size": <k>,
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "<your_text_field>": "<query_string>" } },
        { "knn": { "<your_vector_field>": { "vector": [...], "k": <k> } } }
      ]
    }
  }
}
# Must be run with params={"search_pipeline": "<pipeline_name>"} in Python,
# or ?search_pipeline=<pipeline_name> in curl — otherwise hybrid scoring won't combine correctly.