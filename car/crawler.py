import urllib
from selectolax.parser import HTMLParser
import re

from .models import CarModel
from .models import CarVersion
from .models import CarOffer


def as24(maker = None, model = None, frm = None, to = None):

    DOMAIN_URL = 'https://www.autoscout24.com'
    BASE_URL = DOMAIN_URL + '/lst[MAKER][MODEL]?offer=U%2CJ%2CO%2CD&size=20&page=[PAGE]'

    url = BASE_URL
    url = url.replace('[MAKER]', '/' + maker) if maker != None else url.replace('[MAKER]', '')
    url = url.replace('[MODEL]', '/' + model) if model != None else url.replace('[MODEL]', '')

    if frm != None:
        url += "&fregfrom=" + frm
    if to != None:
        url += "&fregto=" + to

    page = 1
    url = url.replace('[PAGE]', str(page))

    cars = list()

    # TODO: markets
    # TODO: pagination

    with urllib.request.urlopen(url) as resp:
        tree = HTMLParser(resp.read())

        for item in tree.css('.cldt-summary-full-item'):

            carm = CarModel()
            carv = CarVersion()
            carv.car_model = carm
            caro = CarOffer()
            caro.car_version = carv

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
                        carv.version = node.text()

                    elif attrs['class'] == 'summary_item_no_bottom_line' and carv.fuel == None:
                        # carv.fuel = node.text()
                        pass # FIXME
                        
                    elif attrs['class'] == 'cldf-summary-seller-contact-country':
                        caro.market = node.text()

                elif 'data-type' in attrs:

                    if attrs['data-type'] == 'first-registration':
                        carv.year = int(node.text().split('/')[1])

                    elif attrs['data-type'] == 'mileage':
                        caro.miliage = int(re.sub('[^0-9]', '', node.text()))

                    elif attrs['data-type'] == 'transmission-type':
                        # carv.gear = node.text()
                        pass # FIXME

                elif 'data-item-name' in attrs:

                    if attrs['data-item-name'] == 'detail-page-link':
                        caro.link = DOMAIN_URL + attrs['href']

            print(caro)
            cars.append(caro)

    return cars
