from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^index', views.index, name="index"),
    url(r'^home', views.home, name="home"),
    url(r'^login', views.login, name="login"),
    url(r'^cardetails', views.cardetails, name="cardetails"),
    url(r'^cars', views.cars, name="cars"),
    url(r'^city', views.city, name="city"),
    url(r'^addCity', views.addCity, name="addCity"),
    url(r'^updateCity', views.updateCity, name="updateCity"),
    url(r'^deleteCity', views.deleteCity, name="deleteCity"),
    url(r'^area', views.area, name="area"),
    url(r'^addArea', views.addArea, name="addArea"),
    url(r'^updateArea', views.updateArea, name="updateArea"),
    url(r'^deleteArea', views.deleteArea, name="deleteArea"),
    url(r'^customer', views.customer, name="customer"),
    url(r'^fullcstdetail', views.fullcstdetail, name="fullcstdetail"),
    url(r'^driver', views.driver, name="driver"),
    url(r'^fulldriverdetail', views.fulldriverdetail, name="fulldriverdetail"),
    url(r'^profile', views.profile, name="profile"),
    url(r'^adminregister', views.adminregister, name="adminregister"),
    url(r'^areg', views.areg, name="areg"),
    url(r'^cabdriver', views.cabdriver, name="cabdriver"),
    url(r'^header', views.header, name="header"),
    url(r'^addCar', views.addCar, name="addCar"),
    url(r'^updateCar', views.updateCar, name="updateCar"),
    url(r'^deleteCar', views.deleteCar, name="deleteCar"),
    url(r'^hstcar', views.hstcar, name="hstcar"),
    url(r'^hstcab', views.hstcab, name="hstcab"),
    url(r'^hstdriver', views.hstdriver, name="hstdriver"),
    url(r'^dashboard', views.dashboard, name="dashboard")
]