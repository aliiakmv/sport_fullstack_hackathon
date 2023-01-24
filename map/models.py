from django.db import models
import geocoder
from decouple import config

from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    title = models.SlugField(max_length=30, primary_key=True, unique=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sections')
    address = models.TextField()
    coordinate_lat = models.FloatField(blank=True, null=True)
    coordinate_long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'Section: {self.title} Category: {self.category}'

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=config('TOKEN'))
        g = g.latlng
        self.coordinate_lat = g[0]
        self.coordinate_long = g[1]
        return super(Section, self).save(*args, **kwargs)


class ParsingGym(models.Model):
    title = models.CharField(max_length=180)
    address = models.TextField()
    coordinate_lat = models.FloatField(blank=True, null=True)
    coordinate_long = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='images')


class Poster(models.Model):
    image = models.ImageField(upload_to='poster/')
