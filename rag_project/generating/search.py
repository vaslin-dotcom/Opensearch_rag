from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer 

def search(client:OpenSearch,query,k=5,INDEX='rag_poc_index',pipeline_id='rag_hybrid_pipeline'): 
    model=SentenceTransformer('all-MiniLM-L6-v2')
    query_vector=model.encode(query).tolist()
    search_body={
        'size':k,
        'query':{
            'hybrid':{
                'queries':[
                    {
                        'match':{
                        "chunk_text":query
                        }
                    },
                    {
                        'knn':{
                            "chunk_embedding":{
                                "vector":query_vector,
                                "k":k
                            }
                        }
                    }
                ]
            }
        }
    }

    response=client.search(
        index=INDEX,
        body=search_body,
        params={'search_pipeline':pipeline_id}
    )

    return response['hits']['hits']

