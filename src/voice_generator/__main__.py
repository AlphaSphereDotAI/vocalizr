from voice_generator.gui import app_block
from voice_generator import DEBUG, ADDRESS, PORT
from gradio import Blocks


def main() -> None:
    """Launch the Gradio voice generation web application.

    Starts a web server with server-side rendering, multi-client processing,
    and debug mode enabled. The server listens on all interfaces on port 8080.
    """
    app: Blocks = app_block()
    app.launch(
        ssr_mode=True,
        mcp_server=True,
        debug=DEBUG,
        show_api=True,
        enable_monitoring=True,
        show_error=True,
        server_name=ADDRESS,
        server_port=PORT,
    )


if __name__ == "__main__":
    main()
