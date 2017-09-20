from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = (
    ('arrangør', 'ARRANGØR'),
    ('lydtekniker', 'LYDTEKNIKER'),
    ('lystekniker', 'LYSTEKNIKER'),
)


class Employee(models.Model):
    user = models.OneToOneField(User)
    employee_status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username


class Band(models.Model):
    name = models.CharField(max_length=60, default="BandX")
    members = models.IntegerField(default=0)


class Scene(models.Model):
    id = models.AutoField(primary_key=True)
    

class Concert(models.Model):
    name = models.CharField(max_length=50)
    bands = models.ForeignKey(Band)
    date = models.DateField()
    scenes = models.ForeignKey(Scene)



