from django.db import models
from .choices import *
from clientes.models import Cliente, Zona
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL

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

class PerfilPpp(models.Model):
    mikrotik = models.ForeignKey(Mikrotik, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    local_address = models.CharField(max_length=15, null=True, blank=True)
    remote_address = models.CharField(max_length=15, null=True, blank=True)
    dns1 = models.CharField(max_length=15, null=True, blank=True)
    dns2 = models.CharField(max_length=15, null=True, blank=True)
    change_tcp_mss = models.CharField(max_length=7, choices=no_yes, default='default')
    use_upnp = models.CharField(max_length=7, choices=no_yes, default='default')
    use_mpls = models.CharField(max_length=9, choices=no_yes_requiered, default='default')
    use_compression = models.CharField(max_length=9, choices=no_yes_requiered, default='default')
    use_encryption = models.CharField(max_length=9, choices=no_yes_requiered, default='default')
    rate_limit = models.CharField(max_length=9, default='10M/10M')
    only_one = models.CharField(max_length=7, choices=no_yes, default='default')

    class Meta:
        verbose_name = 'Perfil PPPoE'
        verbose_name_plural = 'Perfiles PPPoE'

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
    ip_remote = models.CharField(max_length=15)
    ip_local = models.CharField(max_length=15, blank=True, null=True)
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

class Nodo(models.Model):
    nombre = models.CharField(max_length=50)
    mikrotik = models.ForeignKey(Mikrotik, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.DO_NOTHING, null=True, blank=True)
    coordenadas = models.CharField(max_length=50, null=True, blank=True)
    publicas_recibidas = models.CharField(max_length=150, null=True, blank=True)
    recepcion = models.CharField(choices=recepcio_s, max_length=20, default='FO')
    equipo_proveedor = models.CharField(max_length=50, null=True, blank=True)
    imagen_equipo_proveedor = models.ImageField(upload_to='Nodo/%Y/%m/%d', null=True, blank=True)
    equipo_propio = models.CharField(max_length=50, null=True, blank=True)
    imagen_equpo_propio = models.ImageField(upload_to='Nodo/%Y/%m/%d', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
            verbose_name = 'Nodo'
            verbose_name_plural = 'Nodos'

    def __str__(self):
            return f'{self.nombre}'
    
    def get_imagen_equipo_proveedor(self):
        if self.imagen_equipo_proveedor:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
        
    def get_imagen_equipo_propio(self):
        if self.imagen_equpo_propio:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
        
    def toJSON(self):
            item = model_to_dict(self)
            return item
     
class Torre(models.Model):
    nombre = models.CharField(max_length=50)
    nodo = models.ForeignKey(Nodo, on_delete=models.CASCADE)
    estacion_ip = models.CharField(max_length=15)
    zona = models.ForeignKey(Zona, on_delete=models.DO_NOTHING, null=True, blank=True)
    coordenadas = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
         verbose_name = 'Torres'
         verbose_name_plural = 'Torres'

    def __str__(self):
         return f'{self.nombre}-{self.nodo}'
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
class Accesspoint(models.Model):
     nombre = models.CharField(max_length=50)
     ip = models.CharField(max_length=15)
     image = models.ImageField(upload_to='accesspoint/%Y/%m/%d', null=True, blank=True)
     ssid = models.CharField(max_length=50)
     seguridad = models.CharField(max_length=50)
     nodo = models.ForeignKey(Nodo, on_delete=models.DO_NOTHING, null=True, blank=True)
     torre =  models.ForeignKey(Torre, on_delete=models.DO_NOTHING, null=True, blank=True)
     descripcion = models.TextField(null=True, blank=True)

     class Meta:
         verbose_name = 'Acess Point'
         verbose_name_plural = 'Acess Points'

     def __str__(self):
         return f'{self.nombre}'
    
     def get_image(self):
         if self.image:
             return '{}{}'.format(MEDIA_URL, self.image)
         return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
     def toJSON(self):
        item = model_to_dict(self)
        return item


