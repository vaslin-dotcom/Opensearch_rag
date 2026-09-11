from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer 

model=SentenceTransformer('all-MiniLM-L6-v2')
INDEX='rag_poc_index'

client=OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False
)

def hybrid_search(query,k=5):
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
        params={'search_pipeline':'rag_hybrid_pipeline'}
    )

    return response['hits']['hits']

if __name__=='__main__':
    query=input('Enter your query:')
    results=hybrid_search(query)
    for r in results:
        print(f"\nScore: {r['_score']}")
        print(f"Source: {r['_source']['source_file']} (page {r['_source'].get('page_no')})")
        print(f"Text: {r['_source']['chunk_text']}")
    #print(result)