from django import forms
from django.contrib.auth.models import User
from .models import Employee, Band, Concert

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ExtraInfoEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('employee_status',)


class BandNeedsForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('light_needs', 'sound_needs', 'specific_needs')

class BookBandForm(forms.ModelForm):
    class Meta:
        model = Concert
<<<<<<< HEAD
        fields = ('genre', 'date', 'scene', 'festival')
=======
        fields = ('name', 'genre', 'date', 'scene','festival')
>>>>>>> 76dd607821f4439f2c1fcaca94df85bca41940b7
