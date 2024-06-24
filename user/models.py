from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relación uno a uno con la tabla User
    profile_img = models.ImageField(upload_to='profile_images', blank=True, null=True) # Imagen de perfil

    def __str__(self):
        return self.user.username