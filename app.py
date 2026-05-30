import streamlit as st
import joblib
import requests
import numpy as np
from numpy.linalg import norm

# =========================
# Load Embeddings
# =========================

data = joblib.load("embeddings.joblib")

# =========================
# Embedding Function
# =========================

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "bge-m3",
            "prompt": text
        }
    )

    embedding = response.json()["embedding"]

    return embedding

# =========================
# Cosine Similarity
# =========================

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (norm(a) * norm(b))

# =========================
# Find Best Matching Chunk
# =========================

def retrieve(query):

    query_embedding = get_embedding(query)

    best_score = -1
    best_chunk = None

    # Loop through chunks
    for item in data["chunks"]:

        score = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        if score > best_score:

            best_score = score
            best_chunk = item

    return best_chunk
# =========================
# LLM Inference
# =========================

def inference(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

# =========================
# Streamlit UI
# =========================

st.set_page_config(
    page_title="RAG AI Teaching Assistant",
    layout="centered"
)

st.title("📘 RAG AI Teaching Assistant")

st.write("Ask questions from your lecture videos.")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask AI"):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        # Retrieve Context
        best_chunk = retrieve(question)

        context = best_chunk["text"]

        # Final Prompt
        final_prompt = f"""
You are an AI Teaching Assistant.

Context:
{context}

Question:
{question}

Answer clearly and simply.
"""

        # Generate Answer
        answer = inference(final_prompt)

        # Display Results
        st.subheader("Answer")

        st.write(answer)

        st.subheader("Retrieved Context")

        st.write(context)

        st.subheader("Timestamp")

        st.write(
            f"{best_chunk['start']} sec → {best_chunk['end']} sec"
        )