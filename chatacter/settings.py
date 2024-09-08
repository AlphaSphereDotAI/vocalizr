from pydantic import BaseModel


class AssetsSettings(BaseModel):
    audio: str = "./assets/audio/"
    image: str = "./assets/image/"
    video: str = "./assets/video/"


class BarkSettings(BaseModel):
    name: str = "suno/bark-small"
    path: str = "./chatacter/bark-small"


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: AssetsSettings = AssetsSettings()
    bark: BarkSettings = BarkSettings()


def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings: Settings = get_settings()
    print(settings.model_dump_json(indent=4))
