from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from kokoro import KPipeline
from loguru import logger
from torch import cuda

load_dotenv()

BASE_DIR: Path = Path(__file__).parent.parent.parent
DEBUG: bool = getenv(key="DEBUG", default="False").lower() == "true"
CHAR_LIMIT: int = int(getenv(key="CHAR_LIMIT", default="5000"))
SERVER_NAME: str = getenv(key="GRADIO_SERVER_NAME", default="localhost")
SERVER_PORT: int = int(getenv(key="GRADIO_SERVER_PORT", default="8080"))
PIPELINE: KPipeline = KPipeline(lang_code="a",repo_id="hexgrad/Kokoro-82M")
CUDA_AVAILABLE: bool = cuda.is_available()

logger.info(f"CUDA Available: {CUDA_AVAILABLE}")

CHOICES: dict[str, str] = {
    "🇺🇸 🚺 Heart ❤️": "af_heart",
    "🇺🇸 🚺 Bella 🔥": "af_bella",
    "🇺🇸 🚺 Nicole 🎧": "af_nicole",
    "🇺🇸 🚺 Aoede": "af_aoede",
    "🇺🇸 🚺 Kore": "af_kore",
    "🇺🇸 🚺 Sarah": "af_sarah",
    "🇺🇸 🚺 Nova": "af_nova",
    "🇺🇸 🚺 Sky": "af_sky",
    "🇺🇸 🚺 Alloy": "af_alloy",
    "🇺🇸 🚺 Jessica": "af_jessica",
    "🇺🇸 🚺 River": "af_river",
    "🇺🇸 🚹 Michael": "am_michael",
    "🇺🇸 🚹 Fenrir": "am_fenrir",
    "🇺🇸 🚹 Puck": "am_puck",
    "🇺🇸 🚹 Echo": "am_echo",
    "🇺🇸 🚹 Eric": "am_eric",
    "🇺🇸 🚹 Liam": "am_liam",
    "🇺🇸 🚹 Onyx": "am_onyx",
    "🇺🇸 🚹 Santa": "am_santa",
    "🇺🇸 🚹 Adam": "am_adam",
    "🇬🇧 🚺 Emma": "bf_emma",
    "🇬🇧 🚺 Isabella": "bf_isabella",
    "🇬🇧 🚺 Alice": "bf_alice",
    "🇬🇧 🚺 Lily": "bf_lily",
    "🇬🇧 🚹 George": "bm_george",
    "🇬🇧 🚹 Fable": "bm_fable",
    "🇬🇧 🚹 Lewis": "bm_lewis",
    "🇬🇧 🚹 Daniel": "bm_daniel",
}
