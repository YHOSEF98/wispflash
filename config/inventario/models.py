from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    referecia = models.CharField(max_length=64, null=True, blank=True)
    descripcion = models.TextField()
    preciocompra = models.DecimalField(max_digits=10, decimal_places=2)
    precioventa = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} - {self.precioventa}'
    
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['preciocompra'] = format(self.preciocompra, '.2f')
        item['precioventa'] = format(self.precioventa, '.2F')
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
