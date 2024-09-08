import json
import warnings
from typing import Any

from chatacter.model import generate_audio
from chatacter.settings import Settings, get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

warnings.filterwarnings(action="ignore")
global settings
settings: Settings = get_settings()
app = FastAPI(
    debug=True,
    title="Character Voice Generator",
    description="Character Voice Generator API",
)


@app.get(path="/")
async def is_alive() -> JSONResponse:
    return JSONResponse(
        content={
            "message": "Chatacter Voice Generator is alive!",
        },
    )


@app.get(path="/get_settings")
async def get_settings() -> JSONResponse:
    return JSONResponse(
        content=json.loads(s=settings.model_dump_json(indent=4)),
    )


@app.get(path="/get_audio")
def get_audio(text: str) -> FileResponse:
    print("Generating audio for: ", text)
    results: dict[str, str | Any | float] = generate_audio(response=text)
    return FileResponse(
        path=f"{settings.assets.audio}AUDIO.wav",
        media_type="audio/wav",
        filename="AUDIO.wav",
        headers={
            "text": results["text"],
            "time": str(object=results["time"]),
            "rate": str(object=results["rate"]),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        host="localhost",
        port=8001,
        reload=True,
    )
