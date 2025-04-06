# ============================== teacher_query_module.py ==============================
from langchain_community.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import streamlit as st


# Load FAISS retriever
def load_retriever():
    db = FAISS.load_local("video_index", OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"]),
                          allow_dangerous_deserialization=True)
    return db.as_retriever(search_type="similarity", k=3)


# Generate teaching question and answer key
def generate_teaching_prompt(prompt_text: str):
    retriever = load_retriever()
    docs = retriever.get_relevant_documents(prompt_text)
    best_doc = docs[0]

    context = best_doc.page_content
    meta = best_doc.metadata

    prompt = PromptTemplate.from_template(
        '''
        You are an expert educator helping design a flipped classroom activity using podcast transcripts.
        
        You are an expert who will help teachers to provide a question to students based on the 
        SUBJECT OF THE PROVIDED TOPIC, 
        SUBJECT OF THE PODCAST EPISODE, 
        AND HOW ARE THEY RELATED?

        The question and answer should connect the topic and the DSRP concept from the video.
    
        The teacher gave the following context about their course:
        """
        {teacher_prompt}
        """

        Here is a video:
        """
        {context}
        """

        Based on this, provide:
        1. A clear question the students should answer after watching the episode.
        2. A model answer that demonstrates deep understanding that the teacher can use as a sample for evaluating actual results.
        '''
    )

    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"])
    final_prompt = prompt.format(teacher_prompt=prompt_text, context=context)
    response = llm.invoke(final_prompt)

    return {
        "title": meta.get("video_title", "Unknown Episode"),
        "url": meta.get("video_url", ""),
        "student_question": response.content.strip().split("\n")[0],
        "answer_key": "\n".join(response.content.strip().split("\n")[1:]).strip()
    }
