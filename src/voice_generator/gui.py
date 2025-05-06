import gradio as gr
from voice_generator import (
    CUDA_AVAILABLE,
    CHAR_LIMIT,
    STREAM_NOTE,
    TOKEN_NOTE,
    CHOICES,
)
from gradio import Blocks, Audio, Button, Textbox, Dropdown, Slider
from voice_generator.model import (
    generate_first,
    get_random_quote,
    tokenize_first,
    predict,
    generate_all,
)


def generate_tab_block() -> tuple[Blocks, Audio, Button, Textbox, Button, Button]:
    with gr.Blocks() as generate_tab:
        out_audio: Audio = gr.Audio(
            label="Output Audio", interactive=False, streaming=False, autoplay=True
        )
        generate_btn: Button = gr.Button("Generate", variant="primary")
        with gr.Accordion("Output Tokens", open=True):
            out_ps: Textbox = gr.Textbox(
                interactive=False,
                show_label=False,
                info="Tokens used to generate the audio, up to 510 context length.",
            )
            tokenize_btn: Button = gr.Button("Tokenize", variant="secondary")
            gr.Markdown(TOKEN_NOTE)
            predict_btn: Button = gr.Button(
                "Predict", variant="secondary", visible=False
            )
    return generate_tab, out_audio, generate_btn, out_ps, tokenize_btn, predict_btn


def stream_tab_block() -> tuple[Blocks, Audio, Button, Button]:
    with gr.Blocks() as stream_tab:
        out_stream: Audio = gr.Audio(
            label="Output Audio Stream",
            interactive=False,
            streaming=True,
            autoplay=True,
        )
        with gr.Row():
            stream_btn: Button = gr.Button("Stream", variant="primary")
            stop_btn: Button = gr.Button("Stop", variant="stop")
        with gr.Accordion("Note", open=True):
            gr.Markdown(STREAM_NOTE)
            gr.DuplicateButton()
        return stream_tab, out_stream, stream_btn, stop_btn


def app_block() -> gr.Blocks:
    """Create and return the main application interface.

    Assembles both Generate and Stream tabs into a complete UI with shared input controls.
    Connects UI components to their respective backend functions.

    Returns:
        gr.Blocks: The complete Gradio application interface
    """
    generate_tab, out_audio, generate_btn, out_ps, tokenize_btn, predict_btn = (
        generate_tab_block()
    )
    stream_tab, out_stream, stream_btn, stop_btn = stream_tab_block()
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column():
                text: Textbox = gr.Textbox(
                    label="Input Text",
                    info=(
                        f"Up to ~500 characters per Generate, or "
                        f"{'∞' if CHAR_LIMIT is None else CHAR_LIMIT} characters per Stream"
                    ),
                )
                with gr.Row():
                    voice: Dropdown = gr.Dropdown(
                        list(CHOICES.items()),
                        value="af_heart",
                        label="Voice",
                        info="Quality and availability vary by language",
                    )
                    use_gpu: Dropdown = gr.Dropdown(
                        [("ZeroGPU 🚀", True), ("CPU 🐌", False)],
                        value=CUDA_AVAILABLE,
                        label="Hardware",
                        info="GPU is usually faster, but has a usage quota",
                        interactive=CUDA_AVAILABLE,
                    )
                speed: Slider = gr.Slider(
                    minimum=0.5, maximum=2, value=1, step=0.1, label="Speed"
                )
                random_btn: Button = gr.Button(
                    "🎲 Random Quote 💬", variant="secondary"
                )
            with gr.Column():
                gr.TabbedInterface([generate_tab, stream_tab], ["Generate", "Stream"])
        random_btn.click(fn=get_random_quote, inputs=[], outputs=[text])
        generate_btn.click(
            fn=generate_first,
            inputs=[text, voice, speed, use_gpu],
            outputs=[out_audio, out_ps],
        )
        tokenize_btn.click(fn=tokenize_first, inputs=[text, voice], outputs=[out_ps])
        stream_event = stream_btn.click(
            fn=generate_all, inputs=[text, voice, speed, use_gpu], outputs=[out_stream]
        )
        stop_btn.click(fn=None, cancels=stream_event)
        predict_btn.click(fn=predict, inputs=[text, voice, speed], outputs=[out_audio])
    return app
