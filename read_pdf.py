from pypdf import PdfReader as reader

harry_potter_reader=reader("/workspaces/Opensearch_rag/data/harrypotter.pdf")
got_reader=reader('/workspaces/Opensearch_rag/data/GOT.pdf')

#print(f"Total pages={len(harry_potter_reader.pages)+len(got_reader.pages)}")
print(got_reader.pages[15].extract_text())