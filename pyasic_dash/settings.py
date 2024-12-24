from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


class PyASICDashSettings(BaseSettings):
    title: str = "PyASIC Dash"

    range: list[dict] = Field(default_factory=list)

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
        toml_file = root_dir.parent.joinpath("servers.toml")
        settings_sources = [
            env_settings,
            TomlConfigSettingsSource(settings_cls, toml_file),
        ]
        return tuple(settings_sources)


config = PyASICDashSettings()
