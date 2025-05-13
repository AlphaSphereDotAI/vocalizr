from typing import Any, Generator, Literal

from gradio import Error
from kokoro import KPipeline
from loguru import logger
from numpy import float32
from numpy.typing import NDArray
from soundfile import write

from vocalizr import AUDIO_FILE_PATH, CHAR_LIMIT, PIPELINE


@logger.catch
def save_file_wav(audio: NDArray[float32]) -> None:
    """Save audio data to a WAV file in the 'results' directory.
    Creates a timestamped WAV file in the 'results' directory with
    the provided audio data at a fixed sample rate of 24,000 Hz.

    Args:
        audio (NDArray[float32]): raw audio data.

    Raises:
        RuntimeError: If there are problems with saving the audio file locally.
    """
    try:
        logger.info(f"Saving audio to {AUDIO_FILE_PATH}")
        write(file=AUDIO_FILE_PATH, data=audio, samplerate=24000)
    except Exception as e:
        logger.exception(f"Failed to save audio to {AUDIO_FILE_PATH}: {e}")
        raise RuntimeError(f"Failed to save audio to {AUDIO_FILE_PATH}: {e}") from e


# noinspection PyTypeChecker
@logger.catch
def generate_audio_for_text(
    text: str,
    voice: str = "af_heart",
    speed: float = 1,
    save_file: bool = False,
) -> Generator[tuple[Literal[24000], NDArray[float32]], Any, None]:
    """Generate audio for the input text.

    Args:
        text (str): Input text to convert to speech
        voice (str, optional): Voice identifier. Defaults to "af_heart".
        speed (float, optional): Speech speed. Defaults to 1.
        save_file (bool, optional): If to save the audio file to disk. Defaults to False.

    Raises:
        Error: If text (str) is empty
        Error: If audio (NDArray[float32]) is str
        Error: If audio (NDArray[float32]) is None

    Yields:
        Generator[tuple[Literal[24000], NDArray[float32]], Any, None]: Tuple containing the audio sample rate and raw audio data.
    """
    try:
        text = text if CHAR_LIMIT == -1 else text.strip()[:CHAR_LIMIT]
    except Exception as e:
        logger.exception(str(object=e))
        raise Error(message=str(object=e)) from e
    generator: Generator[KPipeline.Result, None, None] = PIPELINE(
        text=text, voice=voice, speed=speed
    )
    logger.info(f"Generating audio for '{text}'")
    for _, _, audio in generator:
        if audio is None or isinstance(audio, str):
            logger.exception(f"Unexpected type (audio): {type(audio)}")
            raise Error(message=f"Unexpected type (audio): {type(audio)}")
        audio_np: NDArray[float32] = audio.numpy()
        if save_file:
            save_file_wav(audio=audio_np)
            logger.info(f"Yielding audio for '{text}'")
        yield 24000, audio_np
