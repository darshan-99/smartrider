from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.core.mail import send_mail, EmailMultiAlternatives
import datetime
from .forms import resetForm
from django.core.serializers.json import DjangoJSONEncoder

Customerside = apps.get_model('admin_panel', 'Customerside')
Driverside = apps.get_model('admin_panel', 'Driverside')
Cars = apps.get_model('admin_panel', 'Cars')
Cardetails = apps.get_model('admin_panel', 'Cardetails')
Area = apps.get_model('admin_panel', 'Area')
City = apps.get_model('admin_panel', 'City')
Cabdriver = apps.get_model('admin_panel', 'Cabdriver')
Cabbooking = apps.get_model('admin_panel', 'Cabbooking')
Carbooking = apps.get_model('admin_panel', 'Carbooking')
Driverbooking = apps.get_model('admin_panel', 'Driverbooking')


# Create your views here.


def customerlogin(request):
    if request.method == 'POST':
        cuname = request.POST['txtemail']
        cpass = request.POST['txtpass']

        c = Customerside.objects.all().filter(customerUname=cuname).filter(customerPass=cpass)
        x = c.count()

        if x == 1:
            request.session['uid'] = c[0].customerID
            return redirect('customerhome')
        else:
            return render(request, "customerlogin.html")
    return render(request, "customerlogin.html")


def customerhome(request):
    uid = request.session['uid']
    fetch = Customerside.objects.all().filter(customerID=uid)
    name = fetch[0].customerUname
    context = {'app_name': name, 'id': uid}
    return render(request, "customerhome.html", context)


def customerheader(request):
    return render(request, "customerheader.html")


def customercars(request):
    return render(request, "customercars.html")


def rtrip(request):
    return render(request, "rtrip.html")


def fordriver(request):
    dr = Driverside.objects.all().filter(driverIsOwner="no").filter(driverIsAvailable="yes")
    return render(request, "fordriver.html", {"dr": dr})


def dsortR(request):
    drs = Driverside.objects.all().filter(driverIsOwner="no").filter(driverIsAvailable="yes").order_by('-driverRating')
    return render(request, "dsortR.html", {"drs": drs})


def dsortV(request):
    drv = Driverside.objects.all().filter(driverIsOwner="no").filter(driverIsAvailable="yes").order_by('-driverVcnt')
    return render(request, "dsortV.html", {"drv": drv})


def bookdriver(request):
    if request.method == 'GET':
        did = request.GET.get('driverID')

        if did:
            request.session['driverid'] = did
            now = datetime.datetime.now()
            drd = Driverside.objects.all().filter(driverID=did)
            return render(request, "bookdriver.html", {"now": now})


def confirmbookdriver(request):
    dobook = datetime.date.today()
    end = request.POST['aproxdate']
    cstid = request.session['uid']
    cstids = Customerside.objects.get(customerID=cstid)
    cEmail = cstids.customerEmail
    drid = request.session['driverid']
    drids = Driverside.objects.get(driverID=drid)

    a = Driverbooking(driverDOBook=dobook, driverAproxEndTime=end, customerID=cstids, driverID=drids,
                      driverStatus="book")
    a.save()

    c = Driverside.objects.get(driverID=drid)
    c.driverIsAvailable = "no"
    c.save()

    send_mail('driver booking done',
              'thank you for booking a driver ! your driver for a trip is name. mobile number is n ',
              'mailspractice@gmail.com', [cEmail], fail_silently=False)

    return redirect('customerhome')


def forcar(request):
    cid = request.session['uid']
    car = Cardetails.objects.all().filter(~Q(customerID=cid)).filter(cdIsAvailable="yes")
    return render(request, "forcar.html", {"car": car})


def carsort(request):
    cid = request.session['uid']
    cars = Cardetails.objects.all().filter(~Q(customerID=cid)).filter(cdIsAvailable="yes").order_by('-cdFPH')
    return render(request, "carsort.html", {"cars": cars})


def bookcar(request):
    if request.method == 'GET':
        carid = request.GET.get('cdID')

        if carid:
            request.session['carid'] = carid
            now = datetime.datetime.now()
            format_token = now.strftime("%d-%m-%Y %I:%M %p")
            card = Cardetails.objects.all().filter(cdID=carid)
            area = card[0].cdGodown
            a = Area.objects.all()
            context = {"card": card, "now": now, "a": a, "area": area, "min": format_token}
            return render(request, "bookcar.html", context)


def confirmbookcar(request):
    dobook = datetime.date.today()
    end = request.POST['aproxdate']

    drop = request.POST['drop']
    did = Area.objects.get(areaID=drop)

    cstid = request.session['uid']
    cstids = Customerside.objects.get(customerID=cstid)

    carsid = request.session['carid']
    carsids = Cardetails.objects.get(cdID=carsid)
    pickup = Cardetails.objects.all().filter(cdID=carsid)
    pick = pickup[0].cdGodown

    owner = Cardetails.objects.all().filter(cdID=carsid)
    oid = owner[0].customerID
    a = Carbooking(carDOBook=dobook, carAproxEndTime=end, carPickup=pick, carDrop=did, customerID=cstids, ownerID=oid,
                   cdID=carsids, carStatus="book")
    a.save()

    c = Cardetails.objects.get(cdID=carsid)
    c.cdIsAvailable = "no"
    c.save()
    # messsage = 'your car name : ' + carsid
    # send_mail('car booking done', messsage, 'mailspractice@gmail.com',
    #           ['darshansoni14599@gmail.com'], fail_silently=False)

    return render(request, "customerhome.html")


