from django.contrib import admin

from .models import CarModel
from .models import CarVersion
from .models import CarOffer
from .models import Market


admin.site.register(CarModel)
admin.site.register(CarVersion)
admin.site.register(CarOffer)
admin.site.register(Market)
