# app/services/recommender.py

import os
import joblib
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))
ARTIFACT_DIR = os.path.join(BACKEND_ROOT, "artifacts")


class ContentRecommender:

    def __init__(self):
        self.movies = joblib.load(os.path.join(ARTIFACT_DIR, "movies.pkl"))
        self.vectorizer = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf.pkl"))
        self.tfidf_matrix = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf_matrix.pkl"))

        self.indices = pd.Series(
            self.movies.index,
            index=self.movies["title"].str.lower()
        ).drop_duplicates()

    def fetch_poster(self, title):
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    def recommend(self, movie_name: str, top_n: int = 10):

        if not movie_name:
            return []

        movie_name = movie_name.lower().strip()

        if movie_name not in self.indices:
            return []

        idx = self.indices[movie_name]
        query_vector = self.tfidf_matrix[idx]

        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        similarity_scores = list(enumerate(similarity_scores))
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[: top_n]

        results = []

        for i in similarity_scores:
            movie_data = self.movies.iloc[i[0]]
            title = movie_data["title"]

            results.append({
                "title": title,
                "poster_url": self.fetch_poster(title),
                "wikipedia_url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            })

        return results