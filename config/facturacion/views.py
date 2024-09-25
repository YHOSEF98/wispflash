from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from .models import Sale
from .forms import *

# Create your views here.
class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'facturacion/sale.html'
    success_url = reverse_lazy('mikrolist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                aviso = 'Grupo de corte creado correctamente'
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Creacion de una venta'
        context["entity"] = 'Ventas'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear esta venta?'
        return context