from pathlib import Path
from time import time
from typing import Literal

from gradio import (
    Audio,
    Blocks,
    Button,
    Checkbox,
    Column,
    Dropdown,
    Error,
    Group,
    Image,
    Info,
    Markdown,
    Number,
    Row,
    Slider,
    Tab,
    Video,
)
from huggingface_hub import snapshot_download
from librosa import load as librosa_load
from numpy import (
    array as np_array,
    hstack as np_hstack,
    ndarray,
    pad as np_pad,
    squeeze as np_squeeze,
)
from python_speech_features import delta, mfcc
from torch import (
    Tensor,
    cat as torch_cat,
    clamp as torch_clamp,
    no_grad,
    randn as torch_randn,
    zeros as torch_zeros,
)
from tqdm import tqdm
from transformers import HubertModel, Wav2Vec2FeatureExtractor
from vocalizr.app.logger import logger
from vocalizr.app.settings import Settings
from dotenv import load_dotenv
from kokoro import KPipeline
from loguru import logger
from torch import cuda
from typing import Any, Generator, Literal

from gradio import Error
from kokoro import KPipeline
from loguru import logger
from numpy import dtype, float32, ndarray
from soundfile import write
from torch import zeros
from gradio import (
    Audio,
    Blocks,
    Button,
    Checkbox,
    Column,
    Dropdown,
    Number,
    Row,
    Slider,
    Textbox,
)

from vocalizr import CHOICES, CUDA_AVAILABLE, DEBUG
from vocalizr.model import generate_audio_for_text


from vocalizr import AUDIO_FILE_PATH, PIPELINE


class App:
    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        logger.info("Downloading model checkpoint")
        self.pipeline = KPipeline(
            lang_code=self.settings.model.lang_code, repo_id=self.settings.model.repo_id
        )

    def generate_audio_for_text(
        self,
        text: str,
        voice: str = "af_heart",
        speed: float = 1.0,
        save_file: bool = False,
        debug: bool = False,
    ) -> Generator[
        tuple[Literal[24000], ndarray[tuple[float32], dtype[float32]]]
        | tuple[int, ndarray],
        Any,
        None,
    ]:
        """
        Generates audio from the provided text using the specified voice and speed.
        It allows saving the generated audio to a file if required. The function
        yields tuples containing the audio sampling rate and the audio data as a
        NumPy array.

        :param str text: The input text to generate audio for. If CHAR_LIMIT is set to a
            positive value, the text will be truncated to fit that limit.

        :param str voice: The voice profile to use for audio generation.
            Defaults to "af_heart".

        :param float speed: The speed modifier for audio generation. Defaults to 1.0.

        :param bool save_file: Whether to save the generated audio to a file. Defaults
            to False.

        :param bool debug: Whether to enable debug mode. Defaults to False.

        :param int char_limit: The maximum number of characters to include in the input

        :return: A generator that yields tuples, where the first element is the
            fixed sampling rate of 24,000 Hz, and the second element is a NumPy
            array representing the generated audio data.
        :rtype: Generator[tuple[Literal[24000], NDArray[float32]], Any, None]
        """
        if not text:
            logger.exception("No text provided")
        elif len(text) < 4:
            logger.exception(f"Text too short: {text} with length {len(text)}")
        text:str = (
            text
            if self.settings.model.char_limit == -1
            else text.strip()[: self.settings.model.char_limit]
        )
        generator: Generator[KPipeline.Result, None, None] = PIPELINE(
            text=text, voice=voice, speed=speed
        )
        first = True
        for _, _, audio in generator:
            if audio is None or isinstance(audio, str):
                logger.exception(f"Unexpected type (audio): {type(audio)}")
                raise Error(message=f"Unexpected type (audio): {type(audio)}")
            if debug:
                logger.info(f"Generating audio for '{text}'")
            audio_np: ndarray[tuple[float32], dtype[float32]] = audio.numpy()
            if save_file:
                if debug:
                    logger.info(f"Saving audio file at {AUDIO_FILE_PATH}")
                self._save_file_wav(audio=audio_np)
            yield 24000, audio_np
            if first:
                first = False
                yield 24000, zeros(1).numpy()

    def gui(self) -> Blocks:
        """Create the Gradio interface for the voice generation web app."""
        with Blocks() as app:
            with Row():
                with Column():
                    text: Textbox = Textbox(
                        label="Input Text", info="Enter your text here"
                    )
                    with Row():
                        voice: Dropdown = Dropdown(
                            choices=list(CHOICES.items()),
                            value="af_heart",
                            label="Voice",
                            info="Quality and availability vary by language",
                        )
                        Dropdown(
                            choices=[("GPU 🚀", True), ("CPU 🐌", False)],
                            value=CUDA_AVAILABLE,
                            label="Current Hardware",
                            interactive=CUDA_AVAILABLE,
                        )
                        char_limit: Number = Number(label="Character Limit", value=-1)
                    with Row():
                        save_file: Checkbox = Checkbox(label="Save Audio File")
                        debug: Checkbox = Checkbox(value=DEBUG, label="Debug")
                    speed: Slider = Slider(
                        minimum=0.5,
                        maximum=2,
                        value=1,
                        step=0.1,
                        label="Speed",
                    )
                with Column():
                    out_audio: Audio = Audio(
                        label="Output Audio",
                        interactive=False,
                        streaming=True,
                        autoplay=True,
                    )
                    with Row():
                        stream_btn: Button = Button(value="Generate", variant="primary")
                        stop_btn: Button = Button(value="Stop", variant="stop")
            stream_event = stream_btn.click(
                fn=generate_audio_for_text,
                inputs=[text, voice, speed, save_file, debug, char_limit],
                outputs=[out_audio],
            )
            stop_btn.click(fn=None, cancels=stream_event)
            return app

    def _save_file_wav(audio: ndarray[tuple[float32], dtype[float32]]) -> None:
        """
        Saves an audio array to a WAV file using the specified sampling rate. If the saving
        operation fails, it logs the exception and raises a RuntimeError.

        :param ndarray[tuple[float32],dtype[float32]] audio: The audio data to be saved.
            Must be a NumPy array of data type float32, representing the audio signal
            to be written to the file.

        :return: This function does not return a value.
        :rtype: None
        """
        try:
            logger.info(f"Saving audio to {AUDIO_FILE_PATH}")
            write(file=AUDIO_FILE_PATH, data=audio, samplerate=24000)
        except Exception as e:
            logger.exception(f"Failed to save audio to {AUDIO_FILE_PATH}: {e}")
            raise RuntimeError(f"Failed to save audio to {AUDIO_FILE_PATH}: {e}") from e
