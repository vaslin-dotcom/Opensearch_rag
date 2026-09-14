# core/opensearch_client.py
from opensearchpy import OpenSearch
import os

def get_opensearch_client():
    return OpenSearch(
        hosts=[{'host': os.getenv('OPENSEARCH_HOST', 'localhost'),
                'port': int(os.getenv('OPENSEARCH_PORT', 9200))}],
        use_ssl=False, verify_certs=False, http_compress=True
    )