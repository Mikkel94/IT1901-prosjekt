from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

STATUS_CHOICES = (
    ('arranger', 'ARRANGØR'),
    ('sound_technician', 'LYDTEKNIKER'),
    ('light_technician', 'LYSTEKNIKER'),
)

class Employee(models.Model):
    user = models.OneToOneField(User)
    employee_status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username


class AppUser(AbstractUser):
    grp = models.CharField(max_length=128, choices=STATUS_CHOICES)

    def __str__(self):
        return self.username

#
# class Scene(models.Model):
#     name = models.CharField(max_length=32, unique=True)
#
#     def __str__(self):
#         return self.name
#
# class Band(models.Model):
#     name = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.name
#
#
# class Concert(models.Model):
#     band = models.ForeignKey(Band)
#     play_time = models.DateTimeField()
#     scene = models.ForeignKey(Scene)
#
#     def __str__(self):
#         return self.band
#






