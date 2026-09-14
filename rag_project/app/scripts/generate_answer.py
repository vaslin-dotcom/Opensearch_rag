from scripts.search import search
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch
load_dotenv()

def generate_answer( client:OpenSearch, query: str, INDEX="rag_poc_index"):

    llm = ChatOpenAI(
        model="openai/gpt-oss-120b",   # a solid free Groq model
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"   # this is the key part — redirect to Groq
    )

    def generate(query,retrieved_chunks):
        context = "\n\n".join(
            f"[Source: {c['_source']['source_file']}]\n{c['_source']['chunk_text']}\n{c['_source']['page_no']}"
            for c in retrieved_chunks
        )

        prompt = f"""Answer the question using ONLY the context below. If the answer isn't in the context, say you don't know.

        Context:
        {context}

        Question: {query}

        Always give the citation from where you got this output"""

        response = llm.invoke(prompt)
        return response.content

    chunks = search(client, query, INDEX=INDEX)
    answer = generate(query, chunks)

    return answer
