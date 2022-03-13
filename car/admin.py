from django.contrib import admin

from .models import CarModel
from .models import CarVersion
from .models import CarOffer
from .models import Market
from .models import Search
from .models import SearchLog


admin.site.register(CarModel)
admin.site.register(CarVersion)
admin.site.register(CarOffer)
admin.site.register(Market)
admin.site.register(Search)
admin.site.register(SearchLog)
