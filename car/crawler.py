import re
import time
import logging
import random as rnd

import urllib.request
from selectolax.parser import HTMLParser

from .models import Market
from .models import CarModel
from .models import CarVersion
from .models import CarOffer
from .models import Source


def as24(maker = None, model = None, frm = None, to = None, sleep = False):

    DOMAIN_URL = 'https://www.autoscout24.com'
    BASE_URL = DOMAIN_URL + '/lst[MAKER][MODEL]?offer=U%2CJ%2CO%2CD&size=20&page=[PAGE]'

    url = BASE_URL
    url = url.replace('[MAKER]', '/' + maker) if maker != None else url.replace('[MAKER]', '')
    url = url.replace('[MODEL]', '/' + model) if model != None else url.replace('[MODEL]', '')

    if frm != None:
        url += "&fregfrom=" + str(frm)
    if to != None:
        url += "&fregto=" + str(to)

    cars = list()
    log = logging.getLogger(__name__)

    for market in Market.objects.all():

        if market.as24 != None:
            url_market = '%s&cy=%s' % (url, market.as24)

            page = 1
            while True:
                url_page = url_market.replace('[PAGE]', str(page))

                with urllib.request.urlopen(url_page) as resp:
                    root = HTMLParser(resp.read()).css('.cldt-summary-full-item')

                    if len(root) == 0:
                        break

                    for item in root:

                        carm = CarModel()
                        carv = CarVersion(car_model = carm)
                        caro = CarOffer(car_version = carv, market = market, source = Source.AS24)

                        for node in item.traverse():
                            # print("%s: %s -> %s" % (node, node.attributes, node.text(deep = False, strip = True)))
                            attrs = node.attributes

                            if 'class' in attrs:

                                if attrs['class'] == 'cldt-summary-full-item':
                                    mm = attrs['data-tracking-name'].split('|')
                                    carm.maker = mm[0]
                                    carm.model = mm[1]

                                    caro.price = int(attrs['data-tracking-price'])
                                    caro.seller = attrs['data-customerid']

                                elif attrs['class'] == 'cldt-summary-version sc-ellipsis':
                                    carv.version = node.text().strip()

                                elif attrs['class'] == 'summary_item_no_bottom_line' and carv.fuel == None:
                                    carv.fuel = node.text().strip()

                            elif 'data-type' in attrs:

                                if attrs['data-type'] == 'first-registration':
                                    carv.year = int(node.text().strip().split('/')[1])

                                elif attrs['data-type'] == 'mileage':
                                    caro.miliage = int(re.sub('[^0-9]', '', node.text().strip()))

                                elif attrs['data-type'] == 'transmission-type':
                                    carv.gear = node.text().strip()

                            elif 'data-item-name' in attrs:

                                if attrs['data-item-name'] == 'detail-page-link':
                                    caro.link = DOMAIN_URL + attrs['href']

                        log.debug(caro)
                        cars.append(caro)

                page += 1

                if sleep:
                    time.sleep(1 + (rnd.random() * 10))

    return cars
