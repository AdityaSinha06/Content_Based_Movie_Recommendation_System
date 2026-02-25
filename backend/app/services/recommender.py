# app/services/recommender.py

import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))
ARTIFACT_DIR = os.path.join(PROJECT_ROOT, "artifacts")


class ContentRecommender:

    def __init__(self):
        self.movies = joblib.load(os.path.join(ARTIFACT_DIR, "movies.pkl"))
        self.vectorizer = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf.pkl"))
        self.tfidf_matrix = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf_matrix.pkl"))

        self.indices = pd.Series(
            self.movies.index,
            index=self.movies["title"].str.lower()
        ).drop_duplicates()

    def recommend(self, movie_name: str, top_n: int = 10):

        if not movie_name:
            return []

        movie_name = movie_name.lower().strip()

        if movie_name not in self.indices:
            return []

        idx = self.indices[movie_name]

        # Get vector of queried movie
        query_vector = self.tfidf_matrix[idx]

        # Compute cosine similarity ON DEMAND
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # Enumerate + sort
        similarity_scores = list(enumerate(similarity_scores))
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[: top_n]

        results = []

        for i in similarity_scores:
            movie_data = self.movies.iloc[i[0]]

            results.append({
                "title": movie_data["title"],
                "poster_url": None,
                "wikipedia_url": f"https://en.wikipedia.org/wiki/{movie_data['title'].replace(' ', '_')}"
            })

        return results