from django.urls import path
from . import views

urlpatterns = [
    path('solve', views.punto_fijo, name='solve'),
    path('solve/punto-fijo/', views.punto_fijo, name='punto_fijo'),
    path('solve/extrapolacion-richardson/', views.extrapolacion_richardson, name='extrapolacion_richardson'),
    path('history/', views.history, name='history'),
    path('history/<int:exercise_id>', views.exercise_delete, name='exercise_delete'),
]