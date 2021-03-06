from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from .forms import profileForm, AddCar, UpdateCar, AddArea, UpdateArea, AddCity, UpdateCity
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Adminside, Customerside, Driverside, Cars, Cardetails, Cabdriver, Area, City, Driverbooking, \
    Carbooking, Cabbooking


# Create your views here.


def index(request):
    return render(request, "index.html")


def header(request):
    return render(request, "header.html")


def login(request):
    if request.method == 'POST':
        auname = request.POST['txtemail']
        apass = request.POST['txtpass']

        a = Adminside.objects.all().filter(Q(adminUname=auname) | Q(adminEmail=auname) | Q(adminCno=auname)).filter(
            adminPass=apass)
        x = a.count()

        if x == 1:
            request.session['uid'] = a[0].adminID
            request.session['uname'] = a[0].adminUname
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
            return render(request, "login.html")
    return render(request, "login.html")


def home(request):
    uid = request.session['uid']
    name = Adminside.objects.all().filter(adminID=uid)
    uname = name[0].adminUname
    return render(request, "home.html", {'app_name': uname, 'tab_name': 'Home'})


def city(request):
    c = City.objects.all()
    return render(request, "city.html", {'city': c})


def addCity(request):
    form = AddCity()
    if request.method == 'POST':
        form = AddCity(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city')
    context = {'form': form}
    return render(request, "addCity.html", context)


def updateCity(request):
    if request.method == 'GET':
        cid = request.GET.get('cityID')
        if cid:
            cd = City.objects.get(cityID=cid)
            form = UpdateCity(instance=cd)
            context = {'form': form}
            return render(request, "updateCity.html", context)
    if request.method == 'POST':
        cid = request.GET.get('cityID')
        cd = City.objects.get(cityID=cid)
        form = UpdateCity(request.POST, instance=cd)
        if form.is_valid():
            form.save()
            return redirect('city')


def deleteCity(request):
    if request.method == 'GET':
        cid = request.GET.get('cityID')

        if cid:
            a = City.objects.get(cityID=cid)
            a.delete()
            return redirect('city')


def area(request):
    a = Area.objects.all()
    return render(request, "area.html", {'area': a})


def addArea(request):
    form = AddArea()
    if request.method == 'POST':
        form = AddArea(request.POST)
        if form.is_valid():
            form.save()
            return redirect('area')
    context = {'form': form}
    return render(request, "addArea.html", context)


def updateArea(request):
    if request.method == 'GET':
        aid = request.GET.get('areaID')
        if aid:
            cd = Area.objects.get(areaID=aid)
            form = UpdateArea(instance=cd)
            context = {'form': form}
            return render(request, "updateArea.html", context)
    if request.method == 'POST':
        aid = request.GET.get('areaID')
        cd = Area.objects.get(areaID=aid)
        form = UpdateArea(request.POST, instance=cd)
        if form.is_valid():
            form.save()
            return redirect('area')


def deleteArea(request):
    if request.method == 'GET':
        aid = request.GET.get('areaID')

        if aid:
            a = Area.objects.get(areaID=aid)
            a.delete()
            return redirect('area')


def cars(request):
    cs = Cars.objects.all()
    return render(request, "cars.html", {"cs": cs})


def updateCar(request):
    if request.method == 'GET':
        cid = request.GET.get('carID')
        if cid:
            cd = Cars.objects.get(carID=cid)
            form = UpdateCar(instance=cd)
            context = {'form': form}
            return render(request, "updateCar.html", context)
    if request.method == 'POST':
        cid = request.GET.get('carID')
        cd = Cars.objects.get(carID=cid)
        form = UpdateCar(request.POST, request.FILES, instance=cd)
        if form.is_valid():
            form.save()
            return redirect('cars')


def addCar(request):
    form = AddCar()
    if request.method == 'POST':
        form = AddCar(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cars')
    context = {'form': form}
    return render(request, "addCar.html", context)


def deleteCar(request):
    if request.method == 'GET':
        cid = request.GET.get('carID')

        if cid:
            a = Cars.objects.get(carID=cid)
            a.delete()
            return redirect('cars')


def cardetails(request):
    if request.method == 'GET':
        cid = request.GET.get('carID')

        if cid:
            cd = Cardetails.objects.all().filter(carID=cid)
            return render(request, "cardetails.html", {"cd": cd})


def customer(request):
    cst = Customerside.objects.all()
    paginator = Paginator(cst, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "customer.html", {"posts": posts, 'page': page})


def fullcstdetail(request):
    if request.method == 'GET':
        cstid = request.GET.get('customerID')

        if cstid:
            cd = Customerside.objects.all().filter(customerID=cstid)
            area = cd[0].customerArea
            city = cd[0].customerCity
            fetcharea = Area.objects.all().filter(areaID=area)
            areaname = fetcharea[0].areaName
            fetchcity = City.objects.all().filter(cityID=city)
            cityname = fetchcity[0].cityName
            return render(request, "fullcstdetail.html", {'cd': cd, 'area': areaname, 'city': cityname})


def driver(request):
    dr = Driverside.objects.all()
    paginator = Paginator(dr, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page, 'posts': posts}
    return render(request, "driver.html", context)


def fulldriverdetail(request):
    if request.method == 'GET':
        did = request.GET.get('did')

        if did:
            cd = Driverside.objects.all().filter(driverID=did)
            area = cd[0].driverArea
            city = cd[0].driverCity
            fetcharea = Area.objects.all().filter(areaID=area)
            areaname = fetcharea[0].areaName
            fetchcity = City.objects.all().filter(cityID=city)
            cityname = fetchcity[0].cityName
            return render(request, "fulldriverdetail.html", {'cd': cd, 'area': areaname, 'city': cityname})


def profile(request):
    uid = request.session['uid']
    admin = Adminside.objects.get(adminID=uid)
    form = profileForm(instance=admin)
    Image = Adminside.objects.all().filter(adminID=uid)
    if request.method == 'POST':
        form = profileForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form, 'img': Image}
    return render(request, "profile.html", context)


def adminregister(request):
    return render(request, "adminregister.html")


def areg(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        mobile = request.POST['mobileno']
        email = request.POST['emailid']
        dob = request.POST['dob']
        gender = request.POST['gender']
        if gender == 'male':
            ugen = gender
        elif gender == 'female':
            ugen = gender
        if pass1 == pass2:
            a = Adminside(adminUname=uname, adminFname=fname, adminLname=lname, adminPass=pass1, adminCno=mobile,
                          adminEmail=email, adminDOB=dob, adminGender=ugen)
            a.save()
            return redirect('login.html')
        else:
            return redirect('login.html')


def cabdriver(request):
    cbs = Cabdriver.objects.all()
    return render(request, "cabdriver.html", {"cbs": cbs})


def dashboard(request):
    labels = []
    data = []

    db = Driverbooking.objects.all()
    cb = Carbooking.objects.all()
    cabb = Cabbooking.objects.all()
    count1 = db.count()
    count2 = cb.count()
    count3 = cabb.count()
    counter = [count1, count2, count3]
    lbl = ['Driverbooking', 'Carbooking', 'Cabbooking']
    for x in counter:
        data.append(x)
    for y in lbl:
        labels.append(y)
    context = {'labels': labels, 'data': data}
    return render(request, "dashboard.html", context)


def hstcar(request):
    cb = Carbooking.objects.all()
    return render(request, "hstcar.html", {'car': cb})


def hstcab(request):
    cb = Cabbooking.objects.all()
    return render(request, "hstcab.html", {'cab': cb})


def hstdriver(request):
    cb = Driverbooking.objects.all()
    return render(request, "hstdriver.html", {'driver': cb})
