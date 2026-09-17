
from pypdf import PdfReader as reader
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch, helpers
import os
import json


def index_pdf(client: OpenSearch, chunk_size = 1000,
    overlap = 100,
    index_name = "rag_poc_index",
    target_path = '/workspaces/Opensearch_rag/data'):
    

    def load_indexed_files(tracker_file):
        if os.path.exists(tracker_file):
            with open(tracker_file, 'r') as f:
                return set(json.load(f))
        return set()


    def save_indexed_files(tracker_file, indexed_set):
        with open(tracker_file, 'w') as f:
            json.dump(list(indexed_set), f)


    def chunk_text(text: str, size: int, overlap: int) -> list:
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks


    

    # Support pointing at either a single PDF file or a whole folder of them.
    if os.path.isdir(target_path):
        folder = target_path
        pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    else:
        folder = os.path.dirname(target_path) or "."
        pdf_files = [os.path.basename(target_path)]

    tracker_file = os.path.join(folder, '.indexed_files.json')
    already_indexed = load_indexed_files(tracker_file)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    actions = []
    id_counter = 0
    newly_indexed = []

    for file in pdf_files:
        if file in already_indexed:
            print(f"Skipping already-indexed file: {file}")
            continue

        print(f"Indexing new file: {file}")
        file_path = os.path.join(folder, file)
        read = reader(file_path)

        for page_no, page in enumerate(read.pages, start=1):
            page_text = page.extract_text() or ""
            chunks = chunk_text(page_text, chunk_size, overlap)

            for chunk in chunks:
                embedding = model.encode(chunk).tolist()
                actions.append({
                    '_index': index_name,
                    '_id': f"{file}_{id_counter}",
                    '_source': {
                        'chunk_text': chunk,
                        'source_file': file,
                        'chunk_embedding': embedding,
                        'page_no': page_no
                    }
                })
                id_counter += 1

        newly_indexed.append(file)

    if actions:
        success, error = helpers.bulk(client, actions)
        already_indexed.update(newly_indexed)
        save_indexed_files(tracker_file, already_indexed)
        return f"Succeeded: {success}, failed: {error}"
    else:
        return "No new files to index."


