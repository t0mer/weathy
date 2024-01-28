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







if __name__=="__main__":
  logger.debug("Setting Apprise notification channels")
  jobs=NOTIFIERS.split()
  for job in jobs:
    logger.debug("Adding: " + job)
    apobj.add(job)
