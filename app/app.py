import os
import time
import apprise
import schedule
from loguru import logger
from  weatheril import WeatherIL, utils
import datetime
SCHEDULE = os.getenv("SCHEDULE")
NOTIFIERS = os.getenv("NOTIFIERS")
LOCATION = os.getenv("LOCATION")
LANGUAGE = os.getenv("LANGUAGE")

apobj = apprise.Apprise()

def get_weather():
    current_time = datetime.datetime.now().time()
    try:
        forecast = ""
        hourly = "\n\n\n\n"
        weather = WeatherIL(LOCATION,LANGUAGE).get_forecast().days[1]
        forecast = forecast + f"<b>תחזית ארצית ליום {weather.day} ה {weather.date.strftime('%d/%m/%Y')}</b>\n\n"
        forecast = forecast + weather.description + "\n"
        forecast = forecast + f"טמפרטורה ממוצעת: {weather.maximum_temperature}°-{weather.minimum_temperature}°\n\n"
        
        for hour in weather.hours:
            forecast_time = datetime.time(int(hour.hour.split(":")[0]),int(hour.hour.split(":")[1]))
            if forecast_time > current_time:
                hourly = hourly + "<b>" + hour.hour + " :</b>" + str(hour.temperature)  + ", " + utils.HE_WEATHER_CODES.get(str(hour.weather_code), "") +   ", " + str(hour.rain_chance) + "% סיכוי לגשם" + "\n\n"
        forecast = forecast + hourly
        send_forecast(forecast)
    except Exception as e:
        logger.error("aw snap something went wrong: " + str(e))
        send_forecast("aw snap something went wrong")


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


  schedule.every().day.at(SCHEDULE).do(get_weather)
  while True:
    schedule.run_pending()
    time.sleep(1)
