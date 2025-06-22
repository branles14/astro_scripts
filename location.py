"""Utilities for determining geographic location."""

from pathlib import Path
import os
import json
import subprocess
from shutil import which
from timezonefinder import TimezoneFinder

_TF = TimezoneFinder(in_memory=True)


def _timezone_from_coords(lat: float, lon: float) -> str | None:
    """Return timezone name from latitude and longitude."""
    try:
        return _TF.timezone_at(lat=lat, lng=lon)
    except Exception:
        return None


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


def _termux_location() -> tuple[str | None, str | None]:
    """Return coordinates from ``termux-location`` if available."""
    if which("termux-location"):
        try:
            result = subprocess.run(
                ["termux-location", "-p", "network"],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)
            return str(data.get("latitude")), str(data.get("longitude"))
        except Exception:
            pass
    return None, None


def get_location(
    lat: float | None = None, lon: float | None = None, timezone: str | None = None
):
    """Return ``(latitude, longitude, timezone)``.

    Parameters override environment and configuration files when provided.
    If coordinates are missing, ``termux-location`` is used as a last resort.
    The timezone is automatically determined from the coordinates when not
    explicitly supplied.
    """

    lat = str(lat) if lat is not None else os.getenv("LATITUDE")
    lon = str(lon) if lon is not None else os.getenv("LONGITUDE")
    timezone = timezone or os.getenv("TIMEZONE")

    env_path = Path(__file__).resolve().parent / ".env"
    lat, lon, timezone = _read_config(env_path, lat, lon, timezone)

    config_path = Path.home() / ".config/location"
    lat, lon, timezone = _read_config(config_path, lat, lon, timezone)

    if lat is None or lon is None:
        t_lat, t_lon = _termux_location()
        lat = lat or t_lat
        lon = lon or t_lon

    if lat is None or lon is None:
        raise ValueError("LATITUDE or LONGITUDE not found")

    if timezone is None:
        timezone = _timezone_from_coords(float(lat), float(lon))

    if timezone is None:
        raise ValueError("TIMEZONE not found")

    return float(lat), float(lon), timezone