def forcab(request):
    drc = Cabdriver.objects.all().filter(cabIsAvailable="yes")
    return render(request, "forcab.html", {"drc": drc})


def cstcardetails(request):
    if request.method == 'GET':
        cid = request.GET.get('carID')

        if cid:
            cd = Cars.objects.all().filter(carName=cid)
            return render(request, "cstcardetails.html", {"cd": cd})


def bookcab(request):
    if request.method == 'GET':
        cabid = request.GET.get('cabID')

        if cabid:
            now = datetime.datetime.now()
            request.session['cabid'] = cabid
            cabd = Cabdriver.objects.all().filter(cabID=cabid)
            return render(request, "bookcab.html", {"cabd": cabd, "now": now})


def cstconfirmbook(request):
    cabids = request.session['cabid']
    cabidss = Cabdriver.objects.get(cabID=cabids)
    cstid = request.session['uid']
    cstids = Customerside.objects.get(customerID=cstid)
    aproxend = request.POST['aproxdate']
    dobook = datetime.date.today()
    a = Cabbooking(cabDOBook=dobook, cabAproxEndTime=aproxend, customerID=cstids, cabID=cabidss, cabStatus="book")
    a.save()
    c = Cabdriver.objects.get(cabID=cabids)
    c.cabIsAvailable = "no"
    c.save()
    return render(request, "customerhome.html")


def beowner(request):
    c = Cars.objects.all()
    return render(request, "beowner.html", {"c": c})


def confirmowner(request):
    cstid = request.session['uid']
    cstids = Customerside.objects.get(customerID=cstid)
    carid = request.POST['car']
    carids = Cars.objects.get(carID=carid)
    rate = request.POST['rate']
    nplate = request.POST['nplate']

    g = Customerside.objects.all().filter(customerUname=cstids)
    area = g[0].customerArea
    areas = Area.objects.get(areaID=area)
    name = g[0].customerUname
    a = Cardetails(customerID=cstids, carID=carids, cdFPH=rate, cdNumberplate=nplate, cdIsAvailable="yes",
                   cdGodown=areas)
    a.save()

    c = Customerside.objects.get(customerID=cstid)
    c.customerIsOwner = "yes"
    c.save()
    return render(request, "thxaddcar.html",
                  {"uname": name, "cname": carids, "rate": rate, "nplate": nplate, "gdn": areas})


def thxaddcar(request):
    return render(request, "thxaddcar.html")


def cstallcars(request):
    cid = request.session['uid']
    a = Cardetails.objects.all().filter(customerID=cid)
    return render(request, "cstallcars.html", {"a": a})


def cstviewcars(request):
    cid = request.session['uid']
    a = Cardetails.objects.all().filter(customerID=cid).filter(
        ~Q(cdIsAvailable="reverted") & ~Q(cdIsAvailable="given") & ~Q(cdIsAvailable="hold"))
    return render(request, "cstviewcars.html", {"a": a})


def cstrevert(request):
    if request.method == 'GET':
        cardetailid = request.GET.get('cdID')

        if cardetailid:
            x = Cardetails.objects.all().filter(cdID=cardetailid)
            status = x[0].cdIsAvailable
            gdn = x[0].cdGodown
            if status == "yes":
                c = Cardetails.objects.get(cdID=cardetailid)
                c.cdIsAvailable = "reverted"
                c.save()
                return render(request, "revertyes.html", {"gdn": gdn})
            elif status == "no":
                n = Carbooking.objects.all().filter(cdID=cardetailid).filter(Q(carStatus="book") | Q(carStatus="start"))
                gd = n[0].carDrop
                date = n[0].carAproxEndTime
                c = Cardetails.objects.get(cdID=cardetailid)
                c.cdIsAvailable = "hold"
                c.save()
                return render(request, "revertno.html", {"gd": gd, "date": date})


def revertyes(request):
    return render(request, "revertyes.html")


def revertno(request):
    return render(request, "revertno.html")


def yourtrip(request):
    cstid = request.session['uid']
    a = Cabbooking.objects.all().filter(customerID=cstid)

    return render(request, "yourtrip.html", {"a": a})


def chstcab(request):
    cstid = request.session['uid']
    a = Cabbooking.objects.all().filter(customerID=cstid)
    return render(request, "chstcab.html", {"a": a})


def chstcar(request):
    cstid = request.session['uid']
    a = Carbooking.objects.all().filter(customerID=cstid)
    return render(request, "chstcar.html", {"a": a})


def chstdriver(request):
    cstid = request.session['uid']
    a = Driverbooking.objects.all().filter(customerID=cstid)
    return render(request, "chstdriver.html", {"a": a})


