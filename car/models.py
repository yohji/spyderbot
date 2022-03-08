from django.db import models
import hashlib


class Country (models.Model):

    code = models.CharField(primary_key = True, max_length = 2)
    description = models.CharField(max_length = 25)

    def __str__(self):
        return self.description


class CarModel (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    maker = models.CharField(max_length = 255)
    model = models.CharField(max_length = 255)
    timestamp = models.DateTimeField(auto_now = True)

    def save(self):
        m = hashlib.sha256()
        m.update(self.maker.encode())
        m.update(self.model.encode())
        self.hashkey = m.hexdigest()

        super().save(self)

    def __str__(self):
        return "%s %s" % (self.maker, self.model)


class CarVersion (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    version = models.CharField(max_length = 255)
    year = models.IntegerField(null = True)
    fuel = models.CharField(null = True, max_length = 10)
    gear = models.CharField(null = True, max_length = 10)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "%s %s" % (self.car_model.__str__(), self.version)


class CarOffer (models.Model):

    hashkey = models.CharField(primary_key = True, max_length = 64)
    car_version = models.ForeignKey(CarVersion, on_delete=models.PROTECT)
    # country = models.ForeignKey(Country, on_delete=models.PROTECT)
    link = models.CharField(max_length = 2048, null = True)
    price = models.IntegerField(db_index = True)
    miliage = models.IntegerField()
    timestamp = models.DateTimeField(auto_now = True)
