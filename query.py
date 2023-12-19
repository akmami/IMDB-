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
import traceback


# Create Flask application
app = Flask(__name__)

# Lower logging level to give info to user
logging.getLogger().setLevel(logging.INFO)


# Get movie path
CWD = os.getcwd()
movies_path = os.path.join(CWD, "dataset", "IMDb movies preprocessed.csv")

# Get movies dataset
movies = pd.read_csv(os.path.join(CWD, "dataset", "IMDb movies preprocessed.csv"))
# Remove nan
movies = movies.where(pd.notnull(movies), "")

# Initialize TfidfVectorizer
tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
tfidf_wm = tfidfvectorizer.fit_transform(movies["detailed_description"])

# Initialize BM25Okapi
tokenized_docs = [document.split(" ") for document in movies["detailed_description"]]
bm25_wm = BM25Okapi(movies["detailed_description"])



#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
# MARK: Methods
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
def query(sentence):
    try:

        # Scores will be calculated with cosine similarity function

        # Get scores from TF-IDF
        query_scores_tfidf = tfidfvectorizer.transform([sentence])
        query_scores_tfidf = cosine_similarity(query_scores_tfidf, tfidf_wm).flatten()
        query_scores_tfidf_indeces = np.argpartition(query_scores_tfidf, -10)[-10:]
        query_scores_tfidf_10_values = movies.iloc[query_scores_tfidf_indeces]

        # Get scores from BM25
        query_scores_bm25 = bm25_wm.get_scores(sentence)
        query_scores_bm25 = (query_scores_bm25 - np.min(query_scores_bm25)) / (np.max(query_scores_bm25) - np.min(query_scores_bm25) )
        query_scores_bm25_indeces = np.argpartition(query_scores_bm25, -10)[-20:]
        query_scores_bm25_10_movies = movies.iloc[query_scores_bm25_indeces]

        logging.warn(query_scores_bm25_indeces)
        logging.warn(query_scores_bm25_10_movies["imdb_title_id"])
        logging.warn(query_scores_bm25)
        logging.warn(query_scores_bm25_10_movies)

        return {"movies": query_scores_tfidf_10_values.to_dict(orient="records")}
    
    except Exception as e:
        traceback_str = traceback.format_exc()
        logging.error(f"An error occurred: {e}\n{traceback_str}")
        return jsonify({"error": str(e), "traceback": traceback_str}), 500

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
