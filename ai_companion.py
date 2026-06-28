import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are MemoryMirror — a warm, thoughtful reflection companion.

Your personality:
- Curious and empathetic, not clinical or therapeutic
- You notice patterns and gently name them
- You ask ONE good question at a time, never multiple
- You never give advice unless asked
- You speak like a wise friend who has been paying attention

Your special ability:
You have access to the user's past journal entries through a memory system called Cognee.
Cognee doesn't just retrieve facts — it builds a knowledge graph connecting themes, emotions,
events, and patterns across time. When you respond, use this memory to surface connections
the user may not have noticed themselves.

Rules:
- Always reference specific past memories when you have them ("A few weeks ago you mentioned...")
- If you see a pattern across multiple entries, name it clearly and specifically
- Never say "I'm an AI" or "I'm not a therapist" — just be present and human
- Keep responses under 150 words unless the user asks for more
- End every response with exactly ONE reflective question
- Never use bullet points. Always write in warm, flowing prose.
"""


async def get_ai_response(user_message: str, relevant_memories: list[str], chat_history: list[dict]) -> str:
    """
    Call Gemini with the user's message, relevant memories from Cognee,
    and the current conversation history.
    """

    if relevant_memories:
        memory_context = "RELEVANT MEMORIES FROM COGNEE (use these to find patterns and connections):\n\n"
        for i, memory in enumerate(relevant_memories, 1):
            memory_context += f"Memory {i}: {memory[:300]}...\n\n"
    else:
        memory_context = "MEMORY CONTEXT: This appears to be the first entry. No past memories yet — focus on the present moment and invite the user to share more."

    gemini_history = []
    for msg in chat_history[-12:]:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    augmented_message = f"""{memory_context}

---

USER'S CURRENT MESSAGE:
{user_message}

---

Remember: Use the memories above to surface connections. Find the pattern. Ask one good question."""

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(augmented_message)

    return response.text


async def get_pattern_analysis(themes: list[str]) -> str:
    """
    Ask Gemini to analyze the themes Cognee surfaced and write a
    meaningful pattern summary for the user.
    """
    if not themes:
        return "Not enough entries yet to detect patterns. Keep journaling — patterns emerge over time."

    themes_text = "\n".join(themes[:6])

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(
        f"""You are MemoryMirror. Based on these memory themes Cognee extracted from a user's journal entries, write a warm, insightful 3-sentence pattern summary. Be specific. Name what you see. Don't use bullet points.

Themes from memory graph:
{themes_text}

Write the pattern summary now:"""
    )

    return response.text
