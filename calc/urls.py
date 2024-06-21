from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index, name='home'),
    path('punto-fijo/', views.punto_fijo, name='punto_fijo'),
]