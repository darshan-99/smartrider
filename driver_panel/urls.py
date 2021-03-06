from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^driverlogin',views.driverlogin, name="driverlogin"),
    url(r'^driverhome',views.driverhome, name="driverhome"),
    url(r'^driverregister', views.driverregister, name="driverregister"),
    url(r'^dreg', views.dreg, name="dreg"),
    url(r'^newtrip', views.newtrip, name="newtrip"),
    url(r'^accepttrip', views.accepttrip, name="accepttrip"),
    url(r'^currenttrip', views.currenttrip, name="currenttrip"),
    url(r'^starttrip', views.starttrip, name="starttrip"),
    url(r'^runningtrip', views.runningtrip, name="runningtrip"),
    url(r'^endtrip', views.endtrip, name="endtrip"),
    url(r'^triphst', views.triphst, name="triphst"),
    url(r'^drivercab', views.drivercab, name="drivercab"),
    url(r'^cabnewtrip', views.cabnewtrip, name="cabnewtrip"),
    url(r'^cabaccepttrip', views.cabaccepttrip, name="cabaccepttrip"),
    url(r'^cabcurrenttrip', views.cabcurrenttrip, name="cabcurrenttrip"),
    url(r'^cabstarttrip', views.cabstarttrip, name="cabstarttrip"),
    url(r'^cabrunningtrip', views.cabrunningtrip, name="cabrunningtrip"),
    url(r'^cabendtrip', views.cabendtrip, name="cabendtrip"),
    url(r'^cabhst', views.cabhst, name="cabhst"),
    url(r'^becabdriver', views.becabdriver, name="becabdriver"),
    url(r'^confirmcabdriver', views.confirmcabdriver, name="confirmcabdriver"),
    url(r'^driverbill', views.driverbill, name="driverbill"),
    url(r'^driverheader',views.driverheader, name="driverheader")
]