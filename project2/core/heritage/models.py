#from django.db import models

# Create your models here.
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    region = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    etiquette = models.TextField()
    #festival_date = models.CharField(max_length=200, blank=True)
    festival_date = models.DateField(null=True, blank=True)
    qr_info_link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class HiddenGem(models.Model):
    place_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    why_hidden = models.TextField()
    best_time_to_visit = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    approved = models.BooleanField(default=False)  # Optional for admin moderation

    def __str__(self):
        return self.place_name

class CulturalEvent(models.Model):
   title = models.CharField(max_length=100)
   date = models.DateField()
   color = models.CharField(max_length=7, blank=True, null=True)  # optional HEX color

   def __str__(self):
       return self.title


    

