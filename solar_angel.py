from astral import LocationInfo
from astral.sun import elevation
from datetime import datetime, timedelta
import argparse
import pytz

from location import get_location

# Determine location
parser = argparse.ArgumentParser(description="Show current solar elevation")
parser.add_argument("--lat", type=float, help="Latitude")
parser.add_argument("--lon", type=float, help="Longitude")
parser.add_argument("--tz", help="Timezone")
args = parser.parse_args()

lat, lon, tz_name = get_location(args.lat, args.lon, args.tz)
city = LocationInfo("Custom", "Earth", tz_name, lat, lon)
tz = pytz.timezone(tz_name)

# Time to check
now = datetime.now(tz)
observer = city.observer

# Get solar angle
angle = elevation(observer, now)
print(f"Solar angle at {now.strftime('%H:%M')}: {angle:.2f}°")
