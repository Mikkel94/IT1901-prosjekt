from django.db import models

# Create your models here.
class Band(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Concert(models.Model):
    band = models.OneToOneField(Band)

    def __str__(self):
        return self.band.name

