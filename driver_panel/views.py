from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.contrib import messages
import datetime

Driverside = apps.get_model('admin_panel', 'Driverside')
Area = apps.get_model('admin_panel', 'Area')
City = apps.get_model('admin_panel', 'City')
Driverbooking = apps.get_model('admin_panel', 'Driverbooking')
Customerside = apps.get_model('admin_panel', 'Customerside')
Cabdriver = apps.get_model('admin_panel', 'Cabdriver')
Cabbooking = apps.get_model('admin_panel', 'Cabbooking')
Cars = apps.get_model('admin_panel', 'Cars')


def driverheader(request):
    return render(request, "driverheader.html")


def driverlogin(request):
    if request.method == "POST":
        duname = request.POST['txtemail']
        dpass = request.POST['txtpass']

        d = Driverside.objects.all().filter(driverUname=duname).filter(driverPass=dpass)
        x = d.count()

        if x == 1:
            if d[0].driverIsOwner == "yes":
                a = Cabdriver.objects.all().filter(driverID=d[0].driverID)
                cabid = a[0].cabID
                request.session['cabsid'] = cabid
                request.session['uid'] = d[0].driverID
                return redirect('driverhome')
            else:
                request.session['uid'] = d[0].driverID
                return redirect('driverhome')
        else:
            return render(request, "driverlogin.html")
    return render(request, "driverlogin.html")


def driverhome(request):
    uid = request.session['uid']
    d = Driverside.objects.all().filter(driverID=uid)
    if d[0].driverIsOwner == "yes":
        cid = request.session['cabsid']
        name = Driverside.objects.all().filter(driverID=uid)
        uname = name[0].driverUname
        return render(request, "driverhome.html", {'app_name': uname, 'tab_name': 'Home', 'cid': cid, 'uid': uid})
    else:
        name = Driverside.objects.all().filter(driverID=uid)
        uname = name[0].driverUname
        return render(request, "driverhome.html", {'app_name': uname, 'tab_name': 'Home', 'uid': uid})


def driverregister(request):
    area = Area.objects.all()
    city = City.objects.all()
    cars = Cars.objects.all()
    return render(request, "driverregister.html", {"area": area, "city": city, "cars": cars})


