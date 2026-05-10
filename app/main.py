from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import retrieve_assessments
from app.agent import build_agent_response

from app.catalog_loader import load_catalog
from app.state_extractor import extract_state

app = FastAPI()
@app.get("/")
def root():

    return {
        "message": "SHL Assessment Recommendation API"
    }
catalog = load_catalog()


class ChatRequest(BaseModel):
    messages: list


@app.get("/health")
def health():
    return {
        "status": "ok",
        "catalog_size": len(catalog)
    }


@app.post("/debug-state")
def debug_state(request: ChatRequest):

    state = extract_state(request.messages)

    return state

@app.post("/debug-retrieval")
def debug_retrieval(request: ChatRequest):

    state = extract_state(request.messages)

    results = retrieve_assessments(state, catalog)

    return [
        {
            "name": item.name,
            "url": item.url,
            "categories": item.categories
        }
        for item in results
    ]

@app.post("/chat")
def chat(request: ChatRequest):

    response = build_agent_response(
        request.messages,
        catalog
    )

    return response
