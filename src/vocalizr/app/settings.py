"""Settings for the Vocalizr app."""
from enum import Enum
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from gradio import Error
from pydantic import BaseModel, DirectoryPath, Field, FilePath, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from torch.cuda import is_available

from vocalizr.app.logger import logger

load_dotenv()

class DirectorySettings(BaseModel):
    base: DirectoryPath = Field(default_factory=lambda: Path.cwd())
    results: DirectoryPath = Field(default_factory=lambda: Path.cwd() / "results")
    log: DirectoryPath = Field(default_factory=lambda: Path.cwd() / "logs")

    @model_validator(mode="after")
    def create_missing_dirs(self) -> "DirectorySettings":
        """
        Ensure that all specified directories exist, creating them if necessary.

        Checks and creates any missing directories defined in the `DirectorySettings`.

        Returns:
            Self: The validated DirectorySettings instance.
        """
        for directory in [
            self.base,
            self.results,
            self.frames,
            self.checkpoint,
            self.assets,
            self.log,
            self.image,
            self.audio,
            self.video,
        ]:
            if not directory.exists():
                directory.mkdir(exist_ok=True)
                logger.info("Created directory %s.", directory)
        return self

    class Voices(Enum):
    CHOICES: dict[str, str] = {
        "american_female_Heart ❤️": "af_heart",
        "american_female_Bella 🔥": "af_bella",
        "american_female_Nicole 🎧": "af_nicole",
        "american_female_Aoede": "af_aoede",
        "american_female_Kore": "af_kore",
        "american_female_Sarah": "af_sarah",
        "american_female_Nova": "af_nova",
        "american_female_Sky": "af_sky",
        "american_female_Alloy": "af_alloy",
        "american_female_Jessica": "af_jessica",
        "american_female_River": "af_river",
        "american_male_Michael": "am_michael",
        "american_male_Fenrir": "am_fenrir",
        "american_male_Puck": "am_puck",
        "american_male_Echo": "am_echo",
        "american_male_Eric": "am_eric",
        "american_male_Liam": "am_liam",
        "american_male_Onyx": "am_onyx",
        "american_male_Santa": "am_santa",
        "american_male_Adam": "am_adam",
        "british_female_Emma": "bf_emma",
        "british_female_Isabella": "bf_isabella",
        "british_female_Alice": "bf_alice",
        "british_female_Lily": "bf_lily",
        "british_male_George": "bm_george",
        "british_male_Fable": "bm_fable",
        "british_male_Lewis": "bm_lewis",
        "british_male_Daniel": "bm_daniel",
    }
class ModelSettings(BaseModel):
    device: Literal["cuda", "cpu"] = "cuda" if is_available() else "cpu"
    repo_id: str = "hexgrad/Kokoro-82M"
    lang_code: str = "a"


    CHOICES: dict[str, str] = {
    "american_female_Heart ❤️": "af_heart",
    "american_female_Bella 🔥": "af_bella",
    "american_female_Nicole 🎧": "af_nicole",
    "american_female_Aoede": "af_aoede",
    "american_female_Kore": "af_kore",
    "american_female_Sarah": "af_sarah",
    "american_female_Nova": "af_nova",
    "american_female_Sky": "af_sky",
    "american_female_Alloy": "af_alloy",
    "american_female_Jessica": "af_jessica",
    "american_female_River": "af_river",
    "american_male_Michael": "am_michael",
    "american_male_Fenrir": "am_fenrir",
    "american_male_Puck": "am_puck",
    "american_male_Echo": "am_echo",
    "american_male_Eric": "am_eric",
    "american_male_Liam": "am_liam",
    "american_male_Onyx": "am_onyx",
    "american_male_Santa": "am_santa",
    "american_male_Adam": "am_adam",
    "british_female_Emma": "bf_emma",
    "british_female_Isabella": "bf_isabella",
    "british_female_Alice": "bf_alice",
    "british_female_Lily": "bf_lily",
    "british_male_George": "bm_george",
    "british_male_Fable": "bm_fable",
    "british_male_Lewis": "bm_lewis",
    "british_male_Daniel": "bm_daniel",
}
    @model_validator(mode="after")
    def check_image_path(self) -> "ModelSettings":
        if self.image_path and not self.image_path.exists():
            _msg = f"Image path does not exist: {self.image_path}"
            logger.error(_msg)
            Error(_msg)
            raise FileNotFoundError(_msg)
        if self.audio_path and not self.audio_path.exists():
            _msg = f"Audio path does not exist: {self.audio_path}"
            logger.error(_msg)
            Error(_msg)
            raise FileNotFoundError(_msg)
        return self


class Settings(BaseSettings):
    """Configuration for the Vocalizr app."""

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_parse_none_str="None",
        env_file=".env",
        extra="ignore",
    )
    directory: DirectorySettings = DirectorySettings()
    model: ModelSettings = ModelSettings()
