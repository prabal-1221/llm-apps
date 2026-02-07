from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Voice settings for Edge TTS
VOICE_CONFIG = {
    "Host": "en-US-GuyNeural",
    "Guest": "en-US-AriaNeural"
}

# Output paths
DEFAULT_OUTPUT_PATH = "blog_to_podcast_ai_agent/outputs/podcast.mp3"

# LLM Templates
CONVERSATION_TEMPLATE = """
You are a professional content writer and dialogue designer.

Task:
Convert the provided blog content into a structured, two-person conversation.

Rules:
- Use ONLY speaker names: "Host" and "Guest".
- Alternate speakers: (Host → Guest → Host → Guest).
- Cover all major concepts and conclusions from the text.
- Do NOT add external information.
- Output MUST be a single, valid JSON object matching the requested schema.

{format_instructions}

Input Text:
{text}
"""
