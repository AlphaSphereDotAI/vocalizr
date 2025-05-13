from gradio import (
    Audio,
    Blocks,
    Button,
    Checkbox,
    Column,
    Dropdown,
    Row,
    Slider,
    Textbox,
)
from gradio.events import Dependency

from vocalizr import CHOICES, CUDA_AVAILABLE
from vocalizr.model import generate_audio_for_text


def app_block() -> Blocks:
    """Create and return the main application interface.

    :return: Blocks: The complete Gradio application interface
    """
    with Blocks() as app:
        with Row():
            with Column():
                text: Textbox = Textbox(
                    label="Input Text",
                    info=("""Enter your text here"""),
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
                        label="Hardware",
                        info="GPU is usually faster, but has a usage quota",
                        interactive=CUDA_AVAILABLE,
                    )
                    save_file = Checkbox(
                        label="Save Audio",
                        info="Save audio to local storage",
                    )
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
                    stream_btn: Button = Button(
                        value="Generate",
                        variant="primary",
                    )
                    stop_btn = Button(
                        value="Stop",
                        variant="stop",
                    )
        stream_event: Dependency = stream_btn.click(
            fn=generate_audio_for_text,
            inputs=[text, voice, speed, save_file],
            outputs=[out_audio],
        )
        stop_btn.click(fn=None, cancels=stream_event)
    return app
