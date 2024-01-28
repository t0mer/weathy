import io
import os
import sys
import json
import apprise
import schedule
from loguru import logger
from  weatheril import WeatherIL

SCHEDULE = int(os.getenv("SCHEDULE"))
NOTIFIERS = os.getenv("NOTIFIERS")
LOCATION = os.getenv("LOCATION")
LANGUAGE = os.getenv("LANGUAGE")

apobj = apprise.Apprise()

def get_weather():
    try:
        forecast = ""
        weather = WeatherIL(LOCATION,LANGUAGE).get_forecast() 
        for x in range(1, 5):
            forecast = forecast + f"*תחזית ארצית ליום {weather.days[x].day} ה {weather.days[x].date.strftime('%d/%m/%Y')}*\n"
            forecast = forecast + weather.days[x].description + "\n"
            forecast = forecast + f"טמפרטורה: {weather.days[x].maximum_temperature}°-{weather.days[x].minimum_temperature}°\n\n"
        return forecast
    except Exception as e:
        logger.error(e)
        return("aw snap something went wrong")





if __name__=="__main__":
  logger.debug("Setting Apprise notification channels")
  jobs=NOTIFIERS.split()
  for job in jobs:
    logger.debug("Adding: " + job)
    apobj.add(job)
