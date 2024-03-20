# Andres Rua y Juan Esteban Pavas
from django.db import models

#para Usuario defecto de django
from django.contrib.auth.models import AbstractUser
from django.db import models


class Libro(models.Model):
    Titulo = models.CharField(max_length=255)
    Autor = models.CharField (max_length= 100)
    ISBN = models.IntegerField()
    Numero_paginas = models.IntegerField()
    Editorial = models.CharField (max_length= 290)
    Fecha_publicacion = models.DateTimeField()
    precio = models.IntegerField()

    def _str_(self):
        return self.titulo


class Nota(models.Model):
    titulo_nota=models.CharField(max_length=100)
    contenido_nota=models.TextField()
    fecha_creacion=models.DateTimeField()
    fecha_modificacion=models.DateTimeField()

    def _str_(self):
        return self.titulo_nota
    

class Review(models.Model):
    Titulo_Review = models.CharField(max_length = 100)
    Contenido_Review = models.TextField()
    Fecha_Review = models.DateTimeField()



class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('Admin', 'Admin'),
        ('Cliente', 'Cliente'),
    ]
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO_CHOICES)
    
    # Agrega estos campos con related_name único
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    
class Recordatorio(models.Model):
    #id
    titulo = models.CharField(max_length = 40)
    nota_adicional = models.TextField()
    fecha = models.DateTimeField()
    