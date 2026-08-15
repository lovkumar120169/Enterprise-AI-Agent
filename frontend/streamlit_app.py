import sys
from pathlib import Path
import streamlit as st
PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )
from backend.main import chat

st.set_page_config(
    page_title="Enterprise AI Agent - Luv",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# STYLE (kept minimal & scoped — only elements Streamlit's
# own theme doesn't already style are touched, so nothing
# fights the built-in contrast handling)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@500;600&display=swap');

    /* remove default Streamlit chrome + tighten top spacing */
    #MainMenu, footer, header { visibility: hidden; height: 0; }
    .block-container { padding-top: 2.2rem; padding-bottom: 6rem; max-width: 900px; }

    /* ---------------- HERO ---------------- */
    .agent-hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        row-gap: 14px;
        column-gap: 18px;
        padding: 24px 28px;
        margin-bottom: 22px;
        background: var(--secondary-background-color);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
    }
    .agent-hero-left { display: flex; align-items: center; gap: 14px; min-width: 0; }
    .agent-icon {
        width: 46px; height: 46px;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        background: linear-gradient(135deg, #5B8DEF, #2DD4BF);
        flex-shrink: 0;
    }
    .agent-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.25;
        color: var(--text-color);
    }
    .agent-subtitle {
        font-size: 0.8rem;
        color: #8B93A7;
        margin-top: 3px;
        display: flex;
        align-items: center;
        gap: 7px;
        font-family: 'JetBrains Mono', monospace;
    }
    .pulse-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #2DD4BF;
        box-shadow: 0 0 0 0 rgba(45,212,191, 0.6);
        animation: pulse 2s infinite;
        flex-shrink: 0;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(45,212,191, 0.55); }
        70%  { box-shadow: 0 0 0 7px rgba(45,212,191, 0); }
        100% { box-shadow: 0 0 0 0 rgba(45,212,191, 0); }
    }
    .badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
    .badge-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        color: #A6AEC2;
        white-space: nowrap;
    }
    .badge-pill b { color: var(--text-color); font-weight: 600; }

    /* ---------------- SIDEBAR ---------------- */
    .sidebar-heading {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6B7385;
        margin: 6px 0 12px 0;
    }
    .status-card {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 12px;
        margin-bottom: 8px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        font-size: 0.85rem;
    }
    .status-card .dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #2DD4BF;
        flex-shrink: 0;
    }
    .status-card .label {
        color: #6B7385;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: block;
    }
    .status-card .value {
        color: var(--text-color);
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* ---------------- AGENT SETTINGS ---------------- */
    .settings-card {
        # padding: 12px 14px;
        margin-bottom: 6px;
        margin-top: -15px;
        background: rgba(255,255,255,0.03);
        border: 0.5px solid rgba(255,255,255,0.08);
    }
    .settings-note {
        font-size: 0.74rem;
        color: #6B7385;
        line-height: 1.4;
        margin-top: 4px;
    }
    div[data-testid="stToggle"] { margin-bottom: 2px; }
    div[data-testid="stToggle"] label p {
        font-size: 0.88rem !important;
        font-weight: 500;
    }

    /* ---------------- TOOL TRACE ---------------- */
    .tool-trace-item {
        border-left: 2px solid #5B8DEF;
        background: rgba(91,141,239,0.08);
        padding: 7px 11px;
        margin-bottom: 6px;
        border-radius: 0 6px 6px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #7FA8F5;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HERO HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="agent-hero">
        <div class="agent-hero-left">
            <div class="agent-icon">🤖</div>
            <div>
                <p class="agent-title">Enterprise AI Agent</p>
                <div class="agent-subtitle"><span class="pulse-dot"></span>Live · Awaiting input</div>
            </div>
        </div>
        <div class="badge-row">
            <span class="badge-pill"><b>Amazon Bedrock</b></span>
            <span class="badge-pill"><b>ReAct</b> Agent</span>
            <span class="badge-pill">Tools <b>Enabled</b></span>
            <span class="badge-pill">Guardrails <b>On</b></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<p class="sidebar-heading">System Status</p>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="status-card">
            <span class="dot"></span>
            <div>
                <span class="label">Backend</span>
                <span class="value">Python</span>
            </div>
        </div>
        <div class="status-card">
            <span class="dot"></span>
            <div>
                <span class="label">LLM</span>
                <span class="value">Amazon Bedrock</span>
            </div>
        </div>
        <div class="status-card">
            <span class="dot"></span>
            <div>
                <span class="label">UI</span>
                <span class="value">Streamlit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown('<p class="sidebar-heading">Agent Settings</p>', unsafe_allow_html=True)

    # st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    use_knowledge_base = st.toggle(
        "📚 Access Knowledge Base",
        value=False,
        help="When enabled, answers will use information retrieved from the enterprise Knowledge Base."
    )
    st.markdown(
        '<p class="settings-note">Pulls grounded context from the enterprise Knowledge Base before responding.</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    kb_dot_color = "#2DD4BF" if use_knowledge_base else "#4A5268"
    kb_status_text = "Connected" if use_knowledge_base else "Not in use"
    st.markdown(
        f"""
        <div class="status-card">
            <span class="dot" style="background:{kb_dot_color};"></span>
            <div>
                <span class="label">Knowledge Base</span>
                <span class="value">{kb_status_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown('<p class="sidebar-heading">Session</p>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="status-card">
            <span class="dot" style="background:#5B8DEF;"></span>
            <div>
                <span class="label">Messages</span>
                <span class="value">{len(st.session_state.messages)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🗑️  Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------
for message in (
    st.session_state.messages
):
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(
            message["content"]
        )

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
user_message = st.chat_input(
    "Ask me anything..."
)
if user_message:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(
            user_message
        )
    # Convert UI history to Bedrock format
    history = []
    for message in (
        st.session_state.messages[:-1]
    ):
        history.append(
            {
                "role": message["role"],
                "content": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(
            "Thinking..."
        ):
            result = chat(
                user_message=user_message,
                use_knowledge_base=use_knowledge_base,
                history=history
            )
        if result["success"]:
            response = result[
                "response"
            ]
            st.markdown(
                response
            )
            citations = result.get(
                "citations",
                []
            )
            if citations:
                with st.expander(
                    "📚 Sources"
                ):
                    for citation in citations:

                        rank = citation.get(
                            "rank"
                        )

                        score = citation.get(
                            "score"
                        )

                        location = citation.get(
                            "location",
                            {}
                        )

                        metadata = citation.get(
                            "metadata",
                            {}
                        )

                        st.markdown(
                            f"**Source {rank}**"
                        )

                        if score is not None:
                            st.caption(
                                f"Relevance score: {score:.4f}"
                            )

                        if location:
                            st.json(location)

                        if metadata:
                            st.json(metadata)
        else:
            response = result[
                "response"
            ]
            st.error(
                response
            )
        # Debug information
        if result.get(
            "tool_calls"
        ):
            with st.expander(
                "🔧 Tool activity"
            ):
                for call in result[
                    "tool_calls"
                ]:
                    st.markdown(
                        f'<div class="tool-trace-item">▸ {call["tool"]}</div>',
                        unsafe_allow_html=True
                    )
                    st.json(
                        call["input"]
                    )
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )