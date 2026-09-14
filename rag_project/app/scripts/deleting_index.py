from opensearchpy import OpenSearch

def delete_index(client:OpenSearch, index_name='rag_poc_index'):
    client.indices.delete(index=index_name)
    print("Deleted")
    return 'deleted'