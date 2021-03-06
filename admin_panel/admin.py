from django.contrib import admin
from .models import Adminside, Customerside, Driverside, Cars, Cardetails, Area, City, Cabdriver, Cabbooking, Carbooking, Driverbooking
# Register your models here.


admin.site.register(Adminside)
admin.site.register(Customerside)
admin.site.register(Driverside)
admin.site.register(Cars)
admin.site.register(Cardetails)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Cabdriver)
admin.site.register(Cabbooking)
admin.site.register(Carbooking)
admin.site.register(Driverbooking)