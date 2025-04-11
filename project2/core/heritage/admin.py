#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Place
from .models import HiddenGem
from .models import CulturalEvent

admin.site.register(CulturalEvent)
admin.site.register(HiddenGem)
admin.site.register(Place)
