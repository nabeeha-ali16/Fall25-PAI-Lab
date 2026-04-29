import os
import re
import numpy as np
import pandas as pd
import faiss
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s\?\'\-]', '', text)
        return text.lower().strip()
    return ''

def load_hotel_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data")
    csv_file  = os.path.join(data_path, "hotel_qna.csv")

    if not os.path.exists(csv_file):
        # fallback: look for the CSV right next to app.py
        csv_file = os.path.join(base_dir, "hotel_qna.csv")
        if not os.path.exists(csv_file):
            print("[ERROR] hotel_qna.csv not found. "
                  "Place it in the 'data' folder or next to app.py")
            exit(1)

    df = pd.read_csv(
        csv_file,
        quotechar='"',         
        on_bad_lines='skip',   
        engine='python'        
    )

    if "question" not in df.columns or "answer" not in df.columns:
        raise ValueError("CSV must contain 'question' and 'answer' columns")

    # clean data
    df.dropna(subset=["question", "answer"], inplace=True)
    df = df[df["question"].str.strip() != ""]
    df = df[df["answer"].str.strip() != ""]
    df.reset_index(drop=True, inplace=True)

    df["clean_question"] = df["question"].apply(clean_text)

    print(f"[INFO] Loaded {len(df)} QnA pairs successfully")
    return df

def build_embeddings(df, model):
    print("[INFO] Creating embeddings...")
    embeddings = model.encode(
        df["clean_question"].tolist(),
        convert_to_numpy=True,
        show_progress_bar=True
    )
    return embeddings.astype(np.float32)

def build_faiss_index(embeddings):
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    print(f"[INFO] FAISS index built with {index.ntotal} vectors")
    return index

def retrieve_answers(query, model, index, df, k=3):
    query_vec          = model.encode([clean_text(query)]).astype(np.float32)
    distances, indices = index.search(query_vec, k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        row = df.iloc[idx]
        results.append({
            "question": row["question"],
            "answer":   row["answer"],
            "distance": float(distances[0][i])
        })

    return results

print("[START] Loading model...")
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

print("[START] Loading dataset...")
hotel_df = load_hotel_data()

print("[START] Building embeddings...")
embeddings = build_embeddings(hotel_df, model)

print("[START] Building FAISS index...")
faiss_index = build_faiss_index(embeddings)

print("[READY] Chatbot is running!")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data  = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    results = retrieve_answers(query, model, faiss_index, hotel_df)

    return jsonify({
        "query":   query,
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

