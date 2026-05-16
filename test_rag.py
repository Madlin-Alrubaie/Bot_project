from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

query = input("اكتب سؤالك: ")

results = db.similarity_search(query, k=3)

for i, doc in enumerate(results):
    print("\n--- Result", i+1, "---")
    print(doc.page_content)
