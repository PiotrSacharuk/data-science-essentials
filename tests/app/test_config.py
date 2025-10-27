from app.config import Settings


def test_default_settings():
    """Test default settings values."""
    settings = Settings.get_test_settings()
    assert settings.server_host == "localhost"
    assert settings.server_port == 8000


def test_settings_from_env(monkeypatch):
    """Test loading settings from environment variables."""
    monkeypatch.setenv("SERVER_HOST", "testhost")
    monkeypatch.setenv("SERVER_PORT", "9000")

    settings = Settings()
    assert settings.server_host == "testhost"
    assert settings.server_port == 9000


def test_ignore_extra_env_vars(monkeypatch):
    """Test that extra environment variables are ignored."""
    # Set some extra environment variables
    monkeypatch.setenv("SERVER_HOST", "testhost")
    monkeypatch.setenv("SERVER_PORT", "9000")
    monkeypatch.setenv("EXTRA_VAR", "should_be_ignored")

    settings = Settings()
    assert settings.server_host == "testhost"
    assert settings.server_port == 9000
    assert not hasattr(settings, "extra_var")  # Extra var should be ignored
