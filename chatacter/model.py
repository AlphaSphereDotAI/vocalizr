import time
from typing import Any, Literal

import torch
from chatacter.settings import Settings, get_settings
from pydantic import StrictStr
from scipy.io.wavfile import write
from transformers import AutoModel, AutoProcessor, logging

settings: Settings = get_settings()

device: Literal["cuda"] | Literal["cpu"] = (
    "cuda" if torch.cuda.is_available() else "cpu"
)
processor: Any = AutoProcessor.from_pretrained(
    pretrained_model_name_or_path=settings.bark.name
)
model: Any = AutoModel.from_pretrained(
    pretrained_model_name_or_path=settings.bark.name, torch_dtype=torch.float16
).to(device)
model: Any = model.to_bettertransformer()
model.enable_cpu_offload()
logging.set_verbosity_debug()


def generate_audio(response: StrictStr) -> dict[str, str | Any | float]:
    print("Device available: ", model.device)
    start_time: float = time.time()
    inputs: Any = processor(
        text=[response], return_tensors="pt", voice_preset="v2/en_speaker_6"
    )
    inputs: Any = inputs.to(device)
    audio: Any = model.generate(**inputs)
    audio: Any = audio.cpu().squeeze(0).numpy()
    sample_rate: Any = model.generation_config.sample_rate
    write(
        filename=f"{settings.assets.audio}AUDIO.wav",
        rate=sample_rate,
        data=audio.astype("float32"),
    )
    end_time: float = time.time()
    return {
        "audio_dir": settings.assets.audio,
        "rate": model.generation_config.sample_rate,
        "text": response,
        "status": "ok",
        "time": end_time - start_time,
    }
