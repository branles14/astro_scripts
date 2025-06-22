from astral import LocationInfo
from astral.sun import sun
from datetime import date
import argparse

from location import get_location

# Determine location
parser = argparse.ArgumentParser(description="Show today's sunrise time")
parser.add_argument("--lat", type=float, help="Latitude")
parser.add_argument("--lon", type=float, help="Longitude")
args = parser.parse_args()

lat, lon, tz_name = get_location(args.lat, args.lon)
city = LocationInfo("Custom", "Earth", tz_name, lat, lon)
s = sun(city.observer, date=date.today(), tzinfo=tz_name)

print("Sunrise:", s["sunrise"])
