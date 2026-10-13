"""Tests for the shared PreenCut utilities."""

import pytest

import utils


def test_rounding_carries_into_minutes():
    assert utils.seconds_to_hhmmss(59.6) == "00:01:00"


def test_rounding_carries_into_hours():
    assert utils.seconds_to_hhmmss(3599.7) == "01:00:00"


@pytest.mark.parametrize("seconds", [0, 59, 60, 3599, 3600, 3723.4, 86399.6])
def test_round_trip(seconds):
    assert utils.hhmmss_to_seconds(utils.seconds_to_hhmmss(seconds)) == pytest.approx(round(seconds))


def test_missing_audio_stream(monkeypatch):
    class Result:
        stdout = '{"streams": []}'
        stderr = ""

    monkeypatch.setattr("utils.subprocess.run", lambda *a, **k: Result())
    assert utils.get_audio_codec("silent.mp4") is None


def test_present_audio_stream(monkeypatch):
    class Result:
        stdout = '{"streams": [{"codec_name": "aac"}]}'
        stderr = ""

    monkeypatch.setattr("utils.subprocess.run", lambda *a, **k: Result())
    assert utils.get_audio_codec("talk.mp4") == "aac"
