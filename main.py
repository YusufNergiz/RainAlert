import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


MY_LAT = 21.012230
MY_LONG = 28.978359
api_key = os.environ.get("OWN_API_KEY")

account_sid = "AC4998de1745722ffbed33028f9cae7aa7"
auth_token = os.environ.get("AUTH_TOKEN")


response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={MY_LAT}&lon={MY_LONG}"
                        f"&exclude=current,minutely,daily,alerts&appid={api_key}")
response.raise_for_status()
weather_data = response.json()
weather_in_12_hours = weather_data["hourly"]

# Collects 12 hour weather ids inside the weather_ids list (if the id is less than
# 700 it means its a rainy or a snowy day)

weather_ids = []

for hour in range(0, 12):
    weather_output_ids = weather_data["hourly"][hour]["weather"][0]["id"]     ### --> U can also use slices
                                                                              ### weather_data["hourly][:12]
    weather_ids.append(weather_output_ids)

print(weather_ids)
##############################################################################################

# Collects and appends all the ids that are less than 700 to rainy_day list and the remaining
# go inside good_weather list

rainy_day = []
good_weather = []

for weather_id in weather_ids:
    if int(weather_id) < 700:
        rainy_day.append(weather_id)
    else:
        good_weather.append(weather_id)

##########################################################################

# Checks if the rainy_day list has any items inside since if it contains any that means that
# there will be rain in the next 12 hours
if len(rainy_day) > 0:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Hi, Good day it seems like today is gonna be a rainy day take an umbrella with you! ☔",
        from_="+14752514656",
        to="+48883277736"
    )
    print(message.status)




