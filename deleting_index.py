from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    verify_certs=False,
    use_ssl=False,
    http_compress=True
)

client.indices.delete(index="rag_poc_index")
print("Deleted")