from django.shortcuts import render
from .forms import EmployeeForm, ExtraInfoEmployeeForm

# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.
def index(request):
    return render(request, 'festivalapp/index.html')

@login_required
def arranger(request):
    return render(request, 'festivalapp/arranger.html')

@login_required
def light_technician(request):
    return render(request, 'festivalapp/light_technician.html')

@login_required
def sound_technician(request):
    return render(request, 'festivalapp/sound_technician.html')

@login_required
def manager(request):
    return render(request, 'festivalapp/manager.html')

@login_required
def booking_boss(request):
    return render(request, 'festivalapp/booking_boss.html')

@login_required
def booking_supervisor(request):
    return render(request, 'festivalapp/booking_supervisor.html')

@login_required
def all_login_page(request):
    return render(request, 'festivalapp/after_login.html')

def after_login(request, user):
    if user.groups.filter(name='arranger').exists():
        return arranger(request)
    elif user.groups.filter(name='light_technician').exists():
        return light_technician(request)
    elif user.groups.filter(name='sound_technician').exists():
        return sound_technician(request)
    elif user.groups.filter(name='manager').exists():
        return manager(request)
    elif user.groups.filter(name='booking_boss').exists():
        return booking_boss(request)
    elif user.groups.filter(name='booking_supervisor').exists():
        return booking_supervisor(request)
    else:
        return HttpResponse('Something fishy')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('festivalapp:all_login_page'))
            else:
                return HttpResponse('ACCOUNT INACTIVE')
        else:
            print('Username: {} \nPassword: {}'.format(username, password))
            return HttpResponse('INVALID CREDENTIALS')
    else:
        return render(request, 'festivalapp/login.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = EmployeeForm(data=request.POST)
        extra_user_info_form = ExtraInfoEmployeeForm(data=request.POST)
        if user_form.is_valid() and extra_user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            extra_user_info = extra_user_info_form.save(commit=False)
            extra_user_info.user = user
            user.save()
            extra_user_info.save()
            registered = True
        else:
            print(user_form.errors, extra_user_info_form.errors)
    else:
        user_form = EmployeeForm()
        extra_user_info_form = ExtraInfoEmployeeForm()

    return render(request, 'festivalapp/register.html', {
        'user_form': user_form,
        'extra_info_user_form': extra_user_info_form,
        'registered': registered
    })