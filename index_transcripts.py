# ============================== index_transcripts.py ==============================
import os
import re
import pandas as pd
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st

TRANSCRIPTS_DIR = "data/transcripts/"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# Load metadata from updated Excel file
def load_metadata():
    df = pd.read_excel("data/Podcast Transcripts.xlsx", sheet_name="Sheet 1", skiprows=1)
    metadata_map = {}
    for _, row in df.iterrows():
        key = str(row["#"]).strip().replace("#", '')
        metadata_map[key] = {
            "video_title": row["Title"],
            "episode_description": row["Description"],
            "video_url": row["Link"],
            "episode_date": row["Date"],
            "topics_covered": row.get("Topics Covered", "")
        }
    return metadata_map


# Index transcripts
def index_all_transcripts():
    documents = []
    metadata_map = load_metadata()

    for filename in os.listdir(TRANSCRIPTS_DIR):
        if filename.endswith(".docx"):
            episode_number = ''.join(filter(str.isdigit, filename))
            if episode_number not in metadata_map:
                continue
            meta = metadata_map[episode_number]

            path = os.path.join(TRANSCRIPTS_DIR, filename)
            loader = Docx2txtLoader(path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            chunks = splitter.split_documents(docs)

            for doc in chunks:
                doc.metadata.update(meta)
                match = re.search(r"\[(\d{1,2}):(\d{2}):(\d{2})\]", doc.page_content)
                if match:
                    h, m, s = map(int, match.groups())
                    doc.metadata['timestamp'] = h * 3600 + m * 60 + s
                else:
                    doc.metadata['timestamp'] = 0

            documents.extend(chunks)

    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
    if not documents:
        print("No documents were indexed. Please check your transcript files.")
        return

    db = FAISS.from_documents(documents, embeddings)
    db.save_local("video_index")
    print("Indexing complete.")


if __name__ == "__main__":
    index_all_transcripts()
