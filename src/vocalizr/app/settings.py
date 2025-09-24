"""Settings for the Vocalizr app."""

from enum import Enum
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, DirectoryPath, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from torch.cuda import is_available

from vocalizr.app.logger import logger

load_dotenv()


class Voices(Enum):
    """Enumeration of available voice presets for the Vocalizr app."""

    AMERICAN_FEMALE_HEART = "af_heart"
    AMERICAN_FEMALE_BELLA = "af_bella"
    AMERICAN_FEMALE_NICOLE = "af_nicole"
    AMERICAN_FEMALE_AOEDE = "af_aoede"
    AMERICAN_FEMALE_KORE = "af_kore"
    AMERICAN_FEMALE_SARAH = "af_sarah"
    AMERICAN_FEMALE_NOVA = "af_nova"
    AMERICAN_FEMALE_SKY = "af_sky"
    AMERICAN_FEMALE_ALLOY = "af_alloy"
    AMERICAN_FEMALE_JESSICA = "af_jessica"
    AMERICAN_FEMALE_RIVER = "af_river"
    AMERICAN_MALE_MICHAEL = "am_michael"
    AMERICAN_MALE_FENRIR = "am_fenrir"
    AMERICAN_MALE_PUCK = "am_puck"
    AMERICAN_MALE_ECHO = "am_echo"
    AMERICAN_MALE_ERIC = "am_eric"
    AMERICAN_MALE_LIAM = "am_liam"
    AMERICAN_MALE_ONYX = "am_onyx"
    AMERICAN_MALE_SANTA = "am_santa"
    AMERICAN_MALE_ADAM = "am_adam"
    BRITISH_FEMALE_EMMA = "bf_emma"
    BRITISH_FEMALE_ISABELLA = "bf_isabella"
    BRITISH_FEMALE_ALICE = "bf_alice"
    BRITISH_FEMALE_LILY = "bf_lily"
    BRITISH_MALE_GEORGE = "bm_george"
    BRITISH_MALE_FABLE = "bm_fable"
    BRITISH_MALE_LEWIS = "bm_lewis"
    BRITISH_MALE_DANIEL = "bm_daniel"

    def __str__(self):
        return self.value


class DirectorySettings(BaseModel):
    """Hold directory path configurations and ensures their existence."""

    base: DirectoryPath = Path.cwd()
    results: DirectoryPath = Path.cwd() / "results"
    log: DirectoryPath = Path.cwd() / "logs"

    @model_validator(mode="after")
    def create_missing_dirs(self) -> "DirectorySettings":
        """
        Ensure that all specified directories exist, creating them if necessary.

        Checks and creates any missing directories defined in the `DirectorySettings`.

        Returns:
            Self: The validated DirectorySettings instance.
        """
        for directory in [self.base, self.results, self.log]:
            if not directory.exists():
                try:
                    directory.mkdir(exist_ok=True)
                    logger.info("Created directory %s.", directory)
                except PermissionError as e:
                    logger.error(
                        "Permission denied while creating directory %s: %s",
                        directory,
                        e,
                    )
                except Exception as e:
                    logger.error("Error creating directory %s: %s", directory, e)
        return self


class ModelSettings(BaseModel):
    """Settings related to model execution."""

    device: Literal["cuda", "cpu"] = "cuda" if is_available() else "cpu"
    char_limit: int = -1
    repo_id: str = "hexgrad/Kokoro-82M"
    lang_code: str = "a"
    choices: Voices = Voices.AMERICAN_FEMALE_HEART


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
