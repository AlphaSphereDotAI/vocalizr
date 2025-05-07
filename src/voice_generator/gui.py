"""
Gradio-based graphical user interface for the voice generation application.

This module defines the UI components and layout for the voice generator, including
text input, voice selection, and audio output. It connects UI elements to backend
functions for generating speech and fetching random quotes.
"""

from gradio import (
    Accordion,
    Audio,
    Blocks,
    Button,
    Column,
    Dropdown,
    Markdown,
    Row,
    Slider,
    TabbedInterface,
    Textbox,
    Checkbox,
)
from voice_generator import CHAR_LIMIT, CHOICES, CUDA_AVAILABLE, STREAM_NOTE
from voice_generator.model import generate, get_random_quote


def generate_tab_block() -> tuple[Blocks, Audio, Button]:
    """Create and return the Generate tab UI components.

    Returns:
        tuple: (generate_tab, out_audio, generate_btn) containing the tab block
        and its interactive components.
    """
    with Blocks() as generate_tab:
        out_audio: Audio = Audio(
            label="Output Audio", interactive=False, streaming=False, autoplay=True
        )
        generate_btn: Button = Button("Generate", variant="primary")
    return generate_tab, out_audio, generate_btn


def stream_tab_block() -> tuple[Blocks, Audio, Button, Button]:
    """Create and return the Stream tab UI components.

    Returns:
        tuple: (stream_tab, out_stream, stream_btn, stop_btn) containing the tab block
        and its interactive components.
    """
    with Blocks() as stream_tab:
        out_stream: Audio = Audio(
            label="Output Audio Stream",
            interactive=False,
            streaming=True,
            autoplay=True,
        )
        with Row():
            stream_btn: Button = Button("Stream", variant="primary")
            stop_btn: Button = Button("Stop", variant="stop")
        with Accordion("Note", open=True):
            Markdown(STREAM_NOTE)
        return stream_tab, out_stream, stream_btn, stop_btn


def app_block() -> Blocks:
    """Create and return the main application interface.

    Assembles both Generate and Stream tabs into a complete UI with shared input controls.
    Connects UI components to their respective backend functions.

    Returns:
        Blocks: The complete Gradio application interface
    """
    generate_tab, out_audio, generate_btn = generate_tab_block()
    stream_tab, out_stream, stream_btn, stop_btn = stream_tab_block()
    with Blocks() as app:
        with Row():
            with Column():
                text: Textbox = Textbox(
                    label="Input Text",
                    info=(
                        f"Up to ~500 characters per Generate, or "
                        f"{'∞' if CHAR_LIMIT is None else CHAR_LIMIT} characters per Stream"
                    ),
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
                        label="Save Audio", info="Save audio to local storage"
                    )
                speed: Slider = Slider(
                    minimum=0.5,
                    maximum=2,
                    value=1,
                    step=0.1,
                    label="Speed",
                )
                random_btn: Button = Button("🎲 Random Quote 💬", variant="secondary")
            with Column():
                TabbedInterface([generate_tab, stream_tab], ["Generate", "Stream"])
        random_btn.click(
            fn=get_random_quote,
            inputs=[],
            outputs=[text],
        )
        generate_btn.click(
            fn=generate,
            inputs=[text, voice, speed, save_file],
            outputs=[out_audio],
        )
        # tokenize_btn.click(
        #     fn=tokenize_first,
        #     inputs=[text, voice],
        #     outputs=[out_ps],
        # )
        # stream_event = stream_btn.click(
        #     fn=generate_all,
        #     inputs=[text, voice, speed, use_gpu],
        #     outputs=[out_stream],
        # )
        # stop_btn.click(
        #     fn=None,
        #     cancels=stream_event,
        # )
    return app
