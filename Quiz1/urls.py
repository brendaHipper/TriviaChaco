#from django.conf import path
#from django.contrib.auth import login
from django.urls import path

# Incorpora o llama a Views (al archivo que contiene las vistas)
from .views import (
            inicio, 
            registro, 
            loginView, 
            logout_vista, 
            HomeUsuario, 
            jugar,
            resultado_pregunta,
            tablero)

# va contener una lista de urls o rutas. Crea las urls
urlpatterns = [
    path('',inicio, name='inicio'),
    path('HomeUsuario/',HomeUsuario, name='HomeUsuario'),
    path('login/',loginView, name='login'),
    path('logout_vista/',logout_vista, name='logout_vista'),
    path('registro/',registro, name='registro'),
    path('tablero/',tablero, name='tablero'),
    path('jugar/',jugar, name='jugar'),
    path('resultado_pregunta/<int:pregunta_respondida_pk>/',resultado_pregunta, name='resultado'),
]
