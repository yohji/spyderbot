from django.db import models
import hashlib


class Market (models.Model):

    code = models.CharField(primary_key = True, max_length = 2)
    description = models.CharField(max_length = 25)
    as24 = models.CharField(null = True, max_length = 2)

    def __str__(self):
        return self.description


class CarModel (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    maker = models.CharField(max_length = 255, db_index = True)
    model = models.CharField(max_length = 255, db_index = True)
    timestamp = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):

        m = hashlib.sha256()
        m.update(self.maker.encode())
        m.update(self.model.encode())
        self.hashkey = m.hexdigest()

        if not CarModel.objects.filter(hashkey=[self.hashkey]).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return "[%s|%s]" % (self.maker, self.model)


class CarVersion (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    version = models.CharField(max_length = 255, db_index = True)
    year = models.IntegerField(db_index = True)
    fuel = models.CharField(null = True, max_length = 10)
    gear = models.CharField(null = True, max_length = 10)
    timestamp = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):

        m = hashlib.sha256()
        m.update(self.car_model.hashkey.encode())
        m.update(self.version.encode())
        m.update(str(self.year).encode())
        self.hashkey = m.hexdigest()

        if not CarVersion.objects.filter(hashkey=[self.hashkey]).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return "[%s|%s|%s|%s|%s]" % (self.car_model, self.version,
                             self.year, self.fuel, self.gear)

class Source:

    AS24 = 'AS24'

    SOURCES = (
        (AS24, 'autoscout24.com'),
    )

class CarOffer (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    car_version = models.ForeignKey(CarVersion, on_delete=models.PROTECT)
    market = models.ForeignKey(Market, on_delete=models.PROTECT)
    source = models.CharField(max_length = 4, choices = Source.SOURCES, db_index = True)
    price = models.IntegerField(db_index = True)
    seller = models.CharField(max_length = 64, null = True)
    miliage = models.IntegerField()
    link = models.CharField(max_length = 2048, null = True)
    timestamp = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):

        m = hashlib.sha256()
        m.update(self.car_version.hashkey.encode())
        m.update(self.market.code.encode())
        m.update(self.source.encode())
        m.update(str(self.price).encode())
        self.hashkey = m.hexdigest()

        if not CarOffer.objects.filter(hashkey=[self.hashkey]).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return "[%s%s|%s|%s|%s|%s|%s]" % (self.car_version, self.source, self.market,
                                        self.price, self.seller, self.miliage, self.link)


class Search (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    maker = models.CharField(max_length = 255)
    model = models.CharField(max_length = 255, null = True)
    frm = models.IntegerField(null = True)
    to = models.IntegerField(null = True)
    last = models.DateField()
    timestamp = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):

        m = hashlib.sha256()
        m.update(self.maker.encode())
        m.update(self.model.encode())
        m.update(str(self.frm).encode())
        m.update(str(self.to).encode())
        self.hashkey = m.hexdigest()

        if not Search.objects.filter(hashkey=[self.hashkey]).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return "[%s|%s|%s|%s|%s]" % (self.maker, self.model,
                                  self.frm, self.to, self.last)


class SearchLog (models.Model):

    search = models.ForeignKey(Search, on_delete=models.PROTECT)
    source = models.CharField(max_length = 4, choices = Source.SOURCES, db_index = True)
    result = models.IntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "[%s|%s]" % (self.search, self.result)
