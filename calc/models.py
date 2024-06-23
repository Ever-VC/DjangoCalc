from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calculator_History(models.Model):
    # DATOS GENERALES
    method = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    # DATOS PARA RESOLVER PUNTO FIJO
    fx = models.CharField(max_length=200) # Campo obligatorio (se usa en todos los métodos)
    gx = models.CharField(max_length=200, blank=True) # Puede ser None (no se usa en todos los métodos)
    verify_convergence = models.BooleanField(default=False)
    x0 = models.FloatField() # Campo obligatorio (se usa en todos los métodos)
    error = models.FloatField(null=True, blank=True) # Puede ser None (no se usa en todos los métodos)
    max_iter = models.IntegerField(null=True, blank=True) # Puede ser None (no se usa en todos los métodos)
    decimals = models.IntegerField(null=True, blank=True) # Puede ser None (no se usa en todos los métodos)

    # DATOS PARA RESOLVER RICHARDSON (el fx y x0 ya está en el punto fijo)
    h = models.FloatField(null=True, blank=True) # Puede ser None (no se usa en todos los métodos)
    order = models.IntegerField(null=True, blank=True) # Puede ser None (no se usa en todos los métodos)

    # VINCULA CON EL USUARIO QUE LO CREÓ
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Si se elimina el usuario, se elimina el registro
