"""Tests for runtime configuration defaults."""

import importlib
import os


def test_gradio_temp_dir_defaults_into_the_project(monkeypatch):
    monkeypatch.delenv("GRADIO_TEMP_DIR", raising=False)
    import config
    importlib.reload(config)
    value = os.environ["GRADIO_TEMP_DIR"]
    assert value.endswith(os.path.join("temp", "gradio"))
    assert os.path.isdir(value)


def test_gradio_temp_dir_keeps_an_existing_override(monkeypatch, tmp_path):
    override = str(tmp_path / "gradio")
    monkeypatch.setenv("GRADIO_TEMP_DIR", override)
    import config
    importlib.reload(config)
    assert os.environ["GRADIO_TEMP_DIR"] == override
    assert os.path.isdir(override)
