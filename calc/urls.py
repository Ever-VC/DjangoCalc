from django.urls import path
from . import views

urlpatterns = [
    path('punto-fijo/', views.punto_fijo, name='punto_fijo'),
    path('extrapolacion-richardson/', views.extrapolacion_richardson, name='extrapolacion_richardson'),
    path('history/', views.history, name='history'),
    path('history/<int:exercise_id>', views.exercise_delete, name='exercise_delete'),
]