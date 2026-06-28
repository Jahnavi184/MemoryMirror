from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from memory_engine import store_entry, retrieve_relevant_memories, get_all_themes, get_memory_graph_data
from ai_companion import get_ai_response, get_pattern_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    chat_history: list[dict] = []


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    """Store the entry, retrieve memories, return AI response."""
    await store_entry(req.message)
    memories = await retrieve_relevant_memories(req.message)
    response = await get_ai_response(req.message, memories, req.chat_history)
    return {"response": response}


@app.get("/patterns")
async def patterns():
    """Return Cognee themes + Gemini pattern analysis."""
    themes = await get_all_themes()
    analysis = await get_pattern_analysis(themes)
    return {"analysis": analysis}


@app.get("/graph")
async def graph():
    """Return memory graph nodes and edges."""
    data = await get_memory_graph_data()
    return data
