from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^forpickup', views.forpickup, name="forpickup"),
    url(r'^startcar', views.startcar, name="startcar"),
    url(r'^verifycustomer', views.verifycustomer, name="verifycustomer"),
    url(r'^fordrop', views.fordrop, name="fordrop"),
    url(r'^endcar', views.endcar, name="endcar"),
    url(r'^verifydrop', views.verifydrop, name="verifydrop"),
    url(r'^forrevert', views.forrevert, name="forrevert"),
    url(r'^viewowner', views.viewowner, name="viewowner"),
    url(r'^revertcar', views.revertcar, name="revertcar"),
    url(r'^godownhome', views.godownhome, name="godownhome")
]