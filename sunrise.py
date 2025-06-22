from astral import LocationInfo
from astral.sun import sun
from datetime import date

city = LocationInfo("Broomfield", "USA", "America/Denver", 39.9205, -105.0867)
s = sun(city.observer, date=date.today(), tzinfo=city.timezone)

print("Sunrise:", s["sunrise"])
