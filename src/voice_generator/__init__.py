from kokoro import KModel, KPipeline
from torch import cuda
from pathlib import Path

BASE_DIR: Path = Path(__file__).parent

CUDA_AVAILABLE: bool = cuda.is_available()
CHAR_LIMIT: int = 5000

MODELS: dict[bool, KModel] = {
    gpu: KModel().to("cuda" if gpu else "cpu").eval()
    for gpu in [False] + ([True] if CUDA_AVAILABLE else [])
}
pipelines: dict[str, KPipeline] = {
    lang_code: KPipeline(lang_code=lang_code, model=False) for lang_code in "ab"
}
pipelines["a"].g2p.lexicon.golds["kokoro"] = "kˈOkəɹO"
pipelines["b"].g2p.lexicon.golds["kokoro"] = "kˈQkəɹQ"

try:
    with open(BASE_DIR / "en.txt", "r", encoding="utf-8") as r:
        random_quotes: list[str] = [line.strip() for line in r]
except FileNotFoundError:
    print(f"Missing required text file: {BASE_DIR / 'en.txt'}")

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

for v in CHOICES.values():
    try:
        pipelines[v[0]].load_voice(v)
    except Exception as e:  # pylint: disable=broad-except
        import warnings

        warnings.warn(f"Failed to preload voice {v}: {e}")

TOKEN_NOTE = """
💡 Customize pronunciation with Markdown link syntax and /slashes/ like `[Kokoro](/kˈOkəɹO/)`

💬 To adjust intonation, try punctuation `;:,.!?—…"()""` or stress `ˈ` and `ˌ`

⬇️ Lower stress `[1 level](-1)` or `[2 levels](-2)`

⬆️ Raise stress 1 level `[or](+2)` 2 levels (only works on less stressed, usually short words)
"""

_STREAM_NOTE: list[str] = [
    "⚠️ There is an unknown Gradio bug that might yield no audio the first time you click `Stream`."
]
if CHAR_LIMIT is not None:
    _STREAM_NOTE.append(f"✂️ Each stream is capped at {CHAR_LIMIT} characters.")
    _STREAM_NOTE.append(
        "🚀 Want more characters? You can [use Kokoro directly](https://huggingface.co/hexgrad/Kokoro-82M#usage) or duplicate this space:"
    )
STREAM_NOTE: str = "\n\n".join(_STREAM_NOTE)
