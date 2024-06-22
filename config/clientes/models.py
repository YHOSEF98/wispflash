from django.db import models
from .choices import *
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL


# Create your models here.
class Zona(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    image = models.ImageField(upload_to='clientes/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

    def __str__(self):
        return f'{self.nombre}'
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def toJSON(self):
         item = model_to_dict(self)
         return item
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipodocu = models.CharField(max_length=3, choices=tipodocu, default='CC')
    documento = models.CharField(max_length=50, unique=True)
    pais = models.CharField(max_length=50, blank=True)
    departamento = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=50, blank=True)
    codigopostal = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    corregimiento = models.CharField(max_length=50, blank=True)
    barrio = models.CharField(max_length=50, blank=True)
    correoelectronico= models.EmailField()
    telefoo = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombre} - {self.documento}'
    
    def toJSON(self):
         item = model_to_dict(self)
         return item