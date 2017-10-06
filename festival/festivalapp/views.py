from django.shortcuts import render
from . import forms
from . import models
import datetime
# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


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
        user_form = forms.EmployeeForm(data=request.POST)
        extra_user_info_form = forms.ExtraInfoEmployeeForm(data=request.POST)
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
        user_form = forms.EmployeeForm()
        extra_user_info_form = forms.ExtraInfoEmployeeForm()

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
            emp = models.Employee.objects.get(user=request.user)
            if emp.employee_status == 'light_technician':
                info['concerts'] = list(models.Concert.objects.filter(lightingWork=emp).order_by('date'))
            elif emp.employee_status == 'sound_technician':
                info['concerts'] = list(models.Concert.objects.filter(soundWork=emp).order_by('date'))
            elif emp.employee_status == 'arranger':
                info['concerts'] = list(models.Concert.objects.all().order_by('date'))
                # for con in info['concerts']:
                #     con.soundWork=list(con.soundWork)
                #     con.lightingWork=list(con.lightingWork)

    return render(request, 'festivalapp/concert_list.html', info)


# @login_required
# def home(request):
#     info = {}
#     if request.user.is_authenticated():
#         emp = models.Employee.objects.get(user=request.user)
#         cons = []
#         if emp.employee_status == 'light_technician':
#             cons = list(models.Concert.objects.filter(lighting_work=emp))
#         elif emp.employee_status == 'sound_technician':
#             cons = list(models.Concert.objects.filter(sound_work=emp))
#         elif emp.employee_status == 'arranger':
#             cons = list(models.Concert.objects.all())
#
#         info = {
#             'cons': cons
#         }
#         return render(request, 'festivalapp/index.html', info)
#     return render(request, 'festivalapp/index.html')

@login_required
def manager(request):
    manager = models.Employee.objects.get(user=request.user)
    if models.Band.objects.get(manager=manager) != None:
        models.Band = models.Band.objects.get(manager=manager)
        if request.method == 'POST':
            band_needs = forms.BandNeedsForm(data=request.POST)
            if band_needs.is_valid():
                print(band_needs)
                models.Band.sound_needs = band_needs.cleaned_data['sound_needs']
                models.Band.light_needs = band_needs.cleaned_data['light_needs']
                models.Band.specific_needs = band_needs.cleaned_data['specific_needs']
                models.Band.save()
            else:
                print(band_needs.errors)
        else:
            band_needs = forms.BandNeedsForm()
        return render(request, 'festivalapp/manager.html', {
            'manager_form': band_needs,
            'models.Band': models.Band
})

@login_required
def booking_responsible(request):
    if models.Employee.objects.filter(user=request.user, employee_status='booking_responsible'):
        #booking_responsible = models.Employee.objects.get(user=request.user) # Trenger kanskje senere
        bands = models.Band.objects.filter(is_booked=False)
        light_techs = models.Employee.objects.filter(employee_status='light_technician')
        sound_techs = models.Employee.objects.filter(employee_status='light_technician')
        return render(request, 'festivalapp/booking_responsible.html', {
            'bands': bands,
            'light_techs': light_techs,
            'sound_techs': sound_techs,
        })
    else:
        return home(request)

@login_required
def assign_tech_to_concert(request, tech_pk, concert_pk):
    tech = models.Employee.objects.get(pk=tech_pk)
    models.Concert = models.Concert.objects.get(pk=concert_pk)
    if tech.employee_status == 'light_technician':
        models.Concert.lighting_work.add(tech)
    elif tech.employee_status == 'sound_technician':
        models.Concert.sound_work.add(tech)
    return home(request)

@login_required
def delete_band(request, pk):
    # pk = models.Band.kwargs['pk'] #Might be this instead
    models.Band.objects.get(pk=pk).delete()
    return home(request)

@login_required
def book_band(request, pk):
    band = models.Band.objects.get(pk=pk)
    if request.method == 'POST':
        booking_form = forms.BookBandForm(data=request.POST)
        if(booking_form.is_valid()):
            genre = booking_form.cleaned_data['genre']
            date = booking_form.cleaned_data['date']
            scene = booking_form.cleaned_data['scene']
            name = models.Band.name + ' models.Concert'
            Concert = models.Concert.objects.get_or_create(
                                                    name=name,
                                                    date=date,
                                                    scene=scene,
                                                    genre=genre,
                                                    band=band,
                                                )
            models.Band.is_booked = True
            models.Concert.save()
        else:
            print(booking_form.errors)
        return reverse('home')
    else:
        booking_form = forms.BookBandForm()
        return render(request, 'festivalapp/booking_form.html', {
            'booking_form': booking_form
        })

@login_required
def show_previous_festivals(request):
    festivals = models.Festival.objects.all()
    today = datetime.datetime.now()
    for models.Festival in festivals:
        if not ((models.Festival.end_date.day < today.day) and
            (models.Festival.end_date.month <= today.month) and
            (models.Festival.end_date.year <= today.year)):
            festivals.delete(models.Festival)
    return render(request, 'festivalapp/old_festivals.html', {
        'festivals': festivals
    })


