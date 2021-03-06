from django.shortcuts import render, redirect
from django.apps import apps
import datetime
from django.db.models import Q

Carbooking = apps.get_model('admin_panel', 'Carbooking')
Cardetails = apps.get_model('admin_panel', 'Cardetails')
Customerside = apps.get_model('admin_panel', 'Customerside')
Area = apps.get_model('admin_panel', 'Area')


# Create your views here.


def godownhome(request):
    return render(request, "godownhome.html")


def forpickup(request):
    a = Cardetails.objects.all().filter(Q(cdIsAvailable="no") | Q(cdIsAvailable="hold"))
    return render(request, "forpickup.html", {"a": a})


def verifycustomer(request):
    if request.method == 'GET':
        carid = request.GET.get('cdID')

        if carid:
            c = Carbooking.objects.all().filter(cdID=carid).filter(carStatus="book")
            if c:
                carbookID = c[0].carbookID
                date = c[0].carDOBook
                pickup = c[0].carPickup

                cid = c[0].customerID
                cd = Customerside.objects.all().filter(customerUname=cid)
                name = cd[0].customerUname
                pic = cd[0].customerPic
                address = cd[0].customerAddress
                cno = cd[0].customerCno
                return render(request, "verifycustomer.html",
                              {"carbookID": carbookID, "date": date, "pickup": pickup, "cid": cid, "name": name,
                               "pic": pic, "address": address, "cno": cno})
            else:
                return render(request, "forpickup.html")


def startcar(request):
    if request.method == 'GET':
        cbid = request.GET.get('carbookID')

        if cbid:
            time = datetime.datetime.now()
            c = Carbooking.objects.get(carbookID=cbid)
            c.carStartTime = time
            c.carStatus = "start"
            c.save()
            return render(request, "godownhome.html")


def fordrop(request):
    a = Cardetails.objects.all().filter(Q(cdIsAvailable="no") | Q(cdIsAvailable="hold"))
    return render(request, "fordrop.html", {"a": a})


def verifydrop(request):
    if request.method == 'GET':
        carid = request.GET.get('cdID')

        if carid:
            request.session['cardetailid'] = carid
            c = Carbooking.objects.all().filter(cdID=carid).filter(carStatus="start")
            if c:
                carbookID = c[0].carbookID
                start = c[0].carStartTime
                end = c[0].carEndTime
                aprox = c[0].carAproxEndTime
                amt = c[0].carAmount
                drop = c[0].carDrop

                cid = c[0].customerID
                cd = Customerside.objects.all().filter(customerUname=cid)
                name = cd[0].customerUname
                pic = cd[0].customerPic
                address = cd[0].customerAddress
                cno = cd[0].customerCno
                return render(request, "verifydrop.html",
                              {"carbookID": carbookID, "start": start, "end": end, "aprox": aprox, "amt": amt,
                               "drop": drop, "name": name, "pic": pic, "address": address, "cno": cno})
            else:
                return render(request, "fordrop.html")


def endcar(request):
    if request.method == 'GET':
        cbid = request.GET.get('carbookID')

        if cbid:
            time = datetime.datetime.now()
            c = Carbooking.objects.get(carbookID=cbid)
            c.carEndTime = time
            c.carStatus = "end"
            c.carAmount = 100
            c.save()

            cid = request.session['cardetailid']
            check = Cardetails.objects.all().filter(cdID=cid)
            status = check[0].cdIsAvailable
            godown = Carbooking.objects.all().filter(carbookID=cbid)
            gdn = godown[0].carDrop

            x = Cardetails.objects.get(cdID=cid)
            if status == "no":
                x.cdIsAvailable = "yes"
            elif status == "hold":
                x.cdIsAvailable = "reverted"
            x.cdGodown = gdn
            x.save()
            return render(request, "godownhome.html")


def forrevert(request):
    a = Cardetails.objects.all().filter(cdIsAvailable="reverted")
    return render(request, "forrevert.html", {"a": a})


def viewowner(request):
    if request.method == 'GET':
        carid = request.GET.get('cdID')

        if carid:
            c = Cardetails.objects.all().filter(cdID=carid)
            cid = c[0].customerID

            cd = Customerside.objects.all().filter(customerUname=cid)
            name = cd[0].customerUname
            pic = cd[0].customerPic
            cno = cd[0].customerCno
            address = cd[0].customerAddress

            return render(request, "viewowner.html",
                          {"carid": carid, "name": name, "pic": pic, "cno": cno, "address": address})


def revertcar(request):
    if request.method == 'GET':
        carid = request.GET.get('cdID')

        if carid:
            c = Cardetails.objects.get(cdID=carid)
            c.cdIsAvailable = "given"
            c.save()
            return render(request, "godownhome.html")
