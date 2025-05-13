from datetime import datetime
from os import makedirs
from typing import Any, Generator, Literal

from gradio import Error
from kokoro import KPipeline
from loguru import logger
from numpy import float32
from numpy.typing import NDArray
from soundfile import write  # type: ignore
from torch import FloatTensor

from vocalizr import BASE_DIR, CHAR_LIMIT, PIPELINE


def save_file_wav(audio: NDArray[float32]) -> None:
    """Save audio data to a WAV file in the 'results' directory.

    Creates a timestamped WAV file in the 'results' directory with
    the provided audio data at a fixed sample rate of 24,000 Hz.
    """
    makedirs(name="results", exist_ok=True)
    current_date: str = datetime.now().strftime(format="%Y-%m-%d_%H-%M-%S")
    filename: str = f"{BASE_DIR}/results/{current_date}.wav"
    try:
        logger.info(f"Saving audio to {filename}")
        write(file=filename, data=audio, samplerate=24000)
    except Exception as e:
        logger.exception(f"Failed to save audio to {filename}: {e}")
        raise RuntimeError(f"Failed to save audio to {filename}: {e}") from e


def generate_audio_for_text(
    text: str,
    voice: str = "af_heart",
    speed: float = 1,
    save_file: bool = False,
) -> Generator[tuple[Literal[24000], NDArray[float32]], Any, None]:
    """Generate audio for the input text.

    :param text:  Input text to convert to speech
    :param voice: Voice identifier
    :param speed: Speech speed multiplier
    :param save_file: If to save the audio file to disk.
    :return: Tuple containing the audio sample rate and raw audio data.
    :raise Error: If an error occurs during generation.
    """
    try:
        text = text if CHAR_LIMIT == -1 else text.strip()[:CHAR_LIMIT]
    except ValueError as e:
        raise Error(message=str(object=e)) from e
    except Exception as e:
        raise Error(message=str(object=e)) from e
    generator: Generator[KPipeline.Result, None, None] = PIPELINE(
        text=text, voice=voice, speed=speed
    )
    logger.info(f"Generating audio for {text}")
    for _, _, audio in generator:
        if isinstance(audio, str):
            logger.exception(f"Unexpected type (audio): {type(audio)}")
            raise Error(message=f"Unexpected type (audio): {type(audio)}")
        elif audio is None:
            logger.exception(f"Unexpected type (audio): {type(audio)}")
            raise Error(message=f"Unexpected type (audio): {type(audio)}")
        audio_np: NDArray[float32] = audio.numpy()
        if save_file:
            save_file_wav(audio=audio_np)
        yield 24000, audio_np
