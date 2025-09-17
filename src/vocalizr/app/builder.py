from pathlib import Path
from typing import Literal
from uuid import uuid4

from gradio import (
    Audio,
    Blocks,
    Button,
    Column,
    Dropdown,
    Error,
    Row,
    Slider,
)
from numpy import ndarray
from vocalizr.app.logger import logger
from vocalizr.app.settings import Settings
from kokoro import KPipeline
from typing import Any, Generator

from numpy import dtype, float32
from soundfile import write
from torch import zeros
from gradio import Textbox


class App:
    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings
        logger.info("Downloading model checkpoint")
        self.pipeline = KPipeline(
            lang_code=self.settings.model.lang_code, repo_id=self.settings.model.repo_id
        )

    def generate_audio_for_text(
        self, text: str, voice: str = "af_heart", speed: float = 1.0
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
            _msg = "No text provided"
            logger.exception(_msg)
            raise ValueError(_msg)
        elif len(text) < 4:
            _msg = f"Text too short: {text} with length {len(text)}"
            logger.exception(_msg)
            raise ValueError(_msg)
        text: str = (
            text
            if self.settings.model.char_limit == -1
            else text.strip()[: self.settings.model.char_limit]
        )
        generator: Generator[KPipeline.Result, None, None] = self.pipeline(
            text=text, voice=voice, speed=speed
        )
        first = True
        for _, _, audio in generator:
            if audio is None or isinstance(audio, str):
                logger.exception(f"Unexpected type (audio): {type(audio)}")
                raise Error(message=f"Unexpected type (audio): {type(audio)}")
            logger.info(f"Generating audio for '{text}'")
            audio_np: ndarray[tuple[float32], dtype[float32]] = audio.numpy()
            logger.info(f"Saving audio file at {self.settings.directory.results}")
            self._save_file_wav(
                audio_np, self.settings.directory.results / f"{uuid4()}.wav"
            )
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
                    voice: Dropdown = Dropdown(
                        choices=list(self.settings.model.choices.__dict__.items()),
                        value="af_heart",
                        label="Voice",
                        info="Quality and availability vary by language",
                    )
                    speed: Slider = Slider(
                        minimum=0.5,
                        maximum=2,
                        value=1,
                        step=0.1,
                        label="Speed",
                    )
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
                fn=self.generate_audio_for_text,
                inputs=[text, voice, speed],
                outputs=[out_audio],
            )
            stop_btn.click(fn=None, cancels=stream_event)
            return app

    def _save_file_wav(
        audio: ndarray[tuple[float32], dtype[float32]], file_result_path: Path
    ) -> None:
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
            logger.info(f"Saving audio to {file_result_path}")
            write(file=file_result_path, data=audio, samplerate=24000)
        except Exception as e:
            logger.exception(f"Failed to save audio to {file_result_path}: {e}")
            raise RuntimeError(
                f"Failed to save audio to {file_result_path}: {e}"
            ) from e
