from django.db import models
from .choices import *
from clientes.models import Cliente, Zona
from django.forms import model_to_dict

# Create your models here.
class Mikrotik(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    ip = models.CharField(max_length=50, unique=True)
    puertoweb = models.IntegerField()
    puertoapi = models.IntegerField()
    puertoapissl = models.IntegerField(null=True, blank=True)
    puertossh = models.IntegerField(null=True, blank=True)
    puertotelnet = models.IntegerField(null=True, blank=True)
    puertowinbox = models.IntegerField()
    interfazWan = models.CharField(max_length=50, null=True, blank=True)
    interfazlan = models.CharField(max_length=50, null=True, blank=True)
    usuario = models.CharField(max_length=60)
    contraseña = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre} - {self.ip}'
    
    def toJSON(self):
         item = model_to_dict(self)
         return item

    class Meta:
        verbose_name = 'Mikrotik'
        verbose_name_plural = 'Servidores mikrotik'


class Segmentos(models.Model):
    mikro = models.ForeignKey(Mikrotik, on_delete=models.CASCADE)
    segmento = models.CharField(max_length=18)

    class Meta:
        verbose_name = 'Segmento'
        verbose_name_plural = 'Segmentos de red'

    
class grupoCorte(models.Model):
    nombre = models.CharField(max_length=50)
    afacturar = models.CharField(max_length=2, choices=dia_choices)
    apagar = models.CharField(max_length=2, choices=dia_choices)
    acortar = models.CharField(max_length=2, choices=dia_choices)
    periodocobrar = models.CharField(max_length=1, choices=periodo_ACobrar, default='A')
    hora = models.TimeField(default='23:59:59')

    class Meta:
        verbose_name = 'Grupo de corte'
        verbose_name_plural = 'Grupos de corte'

    def __str__(self):
            return f'{self.nombre} - {self.acortar}'
    
class planVelocidad(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    velocidad = models.CharField(max_length=9)
    tipo = models.CharField(max_length=1, choices=tipoPlan, default='R')
    burst_limit = models.CharField(max_length=7, default='0/0')
    limit_at = models.CharField(max_length=7, default='0/0')
    burst_threshold = models.CharField(max_length=13, default='0/0')
    burst_time = models.CharField(max_length=5, default='0s/0s')
    priority = models.CharField(max_length=3, default='8/8')

    class Meta:
        verbose_name = 'Plan de Velocidad'
        verbose_name_plural = 'Planes de Velocidad'

    def __str__(self):
            return f'{self.nombre} - {self.velocidad}'
    
    def toJSON(self):
         item = model_to_dict(self)
         return item

class Servicio(models.Model):
    cli = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    tiposervicio = models.CharField(max_length=12, choices=estado_servicio, default='IP estatica')
    servidor = models.ForeignKey(Mikrotik, on_delete=models.CASCADE)
    plan = models.ForeignKey(planVelocidad, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.CharField(max_length=9, choices=estado_servicio, default='Activo')
    grupocorte = models.ForeignKey(grupoCorte, on_delete=models.CASCADE, blank=True)
    tipofactura = models.CharField(max_length=10, blank=True, null=True)
    coordenas = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
            return f'{self.nombre} - {self.ip}'
    
    def toJSON(self):
         item = model_to_dict(self)
         return item

