import geocoder
from decouple import config
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    title = models.SlugField(max_length=30, primary_key=True, unique=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=50)
    description = models.TextField()
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sections')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            g = geocoder.mapbox(self.address, key=config('TOKEN'))
            g = g.latlng
            self.lat = g[0]
            self.long = g[1]
        except TypeError:
            self.lat = 0
            self.long = 0
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Section: {self.title} Category: {self.category}'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='images')


class Poster(models.Model):
    image = models.ImageField(upload_to='poster/')


class ParsingGym(models.Model):
    title = models.CharField(max_length=180)
    address = models.TextField()
    coordinates = models.TextField()
    image = models.ImageField(upload_to='images/')
