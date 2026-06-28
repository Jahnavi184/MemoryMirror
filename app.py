import streamlit as st
import asyncio
from datetime import datetime
from memory_engine import store_entry_sync, retrieve_memories_sync, get_themes_sync, get_graph_data_sync
from ai_companion import get_ai_response, get_pattern_analysis

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MemoryMirror",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Overall app */
    .stApp { background-color: #0f0f13; color: #e8e8f0; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #16161e; border-right: 1px solid #2a2a3a; }

    /* Chat messages */
    .user-msg {
        background: #1e1e2e;
        border: 1px solid #2a2a3a;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        margin-left: 20%;
        font-size: 14px;
        line-height: 1.6;
    }
    .ai-msg {
        background: #1a1a2e;
        border: 1px solid #3a3a5c;
        border-left: 3px solid #7c6af7;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        margin-right: 10%;
        font-size: 14px;
        line-height: 1.6;
        color: #d0d0e8;
    }
    .memory-tag {
        display: inline-block;
        background: #2a2040;
        color: #9b87f5;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 20px;
        margin: 2px;
    }
    .pattern-box {
        background: #1e1a30;
        border: 1px solid #5a4a9a;
        border-radius: 12px;
        padding: 16px;
        font-size: 14px;
        line-height: 1.7;
        color: #c8b8f8;
        font-style: italic;
    }
    h1 { color: #c8b8f8 !important; }
    h2, h3 { color: #a090e8 !important; }

    /* Input box */
    .stTextArea textarea {
        background: #1e1e2e !important;
        color: #e8e8f0 !important;
        border: 1px solid #3a3a5c !important;
        border-radius: 10px !important;
        font-size: 14px !important;
    }

    /* Buttons */
    .stButton > button {
        background: #5a4af0 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background: #7c6af7 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []
if "entry_count" not in st.session_state:
    st.session_state.entry_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🪞 MemoryMirror")
    st.markdown("*It connects the dots between your days, so you can finally see the pattern.*")
    st.divider()

    st.markdown("### How it works")
    st.markdown("""
    1. **Write** what's on your mind
    2. **Cognee** stores it as a graph node, connected to related memories
    3. **MemoryMirror** surfaces patterns across time
    4. You see yourself more clearly
    """)

    st.divider()

    # Pattern analysis button
    st.markdown("### Your patterns")
    if st.button("✦ Analyze my patterns", use_container_width=True):
        with st.spinner("Cognee is scanning your memory graph..."):
            themes = get_themes_sync()
            analysis = get_pattern_analysis(themes)
            st.session_state.pattern_analysis = analysis

    if "pattern_analysis" in st.session_state:
        st.markdown(f'<div class="pattern-box">{st.session_state.pattern_analysis}</div>', unsafe_allow_html=True)

    st.divider()

    # Memory graph button
    st.markdown("### Memory graph")
    if st.button("⬡ Show memory graph", use_container_width=True):
        st.session_state.show_graph = True

    st.divider()
    st.markdown(f"<small style='color:#5a5a7a'>Entries in memory: {st.session_state.entry_count}</small>", unsafe_allow_html=True)
    st.markdown(f"<small style='color:#5a5a7a'>Powered by Cognee + Gemini</small>", unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("## What's on your mind?")
st.markdown("<small style='color:#6a6a8a'>Write freely. MemoryMirror remembers everything — and connects what matters.</small>", unsafe_allow_html=True)

# Show memory graph if requested
if st.session_state.get("show_graph"):
    st.markdown("### Memory graph — how your thoughts connect")
    with st.spinner("Building graph from Cognee memory..."):
        try:
            from pyvis.network import Network
            import streamlit.components.v1 as components

            graph_data = get_graph_data_sync()

            net = Network(height="400px", width="100%", bgcolor="#16161e", font_color="#c8b8f8")
            net.barnes_hut()

            for node in graph_data["nodes"]:
                net.add_node(node, label=node, color="#7c6af7", size=20, font={"size": 14, "color": "#e8e8f0"})

            for edge in graph_data["edges"]:
                if edge[0] in graph_data["nodes"] and edge[1] in graph_data["nodes"]:
                    net.add_edge(edge[0], edge[1], color="#3a3a5c")

            net.save_graph("/tmp/memory_graph.html")

            with open("/tmp/memory_graph.html", "r") as f:
                html = f.read()
            components.html(html, height=420)

        except Exception as e:
            st.error(f"Graph error: {e}. Make sure pyvis is installed.")

    if st.button("✕ Close graph"):
        st.session_state.show_graph = False
        st.rerun()

# Chat display
chat_container = st.container()
with chat_container:
    for msg in st.session_state.display_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">🪞 {msg["content"]}</div>', unsafe_allow_html=True)

st.divider()

# Input area
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_area(
        "Your entry",
        placeholder="Write anything — what happened today, how you're feeling, what's worrying you...",
        label_visibility="collapsed",
        height=100,
        key="user_input"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    send = st.button("Send →", use_container_width=True)

if send and user_input.strip():
    entry_text = user_input.strip()

    # Add user message to display
    st.session_state.display_messages.append({"role": "user", "content": entry_text})

    # Store in Cognee memory graph
    with st.spinner("Saving to memory..."):
        store_entry_sync(entry_text)
        st.session_state.entry_count += 1

    # Retrieve relevant past memories from Cognee
    with st.spinner("Searching memory graph for connections..."):
        memories = retrieve_memories_sync(entry_text)

    # Get AI response using memories as context
    with st.spinner("MemoryMirror is reflecting..."):
        response = get_ai_response(
            user_message=entry_text,
            relevant_memories=memories,
            chat_history=st.session_state.chat_history
        )

    # Update chat history for next turn
    st.session_state.chat_history.append({"role": "user", "content": entry_text})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Add AI response to display
    st.session_state.display_messages.append({"role": "assistant", "content": response})

    st.rerun()
