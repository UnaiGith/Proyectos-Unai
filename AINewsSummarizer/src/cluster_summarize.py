import pandas as pd
import numpy as np
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import hdbscan
from datetime import date

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)



# === MODELS ===
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# === EXTRACTIVE SUMMARIZATION ===
def extractive_summary(text, embedder, top_n=3):
    """Selects the most central sentences based on cosine similarity."""
    sentences = nltk.sent_tokenize(text)
    if len(sentences) <= top_n:
        return text
    sentence_embeddings = embedder.encode(sentences)
    sim_matrix = cosine_similarity(sentence_embeddings)
    centrality = sim_matrix.sum(axis=1)
    top_indices = np.argsort(centrality)[-top_n:]
    summary = " ".join([sentences[i] for i in sorted(top_indices)])
    return summary


# === CLUSTERING + SUMMARIZATION PIPELINE ===
def cluster_and_summarize(file_path):
    print("🔹 Loading data...")
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["description", "title"], how="all")
    texts = (df["title"].fillna("") + ". " + df["description"].fillna("")).tolist()

    print("🔹 Encoding sentences...")
    embeddings = embedder.encode(texts, batch_size=8, show_progress_bar=True)

    print("🔹 Clustering with HDBSCAN...")
    clusterer = hdbscan.HDBSCAN(min_cluster_size=3, metric="euclidean")
    labels = clusterer.fit_predict(embeddings)
    df["cluster"] = labels

    # Filter out noise (-1 are unclustered items)
    valid_clusters = [c for c in np.unique(labels) if c != -1]

    print(f"✅ Found {len(valid_clusters)} topic clusters.")

    summaries = []
    for cluster_id in valid_clusters:
        cluster_texts = df[df["cluster"] == cluster_id]["description"].dropna().tolist()
        combined_text = " ".join(cluster_texts)
        summary = extractive_summary(combined_text, embedder, top_n=3)
        summaries.append({"cluster": cluster_id, "summary": summary})

    out_path = f"data/processed/cluster_summaries_{date.today()}.csv"
    pd.DataFrame(summaries).to_csv(out_path, index=False)
    print(f"✅ Saved {len(summaries)} summaries to {out_path}")


if __name__ == "__main__":
    cluster_and_summarize("data/raw/news_2025-12-01.csv")  # change to your file’s name
