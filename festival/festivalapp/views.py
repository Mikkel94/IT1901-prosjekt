from django.shortcuts import render
from .forms import EmployeeForm, ExtraInfoEmployeeForm

# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Concert, Employee

# Create your views here.
@login_required
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
        return render(request, 'loginsite.html')


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

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'loginsite.html')


@login_required
def list_concert(request):
    info = {
        'user': request.user
    }
    if request.user.is_authenticated():
            emp = Employee.objects.get(user=request.user)
            if emp.employee_status == 'light_technician':
                info['concerts'] = list(Concert.objects.filter(lightingWork=emp))
            elif emp.employee_status == 'sound_technician':
                info['concerts'] = list(Concert.objects.filter(soundWork=emp))
            elif emp.employee_status == 'arranger':
                info['concerts'] = list(Concert.objects.all())
                # for con in info['concerts']:
                #     con.soundWork=list(con.soundWork)
                #     con.lightingWork=list(con.lightingWork)

            info['emp'] = emp
    return render(
        request, 'festivalapp/concert_list.html', info
    )


@login_required
def home(request):
    info = {}
    if request.user.is_authenticated():
        emp = Employee.objects.get(user=request.user)
        cons = []
        if emp.employee_status == 'light_technician':
            cons = list(Concert.objects.filter(lighting=emp))
        elif emp.employee_status == 'sound_technician':
            cons = list(Concert.objects.filter(sound=emp))

        info = {
            'cons': cons,
            'user': request.user,
            'emp': emp
        }
        return render(request, 'festivalapp/home.html', info)
    return render(request, 'festivalapp/home.html')

