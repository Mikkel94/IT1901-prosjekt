from django.shortcuts import render
from .forms import EmployeeForm, ExtraInfoEmployeeForm, BandNeedsForm

# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Concert, Employee, Band

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
                return home(request) # HttpResponseRedirect(reverse('festivalapp:index'))
            else:
                return HttpResponse('ACCOUNT INACTIVE')
        else:
            print('Username: {} \nPassword: {}'.format(username, password))
            return HttpResponse('INVALID CREDENTIALS')
    else:
        return render(request, 'loginsite.html')

@login_required
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
    info = {}
    if request.user.is_authenticated():
            emp = Employee.objects.get(user=request.user)
            if emp.employee_status == 'light_technician':
                info['concerts'] = list(Concert.objects.filter(lightingWork=emp).order_by('date'))
            elif emp.employee_status == 'sound_technician':
                info['concerts'] = list(Concert.objects.filter(soundWork=emp).order_by('date'))
            elif emp.employee_status == 'arranger':
                info['concerts'] = list(Concert.objects.all().order_by('date'))
                # for con in info['concerts']:
                #     con.soundWork=list(con.soundWork)
                #     con.lightingWork=list(con.lightingWork)

    return render(request, 'festivalapp/concert_list.html', info)


@login_required
def home(request):
    info = {}
    if request.user.is_authenticated():
        emp = Employee.objects.get(user=request.user)
        cons = []
        if emp.employee_status == 'light_technician':
            cons = list(Concert.objects.filter(lighting=emp))
        elif emp.employee_status == 'sound_technician':
            cons = list(Concert.objects.filter(soundWork=emp))
        elif emp.employee_status == 'arranger':
            cons = list(Concert.objects.all())

        info = {
            'cons': cons
        }
        return render(request, 'festivalapp/index.html', info)
    return render(request, 'festivalapp/index.html')

@login_required
def manager(request):
    manager = Employee.objects.get(user=request.user)
    if Band.objects.get(manager=manager) != None:
        band = Band.objects.get(manager=manager)
        if request.method == 'POST':
            band_needs = BandNeedsForm(data=request.POST)
            if band_needs.is_valid():
                print(band_needs)
                band.sound_needs = band_needs.cleaned_data['sound_needs']
                band.light_needs = band_needs.cleaned_data['light_needs']
                band.specific_needs = band_needs.cleaned_data['specific_needs']
                band.save()
            else:
                print(band_needs.errors)
        else:
            band_needs = BandNeedsForm()
        return render(request, 'festivalapp/manager.html', {
            'manager_form': band_needs,
            'band': band
})

@login_required
def arranger(request):
    arranger = Employee.objects.get(user=request.user)
    