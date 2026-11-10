
import streamlit as st
from google import genai
from chatbot.system_prompt import get_system_prompt


def get_ai_response(context, messages):
    try:
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        system_prompt = get_system_prompt(context)

        # Convert conversation history into Gemini format
        conversation = []

        for message in messages:
            role = "user" if message["role"] == "user" else "model"

            conversation.append({
                "role": role,
                "parts": [{"text": message["content"]}]
            })

        response = client.models.generate_content(
            model=st.secrets.get(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            ),
            contents=conversation,
            config={
                "system_instruction": system_prompt,
                "temperature": 0.7,
            }
        )

        return response.text

    except Exception as e:
        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            raise RuntimeError(
                "Gemini is temporarily experiencing high demand. "
                "Please wait a minute and try again."
            ) from e

        raise RuntimeError(
            f"Gemini response generation failed: {error_message}"
        ) from e