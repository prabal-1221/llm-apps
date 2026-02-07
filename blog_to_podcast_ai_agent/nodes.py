import logging
import os

import edge_tts
import trafilatura
from config import CONVERSATION_TEMPLATE, DEFAULT_OUTPUT_PATH, VOICE_CONFIG
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import AgentState, ConversationScript

# Get logger
logger = logging.getLogger(__name__)

async def fetch_blog_content_node(state: AgentState) -> AgentState:
    """Fetches text content from a URL."""
    target_url = state.get("url")

    if not target_url:
        logger.error("Node Execution Failed: 'url' is missing.")
        return {"flg_content": False}

    try:
        logger.info(f"Fetching content from: {target_url}")
        raw_html = trafilatura.fetch_url(url=target_url)

        if raw_html:
            extracted_data = trafilatura.extract(raw_html)
            if extracted_data:
                logger.info("Content extracted successfully.")
                return {"content": extracted_data, "flg_content": True}

        logger.warning("Extraction failed or returned empty.")
        return {"flg_content": False}

    except Exception as e:
        logger.error(f"Error fetching content: {e}", exc_info=True)
        return {"flg_content": False}


async def generate_conversation_script_node(state: AgentState) -> AgentState:
    """Transforms blog content into a dialogue script using Gemini."""
    blog_text = state.get("content", "")

    try:
        logger.info("Generating script with LLM...")
        parser = PydanticOutputParser(pydantic_object=ConversationScript)

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
        )

        prompt = PromptTemplate(
            template=CONVERSATION_TEMPLATE,
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        chain = prompt | llm | parser

        # Limiting text to 20k chars to avoid token limits
        script_output: ConversationScript = await chain.ainvoke({"text": blog_text[:20000]})

        logger.info(f"Script generated with {len(script_output.conversation)} lines.")
        return {"script": script_output, "flg_script": True}

    except Exception as e:
        logger.error(f"Error generating script: {e}", exc_info=True)
        return {"flg_script": False}


async def generate_podcast_audio_node(state: AgentState) -> AgentState:
    """Converts the script to Audio."""
    script_obj = state.get("script")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(DEFAULT_OUTPUT_PATH), exist_ok=True)

    try:
        conversation = script_obj.conversation
        logger.info(f"Starting TTS for {len(conversation)} lines...")

        with open(DEFAULT_OUTPUT_PATH, "wb") as audio_file:
            for turn in conversation:
                speaker = turn.speaker
                message = turn.message

                voice = VOICE_CONFIG.get(speaker, VOICE_CONFIG["Host"])

                if not message:
                    continue

                communicate = edge_tts.Communicate(message, voice)
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_file.write(chunk["data"])

        logger.info(f"Podcast saved to: {DEFAULT_OUTPUT_PATH}")

    except Exception as e:
        logger.error(f"Failed to generate audio: {e}", exc_info=True)
        if os.path.exists(DEFAULT_OUTPUT_PATH):
            os.remove(DEFAULT_OUTPUT_PATH)

    return state

# --- Conditional Logic ---

def check_contents(state: AgentState) -> bool:
    return state["flg_content"]

def check_script(state: AgentState) -> bool:
    return state["flg_script"]
