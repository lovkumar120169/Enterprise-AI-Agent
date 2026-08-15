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
    page_title="Enterprise AI Agent",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Enterprise AI Agent")

st.caption(
    "Amazon Bedrock • ReAct Agent • Tools • Guardrails"
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

    st.header("System")

    st.success(
        "Backend: Python"
    )

    st.success(
        "LLM: Amazon Bedrock"
    )

    st.success(
        "UI: Streamlit"
    )

    st.divider()

    if st.button(
        "Clear conversation",
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

    with st.chat_message(
        message["role"]
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

    with st.chat_message("user"):

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

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            result = chat(
                user_message=user_message,
                history=history
            )

        if result["success"]:

            response = result[
                "response"
            ]

            st.markdown(
                response
            )

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

                    st.write(
                        f"**{call['tool']}**"
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