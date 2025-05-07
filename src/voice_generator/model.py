"""
Voice generation model functions.
This module provides the core functionality for text-to-speech generation,
including token generation, audio synthesis, and streaming capabilities.
"""

from random import choice
from gradio import Error
from numpy import ndarray
from voice_generator import CHAR_LIMIT, PIPELINE, random_quotes

def generate(text: str, voice="af_heart", speed=1) -> tuple[int, ndarray]:
    """Generate audio for the input text.
     
    :param text:  Input text to convert to speech
    :param voice: Voice identifier
    :param speed: Speech speed multiplier
    :return: tuple containing the audio sample rate and raw audio data.
    """
    text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
    try:
        for _, _, audio in PIPELINE(text, voice, speed):
            audio_numpy: ndarray = audio.numpy()  # pyright: ignore [reportAttributeAccessIssue, reportOptionalMemberAccess]
            return 24000, audio_numpy
    except Error as e:
        raise Error(str(e)) from e
    raise RuntimeError("No audio generated")

# def generate_all(text, voice="af_heart", speed=1, use_gpu=CUDA_AVAILABLE):
#     text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
#     pipeline: KPipeline = pipelines[voice[0]]
#     pack = pipeline.load_voice(voice)
#     use_gpu = use_gpu and CUDA_AVAILABLE
#     first = True
#     for _, phonemes, _ in pipeline(text, voice, speed):
#         ref_s = pack[len(phonemes) - 1]
#         try:
#             if use_gpu:
#                 audio = forward_gpu(phonemes, ref_s, speed).cpu()
#             else:
#                 audio = MODELS[False](phonemes, ref_s, speed)
#         except Error as e:
#             if use_gpu:
#                 gr.Warning(str(e))
#                 gr.Info("Switching to CPU")
#                 audio = MODELS[False](phonemes, ref_s, speed).cpu()
#             else:
#                 raise gr.Error(str(e)) from e
#         yield 24000, audio.cpu().numpy()
#         if first:
#             first = False
#             yield 24000, torch.zeros(1).numpy()


def get_random_quote() -> str:
    return choice(random_quotes)


if __name__ == "__main__":
    _, n = generate(text="hi")
    print(n)
    print(type(n))
    print(n.dtype)
