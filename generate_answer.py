from search import hybrid_search
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",   # a solid free Groq model
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"   # this is the key part — redirect to Groq
)

def generate(query,retrieved_chunks):
    context = "\n\n".join(
        f"[Source: {c['_source']['source_file']}]\n{c['_source']['chunk_text']}"
        for c in retrieved_chunks
    )

    prompt = f"""Answer the question using ONLY the context below. If the answer isn't in the context, say you don't know.

    Context:
    {context}

    Question: {query}

    Always give the citation from where you got this output"""

    response = llm.invoke(prompt)
    return response.content

if __name__ == '__main__':
    query = input("Enter your query: ")
    chunks = hybrid_search(query)
    answer = generate(query, chunks)

    print("\n--- Generated Answer ---")
    print(answer)