from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


class Location(BaseSettings):
    name: str
    subnet: str


class PyASICDashSettings(BaseSettings):
    title: str = "PyASIC Dash"

    locations: list[Location] = Field(default_factory=list)
    interval: int = 5

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        root_dir = Path(__file__).parent.resolve()
        toml_file = root_dir.parent.joinpath("settings.toml")
        settings_sources = [
            env_settings,
            TomlConfigSettingsSource(settings_cls, toml_file),
        ]
        return tuple(settings_sources)


config = PyASICDashSettings()
