from pypdf import PdfReader as reader
from sentence_transformers import SentenceTransformer 
from opensearchpy import OpenSearch,helpers
import os 

PATH='/workspaces/Opensearch_rag/data'
chunk_size=1000
overlap=100
index_name="rag_poc_index"

def chunk_text(text:str,size:int,overlap:int)->list:
    chunks=[]
    start=0
    while start<len(text):
        end=start+size
        chunks.append(text[start:end])
        start=end-overlap
    return chunks

model=SentenceTransformer("all-MiniLM-L6-v2")
client=OpenSearch(
    hosts=[{'host':'localhost','port':9200}],
    verify_certs=False,
    use_ssl=False,
    http_compress=True
)

#client.indices.delete(index="rag_poc_index")

actions=[]
id_counter=0

for file in os.listdir(PATH):
    if not file.endswith('.pdf'):
        continue
    file_path=os.path.join(PATH,file)
    read=reader(file_path)

    file_text=''
    for page in read.pages:
        file_text+=page.extract_text()+'\n'
        chunks=chunk_text(file_text,chunk_size,overlap)

    for chunk in chunks:
        embedding=model.encode(chunk).tolist()
        actions.append(
            {
                '_index':index_name,
                '_id':id_counter,
                '_source':{
                    'chunk_text':chunk,
                    'source_file':file,
                    'chunk_embedding':embedding,
                }   
            }
        )
        id_counter+=1

success,error=helpers.bulk(client,actions)
print(f"Succeeded:{success}, failed:{error}")