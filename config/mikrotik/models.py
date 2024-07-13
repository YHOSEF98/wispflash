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
    segmentos_ip = models.CharField(max_length=150, null=True, blank=True)

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
    max_limit = models.CharField(max_length=7, default='10M/10M')
    burst_limit_download = models.CharField(max_length=7, default='0')
    burst_limit_upload = models.CharField(max_length=7, default='0')
    limit_at_upload = models.CharField(max_length=7, default='0')
    limit_at_download = models.CharField(max_length=7, default='0')
    burst_threshold_upload = models.CharField(max_length=7, default='0')
    burst_threshold_download = models.CharField(max_length=7, default='0')
    burst_time_upload = models.CharField(max_length=5, default='0s')
    burst_time_download = models.CharField(max_length=5, default='0s')
    queue_type_upload = models.CharField(max_length=7, default='default')
    queue_type_download = models.CharField(max_length=7, default='default')
    parent = models.CharField(max_length=50, default='none')
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
    estadoservicio = models.CharField(max_length=9, choices=estado_servicio, default='Activo')
    tiposervicio = models.CharField(max_length=12, choices=tipo_servicio, default='----------')
    servidor = models.ForeignKey(Mikrotik, on_delete=models.CASCADE)
    plan = models.ForeignKey(planVelocidad, on_delete=models.CASCADE)
    segmentoip = models.CharField(max_length=18, blank=True, null=True)
    ip = models.CharField(max_length=15)
    perfil =  models.CharField(max_length=50, blank=True, null=True)
    userpppoe = models.CharField(max_length=50, blank=True, null=True)
    passwordpppoe = models.CharField(max_length=50, blank=True, null=True)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, blank=True, null=True)
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

