from __future__ import unicode_literals
from django.db import models


# Create your models here.


class City(models.Model):
    cityID = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=20)

    def __str__(self):
        return self.cityName


class Area(models.Model):
    areaID = models.AutoField(primary_key=True)
    areaName = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    cityID = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.areaName


class Adminside(models.Model):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )
    adminID = models.AutoField(primary_key=True)
    adminUname = models.CharField(max_length=25, blank=True, unique=True)
    adminFname = models.CharField(max_length=25)
    adminLname = models.CharField(max_length=25)
    adminPass = models.CharField(max_length=25)
    adminPic = models.ImageField(null=True, upload_to='static/adminimages', verbose_name='adminPic')
    adminCno = models.CharField(max_length=12, unique=True)
    adminEmail = models.EmailField(max_length=30, unique=True)
    adminDOB = models.DateField()
    adminGender = models.CharField(max_length=10, choices=gender)

    def __str__(self):
        return str(self.adminID) + ' -- ' + self.adminUname + ' -- ' + self.adminPass


class Customerside(models.Model):
    customerID = models.AutoField(primary_key=True)
    customerUname = models.CharField(max_length=20, unique=True)
    customerFname = models.CharField(max_length=20)
    customerLname = models.CharField(max_length=20)
    customerPass = models.CharField(max_length=20)
    customerPic = models.CharField(max_length=20, default="customer.png")
    customerDOB = models.DateField()
    customerIsOwner = models.CharField(default="", max_length=10)
    customerArea = models.IntegerField()
    customerCity = models.IntegerField()
    customerAddress = models.CharField(max_length=50)
    customerCno = models.CharField(max_length=12)
    customerGender = models.CharField(max_length=20)
    customerEmail = models.EmailField(max_length=30)
    customerDOJ = models.DateTimeField(auto_now_add=True)
    customerVcnt = models.IntegerField(null=True)

    def __str__(self):
        return self.customerUname


class Driverside(models.Model):
    status = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    driverID = models.AutoField(primary_key=True)
    driverUname = models.CharField(max_length=25)
    driverFname = models.CharField(max_length=25)
    driverLname = models.CharField(max_length=25)
    driverPass = models.CharField(max_length=25)
    driverPic = models.CharField(max_length=25, default="driver.png")
    driverDOB = models.DateField()
    driverIsOwner = models.CharField(default="", max_length=10)
    driverGender = models.CharField(max_length=25)
    driverArea = models.IntegerField()
    driverCity = models.IntegerField()
    driverAddress = models.CharField(max_length=50)
    driverCno = models.CharField(max_length=12)
    driverEmail = models.EmailField(max_length=30)
    driverDOJ = models.DateTimeField(auto_now_add=True)
    driverDOA = models.DateTimeField(auto_now_add=True, null=True)
    driverFPH = models.IntegerField(null=True)
    driverFPKm = models.IntegerField(null=True)
    driverRating = models.CharField(default="", max_length=10)
    driverVcnt = models.IntegerField(null=True)
    driverLicence = models.CharField(max_length=20)
    driverIsAuth = models.CharField(max_length=10)
    driverIsAvailable = models.CharField(max_length=20, choices=status)

    def __str__(self):
        return self.driverUname


class Cars(models.Model):
    carID = models.AutoField(primary_key=True)
    carName = models.CharField(max_length=30)
    carCompany = models.CharField(max_length=20)
    carType = models.CharField(max_length=30)
    carCapacity = models.IntegerField()
    carPic = models.ImageField(null=True, upload_to='static/carimages', verbose_name='carPic')

    def __str__(self):
        return self.carName


class Cardetails(models.Model):
    status = (
        ('yes', 'yes'),
        ('no', 'no'),
        ('reverted', 'reverted'),
        ('hold', 'hold'),
        ('given', 'given'),
    )
    cdID = models.AutoField(primary_key=True)
    customerID = models.ForeignKey(Customerside, on_delete=models.CASCADE)
    carID = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True)
    cdFPKm = models.IntegerField(null=True)
    cdFPH = models.IntegerField(null=True)
    cdNumberplate = models.CharField(max_length=20, default="")
    cdIsAvailable = models.CharField(max_length=10, choices=status)
    cdGodown = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.customerID) + ' -- ' + str(self.carID) + ' -- ' + self.cdNumberplate


class Cabdriver(models.Model):
    status = (
        ('yes', 'yes'),
        ('no', 'no'),
    )
    cabID = models.AutoField(primary_key=True)
    driverID = models.ForeignKey(Driverside, on_delete=models.CASCADE)
    carID = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True)
    cabFPKm = models.IntegerField(null=True)
    cabNumberplate = models.CharField(max_length=20)
    cabIsAvailable = models.CharField(max_length=20, choices=status)

    def __str__(self):
        return str(self.driverID) + ' -- ' + str(self.carID)


class Cabbooking(models.Model):
    status = (
        ('book', 'book'),
        ('accepted', 'accepted'),
        ('start', 'start'),
        ('end', 'end'),
    )
    cabbookID = models.AutoField(primary_key=True)
    cabDOBook = models.DateField()
    cabStartTime = models.DateTimeField(null=True)
    cabEndTime = models.DateTimeField(null=True)
    cabAproxEndTime = models.DateTimeField()
    cabAmount = models.IntegerField(null=True)
    customerID = models.ForeignKey(Customerside, on_delete=models.CASCADE)
    cabID = models.ForeignKey(Cabdriver, on_delete=models.CASCADE)
    cabStatus = models.CharField(max_length=10, choices=status)

    def __str__(self):
        return str(self.customerID) + ' -- ' + str(self.cabID)


class Carbooking(models.Model):
    status = (
        ('book', 'book'),
        ('start', 'start'),
        ('end', 'end'),
    )
    carbookID = models.AutoField(primary_key=True)
    carDOBook = models.DateField()
    carStartTime = models.DateTimeField(null=True)
    carEndTime = models.DateTimeField(null=True)
    carAproxEndTime = models.DateTimeField()
    carAmount = models.IntegerField(null=True)
    carPickup = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="pick")
    carDrop = models.ForeignKey(Area, on_delete=models.CASCADE)
    customerID = models.ForeignKey(Customerside, on_delete=models.CASCADE, related_name='who_use')
    ownerID = models.ForeignKey(Customerside, on_delete=models.CASCADE)
    cdID = models.ForeignKey(Cardetails, on_delete=models.CASCADE)
    carStatus = models.CharField(max_length=10, choices=status)

    def __str__(self):
        return str(self.cdID)


class Driverbooking(models.Model):
    status = (
        ('book', 'book'),
        ('accepted', 'accepted'),
        ('start', 'start'),
        ('end', 'end')
    )
    driverBookID = models.AutoField(primary_key=True)
    driverDOBook = models.DateField()
    driverStartTime = models.DateTimeField(null=True)
    driverEndTime = models.DateTimeField(null=True)
    driverAproxEndTime = models.DateTimeField()
    driverAmount = models.IntegerField(null=True)
    customerID = models.ForeignKey(Customerside, on_delete=models.CASCADE)
    driverID = models.ForeignKey(Driverside, on_delete=models.CASCADE)
    driverStatus = models.CharField(max_length=20, choices=status)
