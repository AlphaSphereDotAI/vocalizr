"""Tests for the app's HTTP endpoints."""

from os import getenv
from pathlib import Path

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
        text="Hello world",
        api_name="/generate_audio_for_text",
    )
    assert Path(result).is_file()
