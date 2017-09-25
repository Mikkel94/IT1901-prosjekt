from django.shortcuts import render
from .forms import EmployeeForm, ExtraInfoEmployeeForm

# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Concert

# Create your views here.
def index(request):
    return render(request, 'festivalapp/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('festivalapp:index'))
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


def list_concert(request):
    info = {}
    if request.user.is_authenticated():
            info = {
                'concerts': list(Concert.objects.all()),
                'user': request.user,
            }
    return render(
        request, 'festivalapp/concert_list.html', info
    )

