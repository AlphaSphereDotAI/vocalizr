from gradio import Error
from numpy import ndarray
from soundfile import write
from torch import Tensor
from voice_generator import CHAR_LIMIT, PIPELINE, BASE_DIR
from datetime import datetime
from loguru import logger
from os import makedirs


def save_file_wav(audio: ndarray) -> None:
    makedirs(name='results',exist_ok=True)
    filename = f"{BASE_DIR}/results/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"
    try:
        logger.info(f"Saving audio to {filename}")
        write(filename, audio, 24000)
    except OSError as e:
        raise OSError(f"Failed to save audio to {filename}: {e}") from e


def generate(
    text: str, voice="af_heart", speed=1, save_file: bool = False
) -> tuple[int, ndarray]:
    """Generate audio for the input text.

    :param text:  Input text to convert to speech
    :param voice: Voice identifier
    :param speed: Speech speed multiplier
    :param save_file: If to save the audio file to disk.
    :return: Tuple containing the audio sample rate and raw audio data.
    """
    text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
    try:
        for _, _, audio in PIPELINE(text, voice, speed):
            audio = Tensor(audio).numpy()
            if save_file:
                save_file_wav(audio)
            return 24000, audio
    except Error as e:
        raise Error(str(e)) from e
    raise RuntimeError("No audio generated")
