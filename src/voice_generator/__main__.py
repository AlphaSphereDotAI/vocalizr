from gradio import Blocks
from voice_generator import SERVER_NAME, SERVER_PORT, DEBUG
from voice_generator.gui import app_block


def main() -> None:
    """Launch the Gradio voice generation web application."""
    app: Blocks = app_block()
    app.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        debug=DEBUG,
        mcp_server=True,
        show_api=True,
        enable_monitoring=True,
        show_error=True,
    )


if __name__ == "__main__":
    main()
