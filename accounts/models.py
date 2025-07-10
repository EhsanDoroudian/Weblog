from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    male = 'M'
    female = 'F'
    others = 'O'
    GENDERS_CHOICES = {
        male: 'Male',
        female: 'Female',
        others: 'Others',
    }

    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES)


    def __str__(self):
        return self.username