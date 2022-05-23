import requests
from datetime import datetime

MY_LAT = -28.155621
MY_LONG = 153.472519

#Request ISS location from API and enter in variable as dictionary
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

#Assign longitude and latitude values
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Provide current location time in UTC 24hr format to sunrise sunset API
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

#Get current sunrise and sunset time for given location
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

#Get current time UTC
time_now = str(datetime.utcnow())
time_now = int(time_now.split(" ")[1].split(":")[0])

#Determine if night time
if time_now >= sunset and time_now<=sunrise:
    night = True
else:
    night = False

