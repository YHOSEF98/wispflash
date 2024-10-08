from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from .models import Sale, DetSale
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from inventario.models import Producto
from clientes.models import Cliente

# Create your views here.
class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'facturacion/sale.html'
    success_url = reverse_lazy('sale_list')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                productos = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in productos:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
                # aviso = 'Grupo de corte creado correctamente'
                # request.session['aviso'] = aviso
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cliente_id = vents['cliente']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.producto_id = i['id']
                        det.precio = float(i['precioventa'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = float(i['subtotal'])
                        det.save()

            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Creacion de una factura'
        context["entity"] = 'Ventas'
        context["list_url"] = self.success_url
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear esta factura?'
        return context
    
class SaleListView(ListView):
    model = Sale
    template_name = 'facturacion/listfacturas.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'A ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aviso = self.request.session.get('aviso')
        if aviso:
            context['aviso'] = aviso
            del self.request.session['aviso']
        context["title"] = 'Listado de facturas'
        context["create_url"] = reverse_lazy('sale_create')
        context["entity"] = 'Facturas estandar'
        context["list_url"] = reverse_lazy('sale_list')
        context["action"] = 'searchdata'
        return context
    
class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'facturacion/deletesale.html'
    success_url = reverse_lazy('sale_list')

    # @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                form = self.get_form()
                if form.is_valid():
                    sale = self.get_object()
                    sale.delete()
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de esta factura'
        context["entity"] = 'ventas'
        context["list_url"] = reverse_lazy('sale_list')
        context["action"] = 'delete'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar esta factura'
        return context
    
class SaledetailView(DetailView):
    model = Sale
    template_name = 'facturacion/detailfactura.html'
    
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            sale_id = self.get_object().id
            if action == 'detail_products':
                data = []
                for i in DetSale.objects.filter(sale_id=sale_id):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Detalles de la factura'
        context["entity"] = 'Detalles Factura'
        context["list_url"] = reverse_lazy('sale_list')
        context["action"] = 'detail_products'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el Servidor Mikrotik'
        return context
    
class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'facturacion/sale.html'
    success_url = reverse_lazy('sale_list')

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_details_products(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                item['precio'] = float(i.precio)
                data.append(item)
        except:
            pass

        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                productos = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in productos:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
                # aviso = 'Grupo de corte creado correctamente'
                # request.session['aviso'] = aviso
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.cliente_id = vents['cliente']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.producto_id = i['id']
                        det.precio = float(i['precioventa'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = float(i['subtotal'])
                        det.save()

            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de una factura'
        context["det"] = self.get_details_products()
        context["entity"] = 'Ventas'
        context["list_url"] = self.success_url
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear esta factura?'
        return context
 


