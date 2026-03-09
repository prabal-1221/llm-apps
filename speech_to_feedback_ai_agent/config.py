import os
import sys

import nvidia.cublas
import nvidia.cudnn
from dotenv import load_dotenv
from faster_whisper import WhisperModel

# 1. Path Discovery
cublas_lib_path = os.path.join(nvidia.cublas.__path__[0], "lib")
cudnn_lib_path = os.path.join(nvidia.cudnn.__path__[0], "lib")
target_path = f"{cublas_lib_path}:{cudnn_lib_path}"

# 2. The "Self-Restart" Logic
# Check if our custom paths are already in the system's search list
current_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
if target_path not in current_ld_path:
    os.environ["LD_LIBRARY_PATH"] = f"{target_path}:{current_ld_path}"
    print("--- Configuring GPU environment and restarting... ---")
    # This replaces the current process with a new one that HAS the variable set
    os.execv(sys.executable, [sys.executable, *sys.argv])

load_dotenv()

class AppConfig:
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")
    DEVICE = os.getenv("WHISPER_DEVICE", "cuda")
    COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "float16")
    FS = 16000
    RECORD_SECONDS = 5

print(f"--- Loading Whisper ({AppConfig.MODEL_SIZE}) to {AppConfig.DEVICE}... ---")
GLOBAL_WHISPER_MODEL = WhisperModel(
    AppConfig.MODEL_SIZE,
    device=AppConfig.DEVICE,
    compute_type=AppConfig.COMPUTE_TYPE
)
