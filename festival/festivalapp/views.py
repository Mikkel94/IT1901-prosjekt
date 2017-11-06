from django.shortcuts import render
from . import forms
from . import models
from datetime import date, time, timedelta
# Login / Logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from time import sleep


# Create your views here.
@login_required
def index(request):
    user = request.user
    return HttpResponseRedirect(reverse('festivalapp:list_concert'))


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
            return render(request, 'invalid_credentials.html')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

    if emp.employee_status == 'LYSTEKNIKER':
        info['concerts'] = list(models.Concert.objects.filter(lighting_work=emp).filter(
            festival__end_date__gte=date.today()).order_by('date'))
    elif emp.employee_status == 'LYDTEKNIKER':
        info['concerts'] = list(models.Concert.objects.filter(sound_work=emp).filter(
            festival__end_date__gte=date.today()).order_by('date'))
    elif emp.employee_status == 'ARRANGER':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__gte=date.today()).order_by('date'))
    elif emp.employee_status == 'MANAGER':
        try:
            band = models.Band.objects.get(manager=emp)
            info['concerts'] = list(
                models.Concert.objects.filter(band=band).filter(festival__end_date__gte=date.today()).order_by(
                    'date'))
        except:
            # HVIS DU IKKE ER MANAGER FOR NOEN BAND SAA KOMMER DU INGEN STEDER
            return HttpResponseRedirect(reverse('festivalapp:index'))
    elif emp.employee_status == 'PR-MANAGER':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__gte=date.today()).order_by('date'))
    elif emp.employee_status == 'BOOKINGANSVARLIG' or emp.employee_status == 'SERVICE MANAGER':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__gte=date.today()).order_by('date'))
    elif emp.employee_status == 'BOOKINGSJEF':
        info['concerts'] = list(
            models.Concert.objects.filter(festival__end_date__lte=date.today()).order_by('date'))
        info['scenes'] = list(
            models.Scene.objects.filter())

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
    if models.Employee.objects.filter(user=request.user, employee_status='BOOKINGANSVARLIG'):
        # booking_responsible = models.Employee.objects.get(user=request.user) # Trenger kanskje senere
        bands = models.Band.objects.filter(is_booked=False)
        light_techs = models.Employee.objects.filter(employee_status='LYSTEKNIKER')
        sound_techs = models.Employee.objects.filter(employee_status='LYDTEKNIKER')
        concert_requests = {}
        for band in bands:
            concert_requests[band.name] = models.ConcertRequest.objects.filter(band=band)
        return render(request, 'festivalapp/booking_responsible.html', {
            'bands': bands,
            'light_techs': light_techs,
            'sound_techs': sound_techs,
            'concert_requests': concert_requests
        })
    else:
        return HttpResponseRedirect(reverse('festivalapp:index'))

@login_required # TODO Whats happening here? Is this even used?
def delete_band(request, pk):
    band = models.Band.objects.get(pk=pk)
    concerts = models.ConcertRequest()
    return index(request)

def get_festival_now(festival_pk):
    return models.Festival.objects.get(pk=festival_pk)

@login_required
def book_band(request, pk):
    band = models.Band.objects.get(pk=pk)
    if request.method == 'POST':
        booking_form = forms.BookBandForm(data=request.POST)
        if booking_form.is_valid():
            scene = booking_form.cleaned_data['scene']
            in_date = booking_form.cleaned_data['date']
            start_time = booking_form.cleaned_data['start_time']
            end_time = booking_form.cleaned_data['end_time']
            all_conserts = models.Concert.objects.filter(
                                scene=scene,
                                date=in_date,
                                start_time__lte=change_time(end_time),
                                )
            all_conserts2 = models.Concert.objects.filter(
                                scene=scene,
                                date=in_date,
                                end_time__gte=start_time
                                )
            if all_conserts or all_conserts2:
                return HttpResponse('Time of date and/or scene not available') # TODO return popup
            festival = models.Festival.objects.get(end_date__gte=date.today())
            concert_request = models.ConcertRequest.objects.create(
                name=booking_form.cleaned_data['name'],
                date=in_date,
                scene=scene,
                genre=booking_form.cleaned_data['genre'],
                price=booking_form.cleaned_data['price'],
                start_time=start_time,
                end_time=end_time,
                band=band,
                festival=festival
            )
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

def available_dates ( festival,end_date ):
    org_date = date.today()
    date_delta = (end_date - org_date).days
    scenes = models.Scene.objects.all()
    date_list = []
    for x in range(date_delta):
        tmp = [str(org_date.year) + ' - ' + str(org_date.month) + ' - ' + str(org_date.day)]
        for scene in scenes:
            concerts = models.Concert.objects.filter(date=org_date,scene=scene)
            if len(concerts) <= 0:
                tmp.append(str(scene))
        date_list.append(tmp)
        org_date += timedelta(days=1)
    return date_list

