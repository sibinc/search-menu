# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = FastAPI()

# Define the features and other required functions here...
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
features = [
    # Define your feature list and mappings...
]

# Function to search features
def search_feature(query, top_k=3, threshold=0.5):
    # Function implementation as shown previously...
    pass

class QueryRequest(BaseModel):
    query: str

@app.post("/search-ai")
async def search_ai(request: QueryRequest):
    results = search_feature(request.query)
    return {"results": results}
