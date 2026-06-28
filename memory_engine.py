import cognee
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


async def setup_cognee():
    """Initialize Cognee with API keys and local storage."""
    await cognee.config.set_llm_config({
        "provider": "openai",
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    })
    await cognee.config.set_vector_db_config({
        "provider": "lancedb",
        "url": "./memorymirror_db"
    })


async def store_entry(entry_text: str, entry_date: str = None) -> str:
    """
    Store a journal entry in Cognee memory.
    Cognee will automatically extract entities, emotions, themes,
    and build graph edges between related concepts.
    """
    await setup_cognee()

    if entry_date is None:
        entry_date = datetime.now().strftime("%Y-%m-%d")

    # Wrap the entry with metadata so Cognee can build richer graph nodes
    enriched_text = f"""
    Journal Entry — {entry_date}
    ---
    {entry_text}
    ---
    Context: This is a personal reflection from a user. Extract themes, emotions,
    people mentioned, events, stressors, and goals. Connect this to related past memories.
    """

    await cognee.add(enriched_text, dataset_name="journal_entries")
    await cognee.cognify()  # This is where Cognee builds the graph connections

    return "Entry stored and connected to memory graph."


async def retrieve_relevant_memories(query: str, top_k: int = 5) -> list[str]:
    """
    Search Cognee's graph-vector store for memories relevant to the query.
    Returns a list of relevant past entry snippets.
    """
    try:
        await setup_cognee()

        results = await cognee.search(
            query_text=query,
            query_type="GRAPH_COMPLETION"  # Uses graph traversal, not just vector similarity
        )

        if not results:
            return []

        # Extract text from results
        memories = []
        for result in results[:top_k]:
            if hasattr(result, 'text'):
                memories.append(result.text)
            elif isinstance(result, dict) and 'text' in result:
                memories.append(result['text'])
            elif isinstance(result, str):
                memories.append(result)

        return memories

    except Exception as e:
        print(f"[MemoryMirror] retrieve_relevant_memories error: {e}")
        return []


async def get_all_themes() -> list[str]:
    """
    Ask Cognee to surface recurring themes across all stored memories.
    Used to show the user patterns over time.
    """
    try:
        await setup_cognee()

        results = await cognee.search(
            query_text="What are the recurring themes, emotions, and stressors across all journal entries?",
            query_type="GRAPH_COMPLETION"
        )

        themes = []
        for result in results[:8]:
            if hasattr(result, 'text'):
                themes.append(result.text)
            elif isinstance(result, dict) and 'text' in result:
                themes.append(result['text'])
            elif isinstance(result, str):
                themes.append(result)

        return themes

    except Exception as e:
        print(f"[MemoryMirror] get_all_themes error: {e}")
        return []


async def get_memory_graph_data() -> dict:
    """
    Extract nodes and edges from Cognee's graph for visualization.
    Returns data formatted for pyvis network graph.
    """
    try:
        await setup_cognee()

        # Query for connected concepts to build a visualization
        results = await cognee.search(
            query_text="Show all connected themes, emotions, events, and people",
            query_type="GRAPH_COMPLETION"
        )

        # Build a simple node-edge structure from results
        nodes = set()
        edges = []

        keywords = [
            "stress", "anxiety", "interview", "parents", "pressure", "tired",
            "exhausted", "happy", "excited", "worried", "work", "college",
            "placement", "friends", "sleep", "focus", "motivation", "fear",
            "confidence", "study", "exam", "future", "career", "family"
        ]

        for result in results:
            text = ""
            if hasattr(result, 'text'):
                text = result.text.lower()
            elif isinstance(result, dict) and 'text' in result:
                text = result['text'].lower()
            elif isinstance(result, str):
                text = result.lower()

            found_in_this = [k for k in keywords if k in text]
            nodes.update(found_in_this)

            # Connect co-occurring concepts
            for i in range(len(found_in_this)):
                for j in range(i + 1, len(found_in_this)):
                    edges.append((found_in_this[i], found_in_this[j]))

        return {"nodes": list(nodes), "edges": edges}

    except Exception as e:
        print(f"[MemoryMirror] get_memory_graph_data error: {e}")
        return {"nodes": [], "edges": []}


