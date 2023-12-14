import logging
import numpy as np
import pandas as pd
import heapq
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from flask import Flask, request, jsonify
import os


# Create Flask application
app = Flask(__name__)

# Lower logging level to give info to user
logging.getLogger().setLevel(logging.INFO)


# Get movie path
CWD = os.getcwd()
movies_path = os.path.join(CWD, "dataset", "IMDb movies.csv")

# Get movies dataset
movies = pd.read_csv(os.path.join(CWD, "dataset", "IMDb movies.csv"))
# Remove nan
movies = movies.where(pd.notnull(movies), "")

# Initialize TfidfVectorizer
tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
tfidf_wm = tfidfvectorizer.fit_transform(movies["description"])

# Initialize BM25Okapi
tokenized_docs = [document.split(" ") for document in movies["description"]]
bm25_wm = BM25Okapi(tokenized_docs)



#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Methods
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
def query(sentence):
    # Scores will be calculated with cosine similarity function

    # Get scores from TF-IDF
    query_scores_tfidf = tfidfvectorizer.transform([sentence])
    query_scores_tfidf = cosine_similarity(query_scores_tfidf, tfidf_wm).flatten()

    # Get scores from BM25
    query_scores_bm25 = bm25_wm.get_scores(sentence)
    # Normalize scores
    query_scores_bm25 = query_scores_bm25 /  np.linalg.norm(query_scores_bm25)

    top10_tfidf = heapq.nlargest(10, np.ndenumerate(query_scores_tfidf), key=lambda x: x[1])
    top10_bm25 = heapq.nlargest(10, np.ndenumerate(query_scores_bm25), key=lambda x: x[1])
    
    return({"tfidf": top10_tfidf, "bm25": top10_bm25})


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: FLASK
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
@app.route('/', methods=['POST'])
def handle_request():
    try:
        data = request.get_json()

        if data is None or "query" not in data:
            return jsonify({"error": "Invalid JSON data or missing 'query' key"}), 400

        data = data["query"]

        # Process the received data
        result = query(data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Main
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
