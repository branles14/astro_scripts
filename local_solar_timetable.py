from astral import LocationInfo
from astral.sun import (
    sunrise, sunset,
    civil_dawn, civil_dusk,
    nautical_dawn, nautical_dusk,
    astronomical_dawn, astronomical_dusk,
    elevation
)
from datetime import date, datetime, timedelta
from pathlib import Path
import pytz
import json
import os

def load_env_vars():
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")
    tz = os.getenv("TIMEZONE")

    env_path = Path(__file__).resolve().parent / ".env"
    if (not lat or not lon) and env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "LATITUDE" and not lat:
                        lat = v
                    elif k == "LONGITUDE" and not lon:
                        lon = v
                    elif k == "TIMEZONE" and not tz:
                        tz = v

    config_path = Path.home() / ".config/location"
    if (not lat or not lon) and config_path.exists():
        with open(config_path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "LATITUDE" and not lat:
                        lat = v
                    elif k == "LONGITUDE" and not lon:
                        lon = v
                    elif k == "TIMEZONE" and not tz:
                        tz = v

    if not lat or not lon or not tz:
        raise ValueError("LATITUDE, LONGITUDE, or TIMEZONE not found")

    return float(lat), float(lon), tz

def find_angle_time(observer, tz, angle_target):
    now = datetime.combine(date.today(), datetime.min.time())
    t = tz.localize(now + timedelta(hours=4))  # Start search around dawn
    end = tz.localize(now + timedelta(hours=22))
    step = timedelta(minutes=1)

    while t < end:
        angle = elevation(observer, t)
        if angle >= angle_target:
            return t.strftime("%H:%M")
        t += step
    return None

# === Main logic ===
lat, lon, timezone = load_env_vars()
city = LocationInfo("Custom", "Earth", timezone, lat, lon)
tz = pytz.timezone(timezone)
today = date.today()
obs = city.observer

result = {
    "sunrise": sunrise(obs, today, tzinfo=tz).strftime("%H:%M"),
    "sunset": sunset(obs, today, tzinfo=tz).strftime("%H:%M"),
    "dawn": {
        "civil": civil_dawn(obs, today, tzinfo=tz).strftime("%H:%M"),
        "nautical": nautical_dawn(obs, today, tzinfo=tz).strftime("%H:%M"),
        "astronomical": astronomical_dawn(obs, today, tzinfo=tz).strftime("%H:%M"),
    },
    "dusk": {
        "civil": civil_dusk(obs, today, tzinfo=tz).strftime("%H:%M"),
        "nautical": nautical_dusk(obs, today, tzinfo=tz).strftime("%H:%M"),
        "astronomical": astronomical_dusk(obs, today, tzinfo=tz).strftime("%H:%M"),
    },
    "angle": {
        "35": find_angle_time(obs, tz, 35),
        "40": find_angle_time(obs, tz, 40),
        "75": find_angle_time(obs, tz, 75),
        "90": find_angle_time(obs, tz, 90)
    }
}

print(json.dumps(result, indent=2))
