"""Settings for the Vocalizr app."""

from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import (
    BaseModel,
    DirectoryPath,
    Field,
    PositiveInt,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from torch.cuda import is_available

from vocalizr.app.logger import logger

load_dotenv()


class DirectorySettings(BaseModel):
    """Hold directory path configurations and ensures their existence."""

    base: DirectoryPath = Field(default_factory=Path.cwd, frozen=True)

    @computed_field
    @property
    def results(self) -> DirectoryPath:
        """Path to the results directory."""
        return self.base / "results" / APP_NAME

    @computed_field
    @property
    def log(self) -> DirectoryPath:
        """Path to the log directory."""
        return self.base / "logs" / APP_NAME

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

    device: Literal["cuda", "cpu"] = Field(
        default_factory=lambda: "cuda" if is_available() else "cpu",
    )
    char_limit: Literal[-1] | PositiveInt = Field(default=-1)
    min_requested_characters: PositiveInt = Field(default=4)
    repo_id: str = Field(default="hexgrad/Kokoro-82M")
    lang_code: str = Field(default="a")
    choices: Voices = Field(default=Voices.AMERICAN_FEMALE_HEART)


class Settings(BaseSettings):
    """Configuration for the Vocalizr app."""

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_parse_none_str="None",
        env_file=".env",
        extra="ignore",
    )
    directory: DirectorySettings = Field(default_factory=DirectorySettings, frozen=True)
    model: ModelSettings = Field(default_factory=ModelSettings)
