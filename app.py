import streamlit as st
import requests
from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


st.set_page_config(
    page_title="Ibb University AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 مساعد جامعة إب الذكي")
st.caption("يعتمد فقط على بيانات الجامعة الرسمية")


if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])



embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

# ======================
# دالة الذكاء الاصطناعي
# ======================

def ask_ai(question, context):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer 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"
,
        "Content-Type": "application/json"
    }


    

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": """
أنت مساعد جامعة إب.
قواعد صارمة:
- استخدم فقط المعلومات الموجودة في السياق
- لا تخترع أي معلومة
- إذا لا يوجد جواب قل: لا توجد معلومات كافية في بيانات الجامعة
"""
            },
            {
                "role": "user",
                "content": f"المعلومات:\n{context}\n\nالسؤال: {question}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return "خطأ في API"

# ======================
# إدخال المستخدم
# ======================

query = st.chat_input("اكتب سؤالك هنا...")

# ======================
# معالجة السؤال
# ======================

if query:

    # حفظ السؤال
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    query_clean = query.strip().lower()

    # أسئلة عامة
    general_questions = [
        "كيف حالك",
        "شكرا",
        "شكراً",
        "مرحبا",
        "هلا",
        "باي"
    ]

    if query_clean in general_questions:

        answer = "أنا مساعد جامعة إب الذكي، جاهز أساعدك في أي استفسار جامعي."
        sources = []

    else:

        # البحث في قاعدة البيانات
        docs = db.similarity_search(query, k=4)

        context_parts = [d.page_content for d in docs if d.page_content]
        context = "\n\n".join(context_parts)

        if len(context.strip()) < 20:

            answer = "لا توجد معلومات كافية في بيانات الجامعة للإجابة على هذا السؤال."
            sources = []

        else:

            answer = ask_ai(query, context)

            # استخراج المصادر الحقيقية فقط
            sources = []

            for d in docs:
                src = d.metadata.get("source", "")
                if src and src not in sources:
                    sources.append(src)

            sources = sources[:2]

    # ======================
    # تجهيز الرد النهائي
    # ======================

    final_answer = answer

    if sources:
        final_answer += "\n\n📚 المصادر:\n" + "\n".join([f"- {s}" for s in sources])

    # حفظ الرد
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer
    })

    # حفظ في ملف لوج
    with open("logs/questions.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "="*50 + "\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Q: {query}\n")
        f.write(f"A: {answer}\n")

    st.rerun()

