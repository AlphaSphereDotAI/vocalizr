"""
Core constants and environment checks for the Voice Generator package.

Keeping this module tiny avoids pulling heavy dependencies into processes
that only need the shared constants (e.g. docs builders, CI linters).
"""

import os
import random
import gradio as gr
import torch
from gradio import Error
from kokoro import KModel, KPipeline

CUDA_AVAILABLE: bool = torch.cuda.is_available()

# Maximum allowed characters for TTS generation (`None` disables the cap).
CHAR_LIMIT: int = 5000

models = {
    gpu: KModel().to("cuda" if gpu else "cpu").eval()
    for gpu in [False] + ([True] if CUDA_AVAILABLE else [])
}
pipelines = {
    lang_code: KPipeline(lang_code=lang_code, model=False) for lang_code in "ab"
}
pipelines["a"].g2p.lexicon.golds["kokoro"] = "kˈOkəɹO"
pipelines["b"].g2p.lexicon.golds["kokoro"] = "kˈQkəɹQ"

__all__: list[str] = ["CUDA_AVAILABLE", "CHAR_LIMIT", "models", "pipelines"]
