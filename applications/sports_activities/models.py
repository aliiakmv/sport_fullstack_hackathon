from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainers')


class SportsActivity(models.Model):
    title = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='activities')
    price = models.PositiveIntegerField()
