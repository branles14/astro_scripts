#!/bin/python3
from astral import LocationInfo, Depression
from astral.sun import (
    sunrise,
    sunset,
    dawn,
    dusk,
    noon,
    elevation,
)
from datetime import date, datetime, timedelta
import argparse
import pytz
import json

from location import get_location


def _format_time(dt: datetime) -> str:
    """Return a ``HH:MM`` formatted time string."""

    return dt.strftime("%H:%M")


def _crossing_time(observer, start, end, angle_target, ascending=True):
    """Return the local time when the sun crosses ``angle_target``."""

    step = timedelta(minutes=1)
    t = start
    prev_angle = elevation(observer, t)

    while t <= end:
        current_angle = elevation(observer, t)
        if ascending:
            if prev_angle < angle_target <= current_angle:
                return t.strftime("%H:%M")
        else:
            if prev_angle > angle_target >= current_angle:
                return t.strftime("%H:%M")
        prev_angle = current_angle
        t += step
    return None


# === Main logic ===
parser = argparse.ArgumentParser(description="Display solar timetable for today")
parser.add_argument("--lat", type=float, help="Latitude")
parser.add_argument("--lon", type=float, help="Longitude")
args = parser.parse_args()
try:
    lat, lon, timezone = get_location(args.lat, args.lon)
except Exception as exc:
    parser.error(str(exc))

city = LocationInfo("Custom", "Earth", timezone, lat, lon)
tz = pytz.timezone(timezone)
today = date.today()
obs = city.observer

sunrise_time = sunrise(obs, today, tzinfo=tz)
sunset_time = sunset(obs, today, tzinfo=tz)
noon_time = noon(obs, today, tzinfo=tz)

start_day = tz.localize(datetime.combine(today, datetime.min.time()))
end_day = tz.localize(datetime.combine(today, datetime.max.time()))
max_angle = elevation(obs, noon_time)

angles = [a for a in range(0, 95, 5) if a <= max_angle]
solar_path: list[dict[str, float | str]] = []

for angle in angles:
    t_up = _crossing_time(obs, start_day, noon_time, angle, ascending=True)
    if t_up:
        solar_path.append({"time": t_up, "altitude": angle})

solar_path.append({"time": _format_time(noon_time), "altitude": round(max_angle)})

for angle in reversed(angles):
    t_down = _crossing_time(obs, noon_time, end_day, angle, ascending=False)
    if t_down:
        solar_path.append({"time": t_down, "altitude": angle})

result = {
    "date": today.strftime("%Y-%m-%d"),
    "latitude": lat,
    "longitude": lon,
    "timezone": timezone,
    "sun_times": {
        "dawn": {
            "civil": _format_time(
                dawn(obs, today, depression=Depression.CIVIL, tzinfo=tz)
            ),
            "nautical": _format_time(
                dawn(obs, today, depression=Depression.NAUTICAL, tzinfo=tz)
            ),
            "astronomical": _format_time(
                dawn(obs, today, depression=Depression.ASTRONOMICAL, tzinfo=tz)
            ),
        },
        "sunrise": _format_time(sunrise_time),
        "sunset": _format_time(sunset_time),
        "dusk": {
            "civil": _format_time(
                dusk(obs, today, depression=Depression.CIVIL, tzinfo=tz)
            ),
            "nautical": _format_time(
                dusk(obs, today, depression=Depression.NAUTICAL, tzinfo=tz)
            ),
            "astronomical": _format_time(
                dusk(obs, today, depression=Depression.ASTRONOMICAL, tzinfo=tz)
            ),
        },
    },
    "solar_path": solar_path,
}

print(json.dumps(result, indent=2))
