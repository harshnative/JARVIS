
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

geolocator = Nominatim(user_agent="geoapiExercises")

lad = input("Enter your place to find time\n")
print("Location address:", lad)

location = geolocator.geocode(lad)
print("Latitude and Longitude of the said address:")
print((location.latitude, location.longitude))

obj = TimezoneFinder()
result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
print("Time Zone : ", result)
timeZ_Kl = pytz.timezone(result)
dt_Kl = datetime.now(timeZ_Kl)
print(dt_Kl.strftime('%Y-%m-%d %H:%M:%S %Z %z'))
