import io
import os
import sys
import json
import apprise
import schedule
from loguru import logger
from  weatheril import WeatherIL

SCHEDULE = os.getenv("SCHEDULE")
NOTIFIERS = os.getenv("NOTIFIERS")
LOCATION = os.getenv("LOCATION")
LANGUAGE = os.getenv("LANGUAGE")

apobj = apprise.Apprise()

def get_weather():
    try:
        forecast = ""
        weather = WeatherIL(LOCATION,LANGUAGE).get_forecast() 
        forecast = forecast + f"<b>תחזית ארצית ליום {weather.days[1].day} ה {weather.days[1].date.strftime('%d/%m/%Y')}</b>\n\n"
        forecast = forecast + weather.days[1].description + "\n"
        forecast = forecast + f"טמפרטורה: {weather.days[1].maximum_temperature}°-{weather.days[1].minimum_temperature}°\n\n"
        
        send_forecast(forecast)
    except Exception as e:
        logger.error(e)
        return("aw snap something went wrong")


def send_forecast(message):
    if len(NOTIFIERS)!=0:
        apobj.notify(
            body=message,
            title="",
        )
   


if __name__=="__main__":
  logger.debug("Setting Apprise notification channels")
  jobs=NOTIFIERS.split()
  for job in jobs:
    logger.debug("Adding: " + job)
    apobj.add(job)
  get_weather()
