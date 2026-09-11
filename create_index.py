from opensearchpy import OpenSearch

client=OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False
)

index_name='rag_poc_index'

index_body={
    'settings':{
        'index.knn':True
    },
    'mappings':{
        "properties":{
            "chunk_text":{"type":"text"},
            "source_file":{"type":"keyword"},
            "chunk_embedding":{
                "type":"knn_vector",
                "dimension":384,
                "method":{
                    "name":"hnsw",
                    "space_type":"cosinesimil",
                    "engine":"faiss"
                }
            }
        }
    }

}

response=client.indices.create(index=index_name,body=index_body)
print(response)