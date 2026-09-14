from opensearchpy import OpenSearch

def create_hybrid_pipeline(client: OpenSearch, pipeline_id='rag_hybrid_pipeline'):
    pipeline_body={
        'description':'RRF hybrid pipeline',
        'phase_results_processors':[
            {
                "score-ranker-processor":{
                    "combination":{
                        "technique":"rrf",
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

    return response