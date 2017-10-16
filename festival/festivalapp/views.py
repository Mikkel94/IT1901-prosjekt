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
                return index(request) # HttpResponseRedirect(reverse('festivalapp:index'))
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
    emp = models.Employee.objects.get(user=request.user)


    if emp.employee_status == 'light_technician':
        info['concerts'] = list(models.Concert.objects.filter(lighting_work=emp).filter(festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'sound_technician':
        info['concerts'] = list(models.Concert.objects.filter(sound_work=emp).filter(festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'arranger':
        info['concerts'] = list(models.Concert.objects.filter(festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'manager':
        try:
            band = models.Band.objects.get(manager=emp)
            info['concerts'] = list(models.Concert.objects.filter(band=band).filter(festival__end_date__gte=datetime.date.today()).order_by('date'))
        except:
            #HVIS DU IKKE ER MANAGER FOR NOEN BAND SAA KOMMER DU INGEN STEDER
            return HttpResponseRedirect(reverse('festivalapp:index'))

    return render(request, 'festivalapp/concert_list.html', info)



@login_required
def manager(request):
    manager = models.Employee.objects.get(user=request.user)
    try:
        band = models.Band.objects.get(manager=manager)
        if request.method == 'POST':
            band_needs = forms.BandNeedsForm(data=request.POST)
            if band_needs.is_valid():
                print(band_needs)
                band.sound_needs = band_needs.cleaned_data['sound_needs']
                band.light_needs = band_needs.cleaned_data['light_needs']
                band.specific_needs = band_needs.cleaned_data['specific_needs']
                band.save()
            else:
                print(band_needs.errors)
        else:
            band_needs = forms.BandNeedsForm()
        return render(request, 'festivalapp/manager.html', {
            'manager_form': band_needs,
            'band': band
                      })
    except:
        #HVIS DU IKKE ER MANAGER FOR NOEN BAND SAA KOMMER DU INGEN STEDER
        return HttpResponseRedirect(reverse('festivalapp:index'))


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
        return index(request)

@login_required
def assign_tech_to_concert(request, tech_pk, concert_pk):
    tech = models.Employee.objects.get(pk=tech_pk)
    concert = models.Concert.objects.get(pk=concert_pk)
    if tech.employee_status == 'light_technician':
        concert.lighting_work.add(tech)
    elif tech.employee_status == 'sound_technician':
        concert.sound_work.add(tech)
    return index(request)

@login_required
def delete_band(request, pk):
    # pk = models.Band.kwargs['pk'] #Might be this instead
    models.Band.objects.get(pk=pk).delete()
    return index(request)

def get_festival_now(festival_pk):
    return models.Festival.objects.get(pk=festival_pk)

@login_required
def book_band(request, pk):
    band = models.Band.objects.get(pk=pk)
    print(band)
    if request.method == 'POST':
        booking_form = forms.BookBandForm(data=request.POST)
        if(booking_form.is_valid()):
            genre = booking_form.cleaned_data['genre']
            date = booking_form.cleaned_data['date']
            scene = booking_form.cleaned_data['scene']
            name = booking_form.cleaned_data['name']
            festival = models.Festival.objects.get(end_date__gte=datetime.date.today())
            concert, created = models.Concert.objects.get_or_create(
                                                    name=name,
                                                    date=date,
                                                    scene=scene,
                                                    genre=genre,
                                                    band=band,
                                                    festival=festival)
            band.is_booked = True
            concert.save()
            band.save()
        else:
            print(booking_form.errors)
            return HttpResponse("Invalid Syntax")
        return HttpResponseRedirect(reverse('festivalapp:index'))
    else:
        booking_form = forms.BookBandForm()
        return render(request, 'festivalapp/booking_form.html', {
            'booking_form': booking_form
        })

@login_required
def show_previous_festivals(request):
    festivals = []
    concerts = models.Concert.objects.all()
    today = datetime.datetime.now()

    for festival in models.Festival.objects.all():
        if not ((festival.end_date.day >= today.day) and
            (festival.end_date.month >= today.month) and
            (festival.end_date.year >= today.year)):
            festivals.append(festival)

    return render(request, 'festivalapp/old_festivals.html', {
        'festivals': festivals,
        'genres': models.GENRES,
        'concerts': concerts,
    })

@login_required
def set_audience(request, pk):
    if request.method == 'POST':
        audience = request.POST['audience']
        concert = models.Concert.objects.get(pk=pk)
        concert.audience = audience
        concert.save()
        return HttpResponseRedirect(reverse('festivalapp:index'))

@login_required
def set_albums_and_former_concerts(request, pk):
    if request.method == 'POST':
        albums_sold = request.POST['sold_albums']
        former_concerts = request.POST['former_concerts']
        band = models.Band.objects.get(pk=pk)
        band.sold_albums = albums_sold
        band.former_concerts = former_concerts
        band.save()
        return HttpResponseRedirect(reverse('festivalapp:index'))
    else:
        return index(request)


@login_required
def generate_price(request):
    price = 0



