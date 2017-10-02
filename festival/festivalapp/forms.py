from django import forms
from django.contrib.auth.models import User
from .models import Employee, Band

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
        fields = ('light_needs', 'sound_needs')

class CreateNewManagerForm(EmployeeForm):
    pass
    
    def __init__(self):
        super(CreateNewManagerForm, self).__init__(*args, **kwargs)
