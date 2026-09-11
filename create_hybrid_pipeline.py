from opensearchpy import OpenSearch

client=OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    verify_certs=False,
    use_ssl=False,
    http_compress=True
)

pipeline_id='rag_hybrid_pipeline'

pipeline_body={
    'description':'RRF hybrid pipeline',
    'phase_results_processors':[
        {
            "score-ranker-processor":{
                "combination":{
                    "technic":"rrf",
                    "rank_constant":60
                }
            }
        }
    ]
}

response = client.transport.perform_request(
    method="PUT",
    url=f"/_search/pipeline/{pipeline_id}",
    body=pipeline_body
)

print(response)