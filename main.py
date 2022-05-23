import requests
import smtplib
import time
from datetime import datetime

MY_LAT = -28.155621
MY_LONG = 153.472519

# Request ISS location from API and enter in variable as dictionary
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

# Assign longitude and latitude values
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Provide current location time in UTC 24hr format to sunrise sunset API
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Get current sunrise and sunset time for given location
response = requests.get(
    "https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_local = datetime.now()
time_local = time_local.isoformat("#", "minutes").split("#")

# Get current time UTC
time_now = str(datetime.utcnow())
time_now = int(time_now.split(" ")[1].split(":")[0])

# Determine if night time
if time_now >= sunset and time_now <= sunrise:
    night = True
else:
    night = False

# Determine if ISS within latitude and longitude of 5 from current location
lat_prox = abs(abs(MY_LAT) - abs(iss_latitude))
long_prox = abs(abs(MY_LONG) - abs(iss_longitude))

if lat_prox <= 5 and lat_prox <= 5:
    near = True
else:
    near = False

# Send email if night time
# Will repeat every 60s until out of specified area or daytime
while night and near:
    email_address = "_ENTER_SENDING_EMAIL_
    msg = f"Subject:ISS Currently Visible\n\n At {time_local[1]}hrs on the {time_local[0]}, we detected that the Internation Space Station was visible at your location {MY_LAT, MY_LONG}.\n\nLook-up now and see if you can spot it."
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email_address, password=input(
            "Please enter your password: "))
        connection.sendmail(from_addr=email_address,
                            to_addrs="__ENTER_RECIPIENT_EMAIL__, msg=msg)
    time.sleep(60)
