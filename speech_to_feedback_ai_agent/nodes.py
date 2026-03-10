import os
import tempfile

import numpy as np
import sounddevice as sd
from config import GLOBAL_WHISPER_MODEL, AppConfig
from schemas import AgentState
from scipy.io.wavfile import write


def run_initialize_session(state: AgentState) -> AgentState:
    """Sets up the initial environment and state variables."""
    return state

def run_check_system_readiness(state: AgentState) -> str:
    """Validates hardware/API access before starting."""
    questions = state.get("questions")
    if not questions:
        return "failure"

    idx = state.get("idx")
    if idx != 0:
        return "failure"

    return "success"

def run_deliver_question(state: AgentState) -> AgentState:
    """Triggers the AI to ask the current question."""
    idx = state.get("idx")
    questions = state.get("questions")

    print("-"*100)
    print("-"*46 + "QUESTION" + "-"*46)
    print(questions[idx])
    print("-"*100)

    return state

def run_capture_and_process_response(state: AgentState) -> AgentState:
    """Handles audio recording and speech-to-text conversion."""
    return state
    print(f"--- Listening for {AppConfig.RECORD_SECONDS}s ---")

    recording = sd.rec(
        int(AppConfig.RECORD_SECONDS * AppConfig.FS),
        samplerate=AppConfig.FS,
        channels=1
    )
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_data = (recording* 32767).astype(np.int16)
        write(tmp.name, AppConfig.FS, audio_data)
        tmp_path = tmp.name

    print("--- Transcribing... ---")
    segments, _ = GLOBAL_WHISPER_MODEL.transcribe(tmp_path, beam_size=5)
    full_text = "".join([s.text for s in segments])

    os.remove(tmp_path)
    return full_text.strip()

def run_decide_next_step(state: AgentState) -> str:
    """Determines if more questions remain or if the session is complete."""
    pass
