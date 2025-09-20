"""Tests for the app's HTTP endpoints."""

from os import getenv

from gradio_client import Client

URL: str = getenv(key="VOCALIZR_URL", default="http://localhost:7860/")


def test_app() -> None:
    """Test the reachability of Vocalizr."""
    client = Client(URL)
    assert client.heartbeat.is_alive()


def test_generate_audio_for_text() -> None:
    """Test HuBERT full-control inference with a face super-resolution."""
    client = Client(URL)
    result = client.predict(
        text="Hello!!",
        voice="af_heart",
        speed=1,
        save_file=False,
        debug=True,
        char_limit=-1,
        api_name="/generate_audio_for_text",
    )
    print(result)
    # assert Path(result[0]["value"]["audio"]).is_file()
    # assert Path(result[1]["value"]["audio"]).is_file()
    # assert result[2]["value"] == "Audio generated successfully!"
