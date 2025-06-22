from astral import LocationInfo
from astral.sun import elevation
from datetime import datetime, timedelta
import pytz

city = LocationInfo("Broomfield", "USA", "America/Denver", 39.9205, -105.0867)
tz = pytz.timezone(city.timezone)

# Time to check
now = datetime.now(tz)
observer = city.observer

# Get solar angle
angle = elevation(observer, now)
print(f"Solar angle at {now.strftime('%H:%M')}: {angle:.2f}°")
