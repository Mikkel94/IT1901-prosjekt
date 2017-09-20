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

# concert model

class Concert(models.Model):
    name = models.CharField(max_length=50)
    band = models.CharField(max_length=40)
    date = models.DateField()
    scenes = models.ForeignKey(Scene)

class Scene(models.Model):
    id = models.IntegerField(unique=True)


# concert model end