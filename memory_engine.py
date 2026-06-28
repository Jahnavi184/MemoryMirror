import cognee
import asyncio
from datetime import datetime

# No setup_cognee() needed — Cognee reads LLM_PROVIDER, LLM_MODEL, LLM_API_KEY,
# EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_API_KEY from your .env automatically.


async def store_entry(entry_text: str, entry_date: str = None) -> str:
    """
    Store a journal entry in Cognee memory.
    Cognee extracts entities, emotions, themes and builds graph edges automatically.
    """
    if entry_date is None:
        entry_date = datetime.now().strftime("%Y-%m-%d")

    enriched_text = f"""
    Journal Entry — {entry_date}
    ---
    {entry_text}
    ---
    Context: This is a personal reflection from a user. Extract themes, emotions,
    people mentioned, events, stressors, and goals. Connect this to related past memories.
    """

    await cognee.remember(enriched_text)  # Cognee 1.x API: replaces add() + cognify()

    return "Entry stored and connected to memory graph."


async def retrieve_relevant_memories(query: str, top_k: int = 5) -> list[str]:
    """
    Search Cognee's graph-vector store for memories relevant to the query.
    """
    try:
        results = await cognee.recall(query)  # Cognee 1.x API: replaces search()

        if not results:
            return []

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
    Surface recurring themes across all stored memories.
    """
    try:
        results = await cognee.recall(
            "What are the recurring themes, emotions, and stressors across all journal entries?"
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
    """
    try:
        results = await cognee.recall(
            "Show all connected themes, emotions, events, and people"
        )

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

            for i in range(len(found_in_this)):
                for j in range(i + 1, len(found_in_this)):
                    edges.append((found_in_this[i], found_in_this[j]))

        return {"nodes": list(nodes), "edges": edges}

    except Exception as e:
        print(f"[MemoryMirror] get_memory_graph_data error: {e}")
        return {"nodes": [], "edges": []}


# Synchronous wrappers for Streamlit
def store_entry_sync(entry_text: str, entry_date: str = None) -> str:
    return asyncio.run(store_entry(entry_text, entry_date))

def retrieve_memories_sync(query: str) -> list[str]:
    return asyncio.run(retrieve_relevant_memories(query))

def get_themes_sync() -> list[str]:
    return asyncio.run(get_all_themes())

def get_graph_data_sync() -> dict:
    return asyncio.run(get_memory_graph_data())