@login_required
def booking_requests(request):
    concert_requests = models.ConcertRequest.objects.all()
    concert_isbooked = models.Band.objects.filter(is_booked=True)
    avail_num = 0
    a_dates = []
    if models.Festival.objects.filter(end_date__gte=date.today()):
        f = models.Festival.objects.filter(end_date__gte=date.today())[0]
        end_date = f.end_date
        a_dates.append(available_dates(f, end_date))
        avail_num = (end_date - date.today()).days
        avail_num -= len(concert_isbooked)

    return render(request, 'festivalapp/booking_requests.html', {
        'concerts': concert_requests,
        'concerts_isbooked': concert_isbooked,
        'available_dates': avail_num,
        'a_dates': a_dates
    })


@login_required
def send_booking_request(request, pk):
    concert_request = models.Concert.objects.get(pk=pk)
    concert_request.is_sendt = True
    concert_request.save()

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
        price=concert_request.price,
        start_time=concert_request.start_time,
        end_time=concert_request.end_time
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

@login_required
def cancel_booking_request(request, pk):
    models.ConcertRequest.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('festivalapp:booking_responsible'))

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

    for festival in models.Festival.objects.all():
        if (festival.end_date <= date.today()):
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
            concerts.append(models.Concert.objects.filter(band__exact=band).filter(date__lte=date.today()))
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

@login_required
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

# BEGIN assign tech
@login_required  # For bookingansvarlig
def assign_new_tech(request, pk, last_added_or_removed=""):
    user = models.Employee.objects.get(user=request.user)

    if user.employee_status == 'BOOKINGANSVARLIG':
        concert = models.Concert.objects.get(pk=pk)
        band = concert.band
        remaining_needs = 0

        available_light_workers = list()
        available_sound_workers = list()
        for worker in models.Employee.objects.filter(employee_status='LYDTEKNIKER'):
            if is_tech_available(worker, concert):
                available_sound_workers.append(worker)
        for worker in models.Employee.objects.filter(employee_status='LYSTEKNIKER'):
            if is_tech_available(worker, concert):
                available_light_workers.append(worker)

    else:
        return index(request)

    return render(request, 'festivalapp/assign_techs.html',
                  {
                      'remaining_needs': remaining_needs,
                      'band': band,
                      'concert': concert,
                      'light_techs': available_light_workers,
                      'sound_techs': available_sound_workers,
                      'last_added_or_removed': last_added_or_removed
                  })

@login_required  # Også for Bookingansvarlig
def assign_light_tech(request, concert_pk, pk):
    concert = models.Concert.objects.get(pk=concert_pk)
    c = models.Concert.objects.annotate(num_light=Count('lighting_work')).get(pk=concert_pk)
    remaining_needs = concert.band.light_needs - c.num_light
    worker = models.Employee.objects.get(pk=pk)
    if remaining_needs > 0 and worker not in concert.lighting_work.all():
        concert.lighting_work.add(worker)
        concert.save()
        last_added_or_removed = "Lystekniker " + worker.__str__() + " lagt til i konsert: " + concert.__str__()
    elif worker in concert.lighting_work.all():
        concert.lighting_work.remove(worker)
        last_added_or_removed = "Lystekniker " + worker.__str__() + " fjernet fra konsert: " + concert.__str__()
    else:
        last_added_or_removed = "Ingenting skjedde"
    return assign_new_tech(request, concert.pk, last_added_or_removed)

@login_required  # Også for Bookingansvarlig
def assign_sound_tech(request, concert_pk, pk):
    concert = models.Concert.objects.get(pk=concert_pk)
    c = models.Concert.objects.annotate(num_sound=Count('sound_work')).get(pk=concert_pk)
    remaining_needs = concert.band.sound_needs - c.num_sound
    worker = models.Employee.objects.get(pk=pk)
    if remaining_needs > 0 and worker not in concert.sound_work.all():
        concert.sound_work.add(worker)
        concert.save()
        last_added_or_removed = "Lydtekniker " + worker.__str__() + " lagt til i konsert: " + concert.__str__()
    elif worker in concert.sound_work.all():
        concert.sound_work.remove(worker)
        last_added_or_removed = "Lydtekniker " + worker.__str__() + " fjernet fra konsert: " + concert.__str__()
    else:
        last_added_or_removed = "Ingenting skjedde"
    return assign_new_tech(request, concert.pk, last_added_or_removed)

@login_required
def is_tech_available(tech, concert):
    concerts = list()

    for c in models.Concert.objects.filter(date__exact=concert.date):
        if tech in c.sound_work.all() or tech in c.lighting_work.all():
            concerts.append(c)
    if len(concerts) == 1 and concerts[0] == concert:
        return True
    elif len(concerts) >= 1:
        for c in concerts:
            if not (change_time(c.end_time) < change_time(concert.start_time)
                    or change_time(c.start_time) > change_time(concert.end_time)):
                return False
    return True

def change_time(in_time):
    if in_time < time(00, 00, 1):
        return time(23, 59, 59)
    else:
        return in_time

# DEPRECATED
# @login_required
# def assign_tech_to_concert(request, tech_pk, concert_pk):
#     tech = models.Employee.objects.get(pk=tech_pk)
#     concert = models.Concert.objects.get(pk=concert_pk)
#     if tech.employee_status == 'LYSTEKNIKER':
#         concert.lighting_work.add(tech)
#     elif tech.employee_status == 'LYDTEKNIKER':
#         concert.sound_work.add(tech)
#     return index(request)


        # END assign tech
