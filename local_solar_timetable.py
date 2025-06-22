from astral import LocationInfo, Depression
from astral.sun import (
    sunrise,
    sunset,
    dawn,
    dusk,
    elevation,
)
from datetime import date, datetime, timedelta
import argparse
import pytz
import json

from location import get_location


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
parser = argparse.ArgumentParser(description="Display solar timetable for today")
parser.add_argument("--lat", type=float, help="Latitude")
parser.add_argument("--lon", type=float, help="Longitude")
parser.add_argument("--tz", help="Timezone")
args = parser.parse_args()

lat, lon, timezone = get_location(args.lat, args.lon, args.tz)
city = LocationInfo("Custom", "Earth", timezone, lat, lon)
tz = pytz.timezone(timezone)
today = date.today()
obs = city.observer

result = {
    "sunrise": sunrise(obs, today, tzinfo=tz).strftime("%H:%M"),
    "sunset": sunset(obs, today, tzinfo=tz).strftime("%H:%M"),
    "dawn": {
        "civil": dawn(obs, today, depression=Depression.CIVIL, tzinfo=tz).strftime(
            "%H:%M"
        ),
        "nautical": dawn(
            obs, today, depression=Depression.NAUTICAL, tzinfo=tz
        ).strftime("%H:%M"),
        "astronomical": dawn(
            obs, today, depression=Depression.ASTRONOMICAL, tzinfo=tz
        ).strftime("%H:%M"),
    },
    "dusk": {
        "civil": dusk(obs, today, depression=Depression.CIVIL, tzinfo=tz).strftime(
            "%H:%M"
        ),
        "nautical": dusk(
            obs, today, depression=Depression.NAUTICAL, tzinfo=tz
        ).strftime("%H:%M"),
        "astronomical": dusk(
            obs, today, depression=Depression.ASTRONOMICAL, tzinfo=tz
        ).strftime("%H:%M"),
    },
    "angle": {
        "35": find_angle_time(obs, tz, 35),
        "40": find_angle_time(obs, tz, 40),
        "75": find_angle_time(obs, tz, 75),
        "90": find_angle_time(obs, tz, 90),
    },
}

print(json.dumps(result, indent=2))
