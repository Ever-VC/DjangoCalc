from django.urls import path
from . import views

urlpatterns = [
    path('punto-fijo/', views.punto_fijo, name='punto_fijo'),
]