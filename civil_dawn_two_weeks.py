from __future__ import annotations

from astral import LocationInfo, Depression
from astral.sun import dawn
from datetime import date, timedelta
import argparse
import json
import pytz

from location import get_location


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display civil dawn times for the next two weeks"
    )
    parser.add_argument("--lat", type=float, help="Latitude")
    parser.add_argument("--lon", type=float, help="Longitude")
    args = parser.parse_args()

    try:
        lat, lon, tz_name = get_location(args.lat, args.lon)
    except Exception as exc:  # noqa: BLE001
        parser.error(str(exc))

    tz = pytz.timezone(tz_name)
    location = LocationInfo("Custom", "Earth", tz_name, lat, lon)
    observer = location.observer

    start = date.today()
    dawn_times: dict[str, str] = {}
    for i in range(14):
        day = start + timedelta(days=i)
        dt = dawn(observer, day, depression=Depression.CIVIL, tzinfo=tz)
        dawn_times[day.isoformat()] = dt.strftime("%H:%M")

    print(json.dumps(dawn_times, indent=2))


if __name__ == "__main__":
    main()
