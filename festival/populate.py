"""
Population script
requires you to already have a superuser
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','festival.settings')

import django
# Import settings
django.setup()

from festivalapp import models
from django.contrib.auth.models import User
from datetime import datetime

def populate():
    user1 = User.objects.create_user('sound', password='heipaadeg24')
    user2 = User.objects.create_user('light', password='heipaadeg24')
    user3 = User.objects.create_user('manager', password='heipaadeg24')
    user4 = User.objects.create_user('arranger', password='heipaadeg24')
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    emp1 = models.Employee.objects.get_or_create(user=user1, employee_status='sound_technician')[0]
    emp2 = models.Employee.objects.get_or_create(user=user2, employee_status='light_technician')[0]
    emp3 = models.Employee.objects.get_or_create(user=user3, employee_status='manager')[0]
    emp4 = models.Employee.objects.get_or_create(user=user4, employee_status='arranger')[0]
    emp1.save()
    emp2.save()
    emp3.save()
    emp4.save()

    scene1 = models.Scene.objects.get_or_create(name='scene1')[0]
    scene2 = models.Scene.objects.get_or_create(name='scene2')[0]
    scene1.save()
    scene2.save()

    band1 = models.Band.objects.get_or_create(
        name='band1',
        manager=emp3,
        members=1,
        light_needs=1,
        sound_needs=1,
        specific_needs='None',
        is_booked=False
    )[0]
    band1.save()

    festival1 = models.Festival.objects.get_or_create(name='festival1', end_date=datetime.today())[0]
    festival1.save()

    concert1 = models.Concert.objects.get_or_create(
        name='concert1',
        band=band1,
        genre='rock',
        audience=100,
        date=datetime.now(),
        scene=scene1,
        lighting_work=emp1,
        sound_work=emp2,
        festival=festival1
    )[0]
    concert1.save()


if __name__ == '__main__':
    populate()