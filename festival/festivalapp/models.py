from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User)
    employee_status = models.CharField(max_length=32)

    def __str__(self):
        return self.user.username