from pydantic import BaseModel
from typing import List, Optional


class Movie(BaseModel):
    title: str
    poster_url: Optional[str] = None
    wikipedia_url: str


class RecommendationResponse(BaseModel):
    query: str
    results: List[Movie]
    message: Optional[str] = None