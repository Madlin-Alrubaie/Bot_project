from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import os

# =========================
# قراءة جميع ملفات PDF
# =========================

all_docs = []

data_folder = "data"

for file in os.listdir(data_folder):

    if file.endswith(".pdf"):

        file_path = os.path.join(data_folder, file)

        print(f"جاري قراءة الملف: {file}")

        loader = PyPDFLoader(file_path)

        docs = loader.load()

        all_docs.extend(docs)

# =========================
# تقسيم النصوص
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=300
)

split_docs = text_splitter.split_documents(all_docs)

print(f"عدد الأجزاء بعد التقسيم: {len(split_docs)}")

# =========================
# نموذج الـ Embedding
# =========================

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# إنشاء قاعدة البيانات
# =========================

db = Chroma.from_documents(
    split_docs,
    embedding,
    persist_directory="chroma_db"
)

db.persist()

print("تم إنشاء قاعدة البيانات بنجاح")