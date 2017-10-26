from django.shortcuts import render
from . import forms
from . import models
import datetime
# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from time import  sleep


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
                return index(request)  # HttpResponseRedirect(reverse('festivalapp:index'))
            else:
                return HttpResponse('ACCOUNT INACTIVE')
        else:
            print('Username: {} \nPassword: {}'.format(username, password))
            return HttpResponse('<meta http-equiv="refresh" content="5;url=http://127.0.0.1:8000/festivalapp/login/">')
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        info['concerts'] = list(models.Concert.objects.filter(lighting_work=emp).filter(
            festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'sound_technician':
        info['concerts'] = list(models.Concert.objects.filter(sound_work=emp).filter(
            festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'arranger':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__gte=datetime.date.today()).order_by('date'))
    elif emp.employee_status == 'manager':
        try:
            band = models.Band.objects.get(manager=emp)
            info['concerts'] = list(
                models.Concert.objects.filter(band=band).filter(festival__end_date__gte=datetime.date.today()).order_by(
                    'date'))
        except:
            # HVIS DU IKKE ER MANAGER FOR NOEN BAND SAA KOMMER DU INGEN STEDER
            return HttpResponseRedirect(reverse('festivalapp:index'))
    elif emp.employee_status == 'pr_manager':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__gte=datetime.date.today()).order_by('date'))

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
        # HVIS DU IKKE ER MANAGER FOR NOEN BAND SAA KOMMER DU INGEN STEDER
        return HttpResponseRedirect(reverse('festivalapp:index'))


@login_required
def booking_responsible(request):
    if models.Employee.objects.filter(user=request.user, employee_status='booking_responsible'):
        # booking_responsible = models.Employee.objects.get(user=request.user) # Trenger kanskje senere
        bands = models.Band.objects.filter(is_booked=False)
        light_techs = models.Employee.objects.filter(employee_status='light_technician')
        sound_techs = models.Employee.objects.filter(employee_status='light_technician')
        return render(request, 'festivalapp/booking_responsible.html', {
            'bands': bands,
            'light_techs': light_techs,
            'sound_techs': sound_techs,
        })
    else:
        return HttpResponseRedirect(reverse('festivalapp:index'))


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
        if booking_form.is_valid():
            genre = booking_form.cleaned_data['genre']
            date = booking_form.cleaned_data['date']
            scene = booking_form.cleaned_data['scene']
            name = booking_form.cleaned_data['name']
            price = booking_form.cleaned_data['price']
            festival = models.Festival.objects.get(end_date__gte=datetime.date.today())
            concert_request = models.ConcertRequest.objects.get_or_create(
                name=name,
                date=date,
                scene=scene,
                genre=genre,
                band=band,
                festival=festival,
                price=price)[0]
            concert_request.save()

            band.is_booking_req_sendt = True
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
def booking_requests(request):
    concert_requests = models.ConcertRequest.objects.all()
    concert_isbooked = models.Band.objects.filter(is_booked=True)
    avail_num = 0
    if models.Festival.objects.filter(end_date__gte=datetime.date.today()):
        f = models.Festival.objects.filter(end_date__gte=datetime.date.today())[0]
        end_date = f.end_date
        avail_num = (end_date - datetime.date.today()).days
        avail_num -= len(concert_isbooked)

    return render(request, 'festivalapp/booking_requests.html', {
        'concerts': concert_requests,
        'concerts_isbooked': concert_isbooked,
        'available_dates': avail_num
    })


@login_required
def accept_booking_request(request, pk):
    concert_request = models.ConcertRequest.objects.get(pk=pk)
    all_concert = models.Concert.objects.all()
    for concert in all_concert:
        if concert.date == concert_request.date and concert.scene == concert_request.scene:
            return HttpResponse('Date occupied')
    concert = models.Concert.objects.get_or_create(
        name=concert_request.name,
        date=concert_request.date,
        scene=concert_request.scene,
        genre=concert_request.genre,
        band=concert_request.band,
        festival=concert_request.festival,
        price=concert_request.price
    )[0]
    band = models.Band.objects.get(pk=concert.band.pk)
    concert.save()
    band.is_booked = True
    band.is_booking_req_sendt = False
    band.save()
    concert_request.delete()
    return HttpResponseRedirect(reverse('festivalapp:booking_requests'))

@login_required
def decline_booking_request(request, pk):
    c = models.ConcertRequest.objects.get(pk=pk)
    c.band.is_booking_req_sendt = False
    c.delete()
    return HttpResponseRedirect(reverse('festivalapp:booking_requests'))

# If manager needs to accept/decline a booking in the system
# @login_required
# def manager_accept_or_decline_booking_request(request, pk, bool):
#     concert = models.Concert.objects.get(pk=pk)
#     band = models.Band.objects.get(pk=concert.band.pk)
#     if not bool:
#         band.is_booked = False
#         band.save()
#         concert.delete()
#     return HttpResponse('<script>alert("Concert %s removed")</script>' % concert)
#


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
    if len(festivals) < 1:
        festivals.append('')

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
def search(request):
    if request.method == 'POST':
        search_input = request.POST['search']
        bands = models.Band.objects.filter(name__contains=search_input)
        concerts = []
        for band in bands:
            concerts.append(models.Concert.objects.filter(band__exact=band).filter(date__lte=datetime.date.today()))
        return render(request, 'festivalapp/search.html', context={
            'concerts': concerts
        })
    else:
        return HttpResponseRedirect(reverse('festivalapp:index'))


@login_required
def generate_price(request, calc=False):
    if calc == "True":

        # 1. regn ut kostnader (loennn + oppsett)
        # 2. regn ut inntekter (80% av scenekapasitet)
        # 3. generer en billettpris basert paa punkt 1 og 2
        # 4. plusser paa et tall eps

        scenes = models.Scene.objects.all()
        scene_prices = []
        for scene in scenes:
            eps = 50
            x = float(scene.capacity)
            tickets_sold_ca = x * 0.8
            loenn = 40000.0
            oppsett = 20000.0
            kostnader = loenn + oppsett
            ticketprice = kostnader / tickets_sold_ca
            ticketprice += eps
            scene_prices.append({
                'scene': scene,
                'capacity': scene.capacity,
                'ticketprice': ticketprice
            })

        return render(request, 'festivalapp/generate_ticketprice.html', {
            'calc': calc,
            'scenes': scene_prices
        })
    else:
        return render(request, 'festivalapp/generate_ticketprice.html')


def add_review(request, pk):
    band = models.Band.objects.get(pk=pk)
    if request.method == 'POST':
        review = request.POST['review']
        print(review)
        if len(review):
            band.review = review
            band.save()
        return HttpResponseRedirect(reverse('festivalapp:index'))
    else:
        return index(request)
