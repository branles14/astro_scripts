from datetime import datetime, timedelta, time
from astral import LocationInfo
from astral.sun import sun
from astral.location import Location
import pytz
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

latitude = float(os.getenv("LAT"))
longitude = float(os.getenv("LON"))
timezone = os.getenv("TZ")

location = LocationInfo(name="CustomLocation", region="Nowhere", timezone=timezone, latitude=latitude, longitude=longitude)
observer = location.observer
loc = Location(info=location)
tz = pytz.timezone(timezone)

year = datetime.now().year
days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
results = []

for day_offset in range(days):
    date = datetime(year, 1, 1) + timedelta(days=day_offset)
    s = sun(observer, date=date, tzinfo=tz)

    # Solar angle at 08:00
    time_8 = tz.localize(datetime.combine(date, time(8, 0)))
    angle_at_8 = loc.solar_elevation(time_8)

    # Time when sun reaches 35° and 40°, and falls below 40° and 35°
    dt = s['sunrise']
    end = s['sunset']
    hit_35 = hit_40 = drop_40 = drop_35 = None

    while dt <= end:
        angle = loc.solar_elevation(dt)
        if not hit_35 and angle >= 35:
            hit_35 = dt
        if not hit_40 and angle >= 40:
            hit_40 = dt
        if hit_40 and not drop_40 and angle < 40:
            drop_40 = dt
        if hit_35 and not drop_35 and angle < 35:
            drop_35 = dt
        dt += timedelta(minutes=1)

    max_angle = loc.solar_elevation(s['noon'])

    results.append({
        'date': date.date(),
        'sunrise': s['sunrise'].strftime('%H:%M'),
        '08h_angle': f"{angle_at_8:.2f}",
        '35_up': hit_35.strftime('%H:%M') if hit_35 else None,
        '40_up': hit_40.strftime('%H:%M') if hit_40 else None,
        'solar_noon': s['noon'].strftime('%H:%M'),
        'max_angle': f"{max_angle:.2f}",
        '40_down': drop_40.strftime('%H:%M') if drop_40 else None,
        '35_down': drop_35.strftime('%H:%M') if drop_35 else None,
        'sunset': s['sunset'].strftime('%H:%M')
    })

df = pd.DataFrame(results)
df.to_csv("sun_times.csv", index=False)
print("Saved to sun_times.csv")
