from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

STATUS_CHOICES = (
    ('arranger', 'ARRANGER'),
    ('sound_technician', 'LYDTEKNIKER'),
    ('light_technician', 'LYSTEKNIKER'),
    ('manager', 'MANAGER'),

)


class Employee(models.Model):
    user = models.OneToOneField(User, related_name='user')
    employee_status = models.CharField(max_length=32, choices=STATUS_CHOICES)


    def __str__(self):
        return self.user.username


class Scene(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
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

    def __str__(self):
        return self.name



class Concert(models.Model):
    name = models.CharField(max_length=50, default="Concert")
    band = models.ForeignKey(Band)
    date = models.DateField()
    scene = models.ForeignKey(Scene)
    lightingWork = models.ManyToManyField(Employee, related_name="lighting")
    soundWork = models.ManyToManyField(Employee, related_name="sound")

    def __str__(self):
        return self.name + " - " + self.band.name



