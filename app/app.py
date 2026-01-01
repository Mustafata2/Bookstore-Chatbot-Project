import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import joblib
import pandas as pd
import random

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILE_PATH = r"C:\Users\MUSTAFA\Desktop\Chatbot\data\iade.pdf"
EXCEL_FILE_PATH = r"C:\Users\MUSTAFA\Desktop\Chatbot\data\kitap_envanteri.xlsx"
NB_MODEL = r"C:\Users\MUSTAFA\Desktop\Chatbot\models\nb_intent_model.pkl"
LR_MODEL = r"C:\Users\MUSTAFA\Desktop\Chatbot\models\lr_intent_model.pkl"
VECTORIZER_PATH = r"C:\Users\MUSTAFA\Desktop\Chatbot\models\tfidf_vectorizer.pkl"


st.set_page_config(page_title="Bookstore Chatbot", page_icon="🤖")
st.title("🤖 Bookstore Chatbot")

df = pd.read_excel(EXCEL_FILE_PATH)

@st.cache_resource
def initialize_rag_system():
    if not os.path.exists(PDF_FILE_PATH):
        return None, f"HATA: '{PDF_FILE_PATH}' dosyası klasörde bulunamadı!"

    try:
        loader = PyPDFLoader(PDF_FILE_PATH)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500
        )
        splits = text_splitter.split_documents(docs)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            max_tokens=2000
        )

        prompt_template = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            ("user", "{input}")
        ])

        document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

        rag_chain = create_retrieval_chain(
            retriever,
            document_chain
        )

        return rag_chain, None

    except Exception as e:
        return None, f"HATA: PDF işleme sırasında bir hata oluştu: {str(e)}"
    

def load_intent_model():
    try:
        nb_model = joblib.load(NB_MODEL)
        lr_model = joblib.load(LR_MODEL)
        vectorizer = joblib.load(VECTORIZER_PATH)
        return nb_model, lr_model, vectorizer, None
    except Exception as e:
        return None, None, None, f"HATA: Model yükleme sırasında bir hata oluştu: {str(e)}"


nb_model, lr_model, vectorizer, model_error = load_intent_model()

def find_intent(user_input):
    if nb_model is None or lr_model is None or vectorizer is None:
        return None, "Modeller yüklenemedi."

    input_vec = vectorizer.transform([user_input])

    nb_pred = nb_model.predict(input_vec)[0]
    lr_pred = lr_model.predict(input_vec)[0]

    return lr_pred

rag_chain, rag_error = initialize_rag_system()

def find_book(query):
    query = query.lower()
    for _, row in df.iterrows():
        book = str(row.get("Kitap Adi", "")).lower()
        if book in query:
            return row
    return None

def find_author(query):
    query = query.lower()
    authors = set(df["Yazar"].dropna().unique())
    for author in authors:
        if author.lower() in query:
            return author
    return None

def find_category(query):
    query = query.lower()
    categories = set(df["Tur"].dropna().unique())
    for category in categories:
        if category.lower() in query:
            return category
    return None

def answer_question(question):
    if rag_chain is None:
        return f"Soru-cevap sistemi başlatılamadı: {rag_error}"

    try:
        intent = find_intent(question)

        if intent == "return_product":
            if rag_chain:
                response = rag_chain.invoke({"input": question})
                answer = response["answer"]
                return answer
            else:
                return "Bu soruyla ilgili bilgiye sahip değilim. Lütfen iade ile ilgili bir soru sorun."
            
        elif intent == "greeting":
            return random.choice(["Merhaba! Size nasıl yardımcı olabilirim?", "Selam! Kitaplarla ilgili bir sorunuz mu var?", "Hoş geldiniz! Size nasıl yardımcı olabilirim?"])

        elif intent == "goodbye":
            return random.choice(["Görüşmek üzere! İyi günler dilerim.", "Hoşça kalın! Kitaplarla dolu günler!", "Tekrar beklerim! Kitap keyfi sizinle olsun!"])

        elif intent == "ask_price":
            book = find_book(question)
            if book is not None:
                return f"'{book['Kitap Adi']}' kitabının fiyatı {book['Fiyat']} TL'dir."
            else:
                return "Hangi kitabın fiyatını öğrenmek istiyorsunuz? Kitap adını tam yazabilir misiniz?"
        
        elif intent == "ask_stock":
            book = find_book(question)
            if book is not None:
                stok = book["Stok"]
                if stok:
                    return f"'{book['Kitap Adi']}' kitabı stoklarımızda mevcut."
                else:
                    return f"Üzgünüm, '{book['Kitap Adi']}' kitabı şu anda stoklarımızda bulunmamaktadır."
        
        elif intent == "add_to_cart":
            book = find_book(question)
            if book is not None:
                return f"'{book['Kitap Adi']}' kitabını sepete ekledim."
            else:
                return "Hangi kitabı sepete eklemek istiyorsunuz? Kitap adını tam yazabilir misiniz?"

        elif intent == "ask_category":
            category = find_category(question)
            if category is not None:
                books_in_category = df[df["Tur"] == category]["Kitap Adi"].tolist()
                if books_in_category:
                    books_list = ", ".join(books_in_category)
                    return f"'{category}' kategorisindeki kitaplar: {books_list}."
                else:
                    return f"Üzgünüm, '{category}' kategorisinde kitaplarımız bulunmamaktadır."
            else:
                return "Hangi kategoriye ait kitapları öğrenmek istiyorsunuz? Kategori adını tam yazabilir misiniz?"

        elif intent == "surprise_recommendation":
            random_book = df.sample(n=1).iloc[0]
            return f"Sürpriz kitap önerisi: '{random_book['Kitap Adi']}' by {random_book['Yazar']}, Fiyat: {random_book['Fiyat']} TL."

        else:
            return "Bu soruyla ilgili bilgiye sahip değilim."
        

    
    except Exception as e:
        return f"Soru yanıtlanırken bir hata oluştu: {str(e)}"



if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben Kitap Dünyası asistanıyım. İade, stok veya fiyat sorabilirsiniz."}]

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_input := st.chat_input("Sorunuzu buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.chat_message("assistant"):
        with st.spinner("Cevap oluşturuluyor..."):
            answer = answer_question(prompt_input)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})