import asyncio
import os

import streamlit as st
from config import DEFAULT_OUTPUT_PATH
from graph import build_graph

# Page Config
st.set_page_config(
    page_title="Blog to Podcast Agent",
    page_icon="🎙️",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎙️ AI Blog to Podcast Converter")
st.markdown("Turn any blog post into an engaging 2-person podcast conversation.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info("Currently using default voices:\n- Host: Guy (US)\n- Guest: Aria (US)")

# --- 1. Session State Initialization ---
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False

# Input Section
url_input = st.text_input("Enter Blog URL:", placeholder="https://example.com/amazing-article")

# --- 2. Generate Logic ---
if st.button("Generate Podcast", type="primary"):
    if not url_input:
        st.error("Please enter a valid URL.")
    else:
        # Reset state in case we are generating a new one
        st.session_state.processing_complete = False

        # Initialize graph
        podcast_generator = build_graph()
        inputs = {
            "url": url_input,
            "content": None,
            "flg_content": False,
            "script": None,
            "flg_script": False
        }

        # Status Container
        status_container = st.status("🚀 Starting Agent...", expanded=True)

        async def run_agent():
            try:
                async for event in podcast_generator.astream(inputs):
                    if "get_contents" in event:
                        status_container.write("✅ **Fetched Content**: Blog text extracted successfully.")
                        status_container.update(label="✍️ Writing Script...")
                    elif "get_script" in event:
                        status_container.write("✅ **Script Generated**: Dialogue created.")
                        status_container.update(label="🗣️ Synthesizing Audio...")
                    elif "get_podcast" in event:
                        status_container.write("✅ **Audio Ready**: TTS generation complete.")
                        status_container.update(label="🎉 Process Complete!", state="complete")
                return True
            except Exception as e:
                status_container.update(label="❌ Error Occurred", state="error")
                st.error(f"An error occurred: {e}")
                return False

        # Run the agent
        success = asyncio.run(run_agent())

        if success:
            # Set the flag to True so we remember it happened
            st.session_state.processing_complete = True


# --- 3. Result Display Logic ---
if st.session_state.processing_complete:

    # Check if file exists
    if os.path.exists(DEFAULT_OUTPUT_PATH):
        st.success("Podcast generated successfully!")

        # Read the file
        with open(DEFAULT_OUTPUT_PATH, "rb") as audio_file:
            audio_bytes = audio_file.read()

            # Display Audio Player
            st.audio(audio_bytes, format="audio/mp3")

            # Download Button
            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="podcast.mp3",
                mime="audio/mpeg"
            )
    else:
        st.error("File not found. Please try generating again.")
