from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    referecia = models.CharField(max_length=64, null=True, blank=True)
    descripcion = models.TextField()
    preciocompra = models.DecimalField(max_digits=10, decimal_places=2)
    precioventa = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} - {self.precioventa}'
    
    def tojson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Entradaproducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.IntegerField()
    preciocompra = models.DecimalField(max_digits=10, decimal_places=2)
    facturacompra = models.CharField(max_length=50, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

class Salidaproducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.IntegerField()
    observaciones = models.TextField(null=True, blank=True)
