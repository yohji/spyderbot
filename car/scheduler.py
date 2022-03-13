import logging
import datetime as dt
import random as rnd
from apscheduler.schedulers.background import BackgroundScheduler

from car.crawler import as24
from car.models import CarModel
from car.models import CarVersion
from car.models import CarOffer
from car.models import Search
from car.models import SearchLog


def crawler(search):

    cars = as24(maker = search.maker, model = search.model,
                frm = search.frm, to = search.to, sleep = True)

    # TODO save cars

    search.last = dt.date.today()
    search.save()

    SearchLog(search = search, result = len(cars)).save()

def gather(scheduler):

    now = dt.datetime.now()

    for search in Search.objects.all():
        if search.last != dt.date.today():

            scheduler.add_job(crawler, 'cron',
                              hour = (rnd.randint(now.hour + 1, 23)),
                              minute = (rnd.randint(0, 59)), args = [search])

    logging.getLogger(__name__).info(scheduler.print_jobs())

def start():

    scheduler = BackgroundScheduler()
    gather(scheduler)

    scheduler.add_job(gather, 'cron', hour = 0, minute = 30, args = [scheduler])
    scheduler.start()
