from django.contrib import admin
from .models import Employee, Concert, Band, Scene

# Register your models here.
admin.site.register(Employee)
admin.site.register(Concert)
admin.site.register(Band)
admin.site.register(Scene)