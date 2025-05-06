import gradio as gr
from gradio import Error
from kokoro import KPipeline
import torch
from voice_generator import CUDA_AVAILABLE, CHAR_LIMIT, MODELS, pipelines, random_quotes
from torch import FloatTensor, Tensor
from typing import Any
import random


def forward_gpu(ps, ref_s, speed) -> Any:
    return MODELS[True](ps, ref_s, speed)


def generate_first(text, voice="af_heart", speed=1, use_gpu=CUDA_AVAILABLE):
    text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
    pipeline: KPipeline = pipelines[voice[0]]
    pack: FloatTensor = pipeline.load_voice(voice)
    use_gpu = use_gpu and CUDA_AVAILABLE
    for _, ps, _ in pipeline(text, voice, speed):
        ref_s: Tensor = pack[len(ps) - 1]
        try:
            if use_gpu:
                audio = forward_gpu(ps, ref_s, speed)
            else:
                audio = MODELS[False](ps, ref_s, speed)
        except Error as e:
            if use_gpu:
                gr.Warning(str(e))
                gr.Info(
                    "Retrying with CPU. To avoid this error, change Hardware to CPU."
                )
                audio = MODELS[False](ps, ref_s, speed)
            else:
                raise Error(e.message) from e
        return (24000, audio.numpy()), ps
    return None, ""


# Arena API
def predict(text, voice="af_heart", speed=1):
    return generate_first(text, voice, speed, use_gpu=False)[0]


def tokenize_first(text, voice="af_heart"):
    pipeline = pipelines[voice[0]]
    for _, ps, _ in pipeline(text, voice):
        return ps
    return ""


def generate_all(text, voice="af_heart", speed=1, use_gpu=CUDA_AVAILABLE):
    text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
    pipeline = pipelines[voice[0]]
    pack = pipeline.load_voice(voice)
    use_gpu = use_gpu and CUDA_AVAILABLE
    first = True
    for _, ps, _ in pipeline(text, voice, speed):
        ref_s = pack[len(ps) - 1]
        try:
            if use_gpu:
                audio = forward_gpu(ps, ref_s, speed)
            else:
                audio = MODELS[False](ps, ref_s, speed)
        except Error as e:
            if use_gpu:
                gr.Warning(e.message)
                gr.Info("Switching to CPU")
                audio = MODELS[False](ps, ref_s, speed)
            else:
                raise gr.Error(e.message)
        yield 24000, audio.numpy()
        if first:
            first = False
            yield 24000, torch.zeros(1).numpy()


def get_random_quote():
    return random.choice(random_quotes)
