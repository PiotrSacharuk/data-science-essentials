from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.test"), extra="ignore")

    server_host: str = "localhost"
    server_port: int = 8000

    @classmethod
    def get_test_settings(cls, **env_values) -> "Settings":
        """Create Settings instance for testing with specified env values.

        Args:
            **env_values: Environment variables to set for testing.

        Returns:
            Settings: Settings instance with test configuration.
        """
        return cls(_env_file=None, **env_values)


settings = Settings()
