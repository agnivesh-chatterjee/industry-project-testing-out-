
import streamlit as st

from chatbot.chatbot_backend import get_ai_response


def render_chatbot_launcher(context):

    # Initialise conversation history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Initialise chatbot visibility
    if "chatbot_open" not in st.session_state:
        st.session_state.chatbot_open = False

    # Floating button styling
    st.markdown(
        """
        <style>

        div.st-key-open_ai_assistant {
            position: fixed;
            right: 28px;
            bottom: 28px;
            z-index: 999999;
        }

        div.st-key-open_ai_assistant button {
            border-radius: 30px;
            padding: 12px 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Floating launcher button
    if st.button(
        "💬 AI Assistant",
        key="open_ai_assistant",
        type="primary"
    ):

        st.session_state.chatbot_open = (
            not st.session_state.chatbot_open
        )

    # Display chatbot dialog
    if st.session_state.chatbot_open:

        @st.dialog("AI Assistant", width="large")
        def chat_window():

            st.caption(
                "Ask me anything about the Retirement Expenditure Simulator."
            )

            # Clear conversation
            col1, col2 = st.columns([5, 1])

            with col2:
                if st.button("Clear chat"):
                    st.session_state.chat_messages = []
                    st.rerun()

            # Display conversation history
            for message in st.session_state.chat_messages:

                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input
            user_input = st.chat_input(
                "Ask something..."
            )

            if user_input:

                # Save user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })

                # Generate response
                with st.spinner("Thinking..."):

                    try:

                        answer = get_ai_response(
                            context,
                            st.session_state.chat_messages
                        )

                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as e:

                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"Sorry, something went wrong: {e}"
                        })

                st.rerun()

        chat_window()
