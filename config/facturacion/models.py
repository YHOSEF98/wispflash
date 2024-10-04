from django.db import models
from clientes.models import Cliente
from inventario.models import Producto
from datetime import datetime
from django.forms import model_to_dict


# Create your models here.
#factura del servicio

class Sale(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cliente.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['subtotal'] = self.subtotal
        item['iva'] = self.iva
        item['total'] = self.total
        return item
    
class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['producto'] = self.producto.nombre
        item['precio'] = self.precio
        item['cantidad'] = self.cantidad
        item['subtotal'] = self.subtotal
        return item
    

