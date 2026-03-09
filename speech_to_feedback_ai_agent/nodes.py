import os
import tempfile

import numpy as np
import sounddevice as sd
from config import GLOBAL_WHISPER_MODEL, AppConfig
from schemas import Agentstate
from scipy.io.wavfile import write


def run_intial_configuration(state: Agentstate) -> Agentstate:
    pass

def run_ask_question(state: Agentstate) -> Agentstate:
    pass

def run_record_and_transcribe_answer():
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

