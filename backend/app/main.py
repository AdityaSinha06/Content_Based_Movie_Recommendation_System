from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.services.recommender import ContentRecommender
from app.api.schemas import RecommendationResponse

app = FastAPI(title="Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = ContentRecommender()


@app.get("/")
def root():
    return {"message": "Movie Recommender API is running"}

@app.get("/recommend", response_model=RecommendationResponse)
def recommend(query: str, top_n: int = 10):

    result = recommender.recommend(query, top_n)

    if isinstance(result, dict) and "error" in result:
        return {
            "query": query,
            "results": [],
            "message": result["error"]
        }

    return {
        "query": query,
        "results": result,
        "message": None
    }