def ddetails(request):
    if request.method == 'GET':
        ddid = request.GET.get('did')

        if ddid:
            x = Driverside.objects.all().filter(driverUname=ddid)
            return render(request, "ddetails.html", {'x': x})


def cstcarreport(request):
    cstid = request.session['uid']
    a = Carbooking.objects.all().filter(ownerID=cstid)
    return render(request, "cstcarreport.html", {"a": a})


def customerregister(request):
    arr = []
    a = Area.objects.all()
    c = City.objects.all()

    cars = Cars.objects.all()
    c_list = Customerside.objects.all()
    for x in c_list:
        arr.append(x.customerUname)
    json.dumps(arr)

    context = {"a": a, "c": c, "cars": cars, "c_list": arr}
    return render(request, "customerregister.html", context)


def creg(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        dob = request.POST['dob']

        owner = request.POST['isowner']
        if owner == 'Yes':
            ansowner = owner
        elif owner == 'No':
            ansowner = owner

        aname = request.POST['area']
        cname = request.POST['city']
        address = request.POST['address']
        mobile = request.POST['mobileno']

        gender = request.POST['gender']
        if gender == 'male':
            ugen = gender
        elif gender == 'female':
            ugen = gender

        email = request.POST['emailid']

        if pass1 == pass2:
            b = Customerside.objects.all().filter(customerEmail=email).count()
            if b != 0:
                return render(request, "customerregister.html")
            else:
                if ansowner == 'No':
                    cst = Customerside(customerUname=uname, customerFname=fname, customerLname=lname,
                                       customerPass=pass1,
                                       customerDOB=dob, customerIsOwner=ansowner,
                                       customerArea=aname, customerCity=cname, customerAddress=address,
                                       customerCno=mobile, customerGender=gender, customerEmail=email, customerVcnt=0)
                    cst.save()
                    return render(request, "customerlogin.html")

                else:
                    cst = Customerside(customerUname=uname, customerFname=fname, customerLname=lname,
                                       customerPass=pass1,
                                       customerDOB=dob, customerIsOwner=ansowner,
                                       customerArea=aname, customerCity=cname, customerAddress=address,
                                       customerCno=mobile, customerGender=gender, customerEmail=email, customerVcnt=0)

                    cst.save()

                    cids = Customerside.objects.all().filter(customerEmail=email)
                    cid = cids[0].customerID
                    cidn = Customerside.objects.get(customerID=cid)

                    carids = request.POST['carmodel']
                    carid = Cars.objects.get(carID=carids)

                    fph = request.POST['fph']
                    nplate = request.POST['nplate']
                    ar_name = Area.objects.get(areaID=aname)

                    crd = Cardetails(customerID=cidn, carID=carid, cdFPH=fph, cdNumberplate=nplate, cdIsAvailable="yes",
                                     cdGodown=ar_name)
                    crd.save()
                    return render(request, "customerlogin.html")

        else:
            messages.info(request, "Password not Matching.")
            return redirect('customerregister')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def customerforgotpass(request):
    if request.method == 'POST':
        enteredemail = request.POST['txtemail']
        check = Customerside.objects.all().filter(customerEmail=enteredemail)
        counter = check.count()

        if counter != 0:
            request.session['resetemail'] = enteredemail

            message = render_to_string(template_name='resetlink.html')
            msg = EmailMultiAlternatives('Reset Password', 'text_content', 'mailspractice@gmail.com', [enteredemail])
            msg.attach_alternative(message, "text/html")
            msg.send()

            time_token = datetime.datetime.now()
            expire_token = datetime.datetime.now() + datetime.timedelta(minutes=2)
            format_token = expire_token.strftime("%Y-%m-%d %H:%M:%S")
            expire_tokens = json.dumps(format_token, default=myconverter)
            request.session['expired'] = expire_tokens

            print("exact token is ")
            print("---------------------------")
            print(time_token)
            print("expire token is ")
            print("---------------------------")
            print(expire_tokens)
            messages.success(request, 'Verification Link send, check your mail box')
            return render(request, "customerforgotpass.html")
        else:
            messages.error(request, 'Email is not registered')
            return render(request, "customerforgotpass.html")
    return render(request, "customerforgotpass.html")


def customerresetpass(request):
    email = request.session['resetemail']
    format = '"%Y-%m-%d %H:%M:%S"'
    expire = request.session['expired']
    expired = datetime.datetime.strptime(expire, format)
    now = datetime.datetime.now()
    flag = 0  # not working
    if now.isoformat() < expired.isoformat() and flag == 0:
        if request.method == 'POST':
            password = request.POST['pass']
            cpassword = request.POST['cpass']
            if password == cpassword:
                fetch = Customerside.objects.get(customerEmail=email)
                fetch.customerPass = password
                fetch.save()
                flag += 1
                return redirect('customerlogin')
            else:
                messages.error(request, 'password mismatched')
                return render(request, "customerresetpass.html")

        else:
            context = {'email': email}
            return render(request, "customerresetpass.html", context)
    else:
        return HttpResponse("link expired")  # snapchat jevi system karvani
