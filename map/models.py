from django.db import models
import geocoder

token = 'pk.eyJ1IjoiYW1vbnlhIiwiYSI6ImNsZDFkZmtibDBiZXczbm1wMWNmaXNtNDgifQ.zdiIZ8oySKdSFYwcpPs-uQ'

# Create your models here.
class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)