def dreg(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        dob = request.POST['dob']

        cabdriver = request.POST['cab']
        if cabdriver == 'yes':
            ucab = cabdriver
        elif cabdriver == 'no':
            ucab = cabdriver

        gender = request.POST['gender']
        if gender == 'Male':
            ugen = gender
        elif gender == 'Female':
            ugen = gender
        aname = request.POST['area']
        cname = request.POST['city']
        address = request.POST['address']
        mobile = request.POST['mobileno']
        email = request.POST['emailid']
        fph = request.POST['fph']
        licence = request.POST['license']

        if pass1 == pass2:
            b = Driverside.objects.all().filter(driverEmail=email).count()
            if b != 0:
                return render(request, "driverregister.html")
            else:
                if ucab == 'no':
                    d = Driverside(driverUname=uname, driverFname=fname, driverLname=lname, driverPass=pass1,
                                   driverDOB=dob, driverIsOwner=ucab, driverGender=ugen, driverArea=aname,
                                   driverCity=cname,
                                   driverAddress=address, driverCno=mobile, driverEmail=email, driverFPH=fph,
                                   driverFPKm=0,
                                   driverRating=0, driverVcnt=0, driverLicence=licence, driverIsAuth="yes",
                                   driverIsAvailable="yes")
                    d.save()
                    return redirect('driverlogin')
                else:
                    d = Driverside(driverUname=uname, driverFname=fname, driverLname=lname, driverPass=pass1,
                                   driverDOB=dob, driverIsOwner=ucab, driverGender=ugen, driverArea=aname,
                                   driverCity=cname,
                                   driverAddress=address, driverCno=mobile, driverEmail=email, driverFPH=fph,
                                   driverFPKm=0,
                                   driverRating=0, driverVcnt=0, driverLicence=licence, driverIsAuth="yes",
                                   driverIsAvailable="yes")
                    d.save()

                    dids = Driverside.objects.all().filter(driverEmail=email)
                    did = dids[0].driverID
                    didn = Driverside.objects.get(driverID=did)

                    carids = request.POST['carmodel']
                    carid = Cars.objects.get(carID=carids)

                    cabfpkm = request.POST['fpkm']
                    nplate = request.POST['nplate']

                    cabd = Cabdriver(driverID=didn, carID=carid, cabFPKm=cabfpkm, cabNumberplate=nplate,
                                     cabIsAvailable="yes")
                    cabd.save()
                    return redirect('driverlogin')

        else:
            messages.info(request, "Password not Matching.")
            return redirect('driverregister')


def newtrip(request):
    did = request.session['uid']
    a = Driverbooking.objects.all().filter(driverID=did).filter(driverStatus="book")
    return render(request, "newtrip.html", {"a": a})


def accepttrip(request):
    if request.method == 'GET':
        dbid = request.GET.get('driverBookID')
        if dbid:
            a = Driverbooking.objects.get(driverBookID=dbid)
            a.driverStatus = "accepted"
            a.save()
            return redirect('currenttrip')


def currenttrip(request):
    did = request.session['uid']
    a = Driverbooking.objects.all().filter(driverID=did).filter(driverStatus="accepted")
    if a:
        cid = a[0].customerID
        c = Customerside.objects.all().filter(customerUname=cid)
        address = c[0].customerAddress
        cno = c[0].customerCno
        context = {"a": a, "address": address, "cno": cno}
        return render(request, "currenttrip.html", context)
    else:
        return render(request, "currenttrip.html", {"a": a})


def starttrip(request):
    if request.method == 'GET':
        dbid = request.GET.get('driverBookID')
        if dbid:
            time = datetime.datetime.now()
            a = Driverbooking.objects.get(driverBookID=dbid)
            a.driverStatus = "start"
            a.driverStartTime = time
            a.save()

            return redirect('runningtrip')


def runningtrip(request):
    did = request.session['uid']
    a = Driverbooking.objects.all().filter(driverID=did).filter(driverStatus="start")
    if a:
        cid = a[0].customerID
        c = Customerside.objects.all().filter(customerUname=cid)
        address = c[0].customerAddress
        cno = c[0].customerCno
        context = {"a": a, "address": address, "cno": cno}
        return render(request, "runningtrip.html", context)
    else:
        return render(request, "runningtrip.html", {"a": a})


def endtrip(request):
    if request.method == 'GET':
        dbid = request.GET.get('driverBookID')
        if dbid:
            did = request.session['uid']
            n = Driverbooking.objects.all().filter(driverBookID=dbid)
            name = n[0].customerID
            start = n[0].driverStartTime
            end = datetime.datetime.today()
            format = '%Y-%m-%d %H:%M:%S'
            start_time = datetime.datetime.strftime(start, format)
            end_time = datetime.datetime.strftime(end, format)

            s = datetime.datetime.strptime(start_time, format)
            e = datetime.datetime.strptime(end_time, format)
            diff = e - s
            days = diff.days
            days_to_hours = days * 246
            diff_btw_two_times = diff.seconds / 3600
            overall_hours = days_to_hours + diff_btw_two_times
            fetchrate = Driverside.objects.get(driverID=did)
            fph = fetchrate.driverFPH
            # print(str(overall_hours) + ' hours');
            # print("start: ", s, ":end :", e)

            total = overall_hours * fph

            a = Driverbooking.objects.get(driverBookID=dbid)
            a.driverStatus = "end"
            a.driverEndTime = end
            a.driverAmount = total
            a.save()
            x = Driverside.objects.all().filter(driverID=did)
            rate = x[0].driverFPH
            d = Driverside.objects.get(driverID=did)
            d.driverIsAvailable = "yes"
            d.save()
            context = {"name": name, "start": start, "end": end, "rate": rate, "t": total}
            return render(request, "driverbill.html", context)


def driverbill(request):
    return render(request, "driverbill.html")


def triphst(request):
    did = request.session['uid']
    a = Driverbooking.objects.all().filter(driverID=did).filter(driverStatus="end")
    return render(request, "triphst.html", {"a": a})


def drivercab(request):
    did = request.session['uid']
    a = Cabdriver.objects.all().filter(driverID=did)
    return render(request, "drivercab.html", {"a": a})


def cabnewtrip(request):
    cid = request.session['cabsid']
    a = Cabbooking.objects.all().filter(cabID=cid).filter(cabStatus="book")
    return render(request, "cabnewtrip.html", {"a": a})


def cabaccepttrip(request):
    if request.method == 'GET':
        cbid = request.GET.get('cabbookID')
        if cbid:
            a = Cabbooking.objects.get(cabbookID=cbid)
            a.cabStatus = "accepted"
            a.save()
            return render(request, "driverhome.html")


def cabcurrenttrip(request):
    cid = request.session['cabsid']
    a = Cabbooking.objects.all().filter(cabID=cid).filter(cabStatus="accepted")
    if a:
        cstid = a[0].customerID
        c = Customerside.objects.all().filter(customerUname=cstid)
        address = c[0].customerAddress
        cno = c[0].customerCno
        return render(request, "cabcurrenttrip.html", {"a": a, "address": address, "cno": cno})
    else:
        return render(request, "cabcurrenttrip.html", {"a": a})


def cabstarttrip(request):
    if request.method == 'GET':
        cbid = request.GET.get('cabbookID')
        if cbid:
            time = datetime.datetime.now()
            a = Cabbooking.objects.get(cabbookID=cbid)
            a.cabStatus = "start"
            a.cabStartTime = time
            a.save()
            return render(request, "driverhome.html")


def cabrunningtrip(request):
    cid = request.session['cabsid']
    a = Cabbooking.objects.all().filter(cabID=cid).filter(cabStatus="start")
    if a:
        cstid = a[0].customerID
        c = Customerside.objects.all().filter(customerUname=cstid)
        address = c[0].customerAddress
        cno = c[0].customerCno
        return render(request, "cabrunningtrip.html", {"a": a, "address": address, "cno": cno})
    else:
        return render(request, "cabrunningtrip.html", {"a": a})


def cabendtrip(request):
    if request.method == 'GET':
        cbid = request.GET.get('cabbookID')
        if cbid:
            time = datetime.datetime.now()
            a = Cabbooking.objects.get(cabbookID=cbid)
            a.cabStatus = "end"
            a.cabEndTime = time
            a.cabAmount = 100
            a.save()

            cid = request.session['cabsid']
            d = Cabdriver.objects.get(cabID=cid)
            d.cabIsAvailable = "yes"
            d.save()
            return render(request, "driverhome.html")


def cabhst(request):
    cid = request.session['cabsid']
    a = Cabbooking.objects.all().filter(cabID=cid).filter(cabStatus="end")
    return render(request, "cabhst.html", {"a": a})


def becabdriver(request):
    did = request.session['uid']
    d = Driverside.objects.all().filter(driverID=did)
    a = Cars.objects.all()
    # if d[0].driverIsOwner == "yes":
    #     messages.info(request,'already a cab driver')
    #     return HttpResponseRedirect('driverhome.html')
    # else:
    #     a = Cars.objects.all()
    #     return render(request, "becabdriver.html",{"a":a})
    return render(request, "becabdriver.html", {'a': a, 'd': d})


def confirmcabdriver(request):
    did = request.session['uid']
    dids = Driverside.objects.get(driverID=did)

    cid = request.POST['car']
    cids = Cars.objects.get(carID=cid)

    fair = request.POST['fair']
    nplate = request.POST['nplate']
    a = Cabdriver(driverID=dids, carID=cids, cabFPKm=fair, cabNumberplate=nplate, cabIsAvailable="yes")
    a.save()

    c = Driverside.objects.get(driverID=did)
    c.driverIsOwner = "yes"
    c.save()

    return render(request, "drivercab.html")
