from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

STATUS_CHOICES = (
    ('arranger', 'ARRANGER'),
    ('sound_technician', 'LYDTEKNIKER'),
    ('light_technician', 'LYSTEKNIKER'),
    ('manager', 'MANAGER'),
    ('booking_responsible', 'BOOKINGANSVARLIG'),
)

GENRES = (
    ('rock', 'ROCK'),
    ('pop', 'POP'),
    ('electric', 'ELECTRIC'),
)


class Employee(models.Model):
    user = models.OneToOneField(User, related_name='user')
    employee_status = models.CharField(max_length=32, choices=STATUS_CHOICES)


    def __str__(self):
        return self.user.username


class Scene(models.Model):
    name = models.CharField(max_length=50, default="Scene")

    def __str__(self):
        return self.name

class Band(models.Model):
    name = models.CharField(max_length=60, null=True)
    manager = models.OneToOneField(Employee, null=True)
    members = models.IntegerField(null = True, default=1)
    light_needs = models.IntegerField(default=0)
    sound_needs = models.IntegerField(default=0)
    specific_needs = models.TextField(default=None)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Festival(models.Model):
    name = models.CharField(max_length=32)
    end_date = models.DateField()
   # concerts = [concert for concert in Concert.objects.all()]
   # total_audience = sum([concert.audience for concert in concerts])

    def __str__(self):
        return self.name


class Concert(models.Model):
    name = models.CharField(max_length=50, default="Concert")
    band = models.ForeignKey(Band)
    genre = models.CharField(max_length=32, choices=GENRES, default=None, null=True)
    audience = models.IntegerField(default=0)
    date = models.DateField()
    scene = models.ForeignKey(Scene)
    lighting_work = models.ManyToManyField(Employee, related_name="lighting", blank=True)
    sound_work = models.ManyToManyField(Employee, related_name="sound", blank=True)
    festival = models.ForeignKey(Festival, blank=True, default=None)


    def __str__(self):
        return self.name + " - " + self.band.name




# class OldFestival(models.Model):
#     festivals = models.ManyToManyField(Festival)
#
#     def __str__(self):
#         return ['Festival name: ' + festival.name + '\nEnd date: ' +
#                 festival.end_date for festival in self.festivals.all()]
