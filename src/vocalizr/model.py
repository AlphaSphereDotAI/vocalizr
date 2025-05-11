from datetime import datetime
from os import makedirs

from gradio import Error
from loguru import logger
from numpy import ndarray
from soundfile import write
from torch import Tensor

from vocalizr import BASE_DIR, CHAR_LIMIT, PIPELINE


def save_file_wav(audio: ndarray) -> None:
    """Save audio data to a WAV file in the 'results' directory.

    Creates a timestamped WAV file in the 'results' directory with
    the provided audio data at a fixed sample rate of 24,000 Hz.

    :param audio: Data to save.
    :return: None
    :raise OSError: If an error occurs while saving the file.
    """
    makedirs(name="results", exist_ok=True)
    filename: str = (
        f"{BASE_DIR}/results/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"
    )
    try:
        logger.info(f"Saving audio to {filename}")
        write(file=filename, data=audio, samplerate=24000)
    except OSError as e:
        raise OSError(f"Failed to save audio to {filename}: {e}") from e


def generate_audio_for_text(
    text: str, voice: str = "af_heart", speed: float = 1, save_file: bool = False
) -> tuple[int, ndarray]:
    """Generate audio for the input text.

    :param text:  Input text to convert to speech
    :param voice: Voice identifier
    :param speed: Speech speed multiplier
    :param save_file: If to save the audio file to disk.
    :return: Tuple containing the audio sample rate and raw audio data.
    :raise Error: If an error occurs during generation.
    """
    text = text if CHAR_LIMIT is None else text.strip()[:CHAR_LIMIT]
    try:
        for _, _, audio in PIPELINE(text, voice, speed):
            audio = Tensor(audio).numpy()
            if save_file:
                save_file_wav(audio=audio)
            return 24000, audio
    except Error as e:
        raise Error(message=str(e)) from e
    raise RuntimeError("No audio generated")
