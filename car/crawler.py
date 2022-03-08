import urllib
from selectolax.parser import HTMLParser

from .models import CarModel
from .models import CarVersion
from .models import CarOffer


def autoscout24(maker = None, model = None):

    BASE_URL = "https://www.autoscout24.com/lst[MAKER][MODEL]?offer=U%2CJ%2CO%2CD&size=20&page=[PAGE]"
    url = BASE_URL
    page = 1

    url = url.replace('[MAKER]', '/' + maker) if maker != None else url.replace('[MAKER]', '')
    url = url.replace('[MODEL]', '/' + model) if model != None else url.replace('[MODEL]', '')
    url = url.replace('[PAGE]', str(page))

    cars = list()

    with urllib.request.urlopen(url) as resp:
        tree = HTMLParser(resp.read())

        for item in tree.css('.cldt-summary-full-item'):

            for node in item.traverse():
                print(node.attributes)
                # TODO

            mm = item.attributes['data-tracking-name'].split('|')

            carm = CarModel()
            carm.maker = mm[0]
            carm.model = mm[1]

            carv = CarVersion()
            carv.car_model = carm
            carv.version = node.css_first('.cldt-summary-version').text()
            carv.year = int(node.css_first('.first-registration').text().split('/')[1])
            carv.fuel = node.css_first('.summary_item_no_bottom_line').text()
            carv.gear = node.css_first('.transmission-type').text()

            caro = CarOffer()
            caro.car_version = carv
            caro.link = None # TODO
            # caro.country = None # TODO
            caro.price = int(node.attributes['data-tracking-price'])
            caro.miliage = int(node.css_first('.mileage').text().sub('[^0-9]', ''))

            cars.append(caro)

    return cars
