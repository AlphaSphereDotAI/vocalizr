from gradio import Blocks
from voice_generator.gui import app_block
from os import getenv


def main() -> None:
    """Launch the Gradio voice generation web application."""
    app: Blocks = app_block()
    app.launch(
        server_name=getenv(key="SERVER_NAME", default="0.0.0.0"),
        server_port=int(getenv(key="SERVER_PORT", default="8080")),
        debug=bool(getenv(key="DEBUG", default="0")),
        mcp_server=True,
        show_api=True,
        enable_monitoring=True,
        show_error=True,
    )


if __name__ == "__main__":
    main()
