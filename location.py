"""Utilities for determining geographic location."""

from pathlib import Path
import os


def _read_config(path: Path, lat: str | None, lon: str | None, tz: str | None):
    """Read location data from a simple key=value file."""
    if path.exists():
        with open(path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "LATITUDE" and not lat:
                        lat = v
                    elif k == "LONGITUDE" and not lon:
                        lon = v
                    elif k == "TIMEZONE" and not tz:
                        tz = v
    return lat, lon, tz


def get_location(
    lat: float | None = None, lon: float | None = None, timezone: str | None = None
):
    """Return ``(latitude, longitude, timezone)``.

    Parameters override environment and configuration files when provided.
    If any value is missing, the search order is:
    1. environment variables ``LATITUDE``, ``LONGITUDE``, ``TIMEZONE``
    2. ``.env`` file next to this module
    3. ``~/.config/location``
    """

    lat = str(lat) if lat is not None else os.getenv("LATITUDE")
    lon = str(lon) if lon is not None else os.getenv("LONGITUDE")
    timezone = timezone or os.getenv("TIMEZONE")

    env_path = Path(__file__).resolve().parent / ".env"
    lat, lon, timezone = _read_config(env_path, lat, lon, timezone)

    config_path = Path.home() / ".config/location"
    lat, lon, timezone = _read_config(config_path, lat, lon, timezone)

    if lat is None or lon is None or timezone is None:
        raise ValueError("LATITUDE, LONGITUDE, or TIMEZONE not found")

    return float(lat), float(lon), timezone
