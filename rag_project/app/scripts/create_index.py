from opensearchpy import OpenSearch

def create_index(client: OpenSearch, index_name: str = 'rag_poc_index'):



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

    response = client.indices.create(index=index_name, body=index_body)
    return(response)

