from typing import Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import redirect
from .models import Cliente
from .forms import *

# Create your views here.
class ClientesListView(ListView):
    model = Cliente
    template_name = 'clientes/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'A ocurrido un error'
            # data = Mikrotik.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aviso = self.request.session.get('aviso')
        if aviso:
            context["aviso"] = aviso
            del self.request.session['aviso']
        context["title"] = 'Listado de clientes'
        context["create_url"] = reverse_lazy('clienteadd')
        context["entity"] = 'Clientes'
        context["list_url"] = reverse_lazy('clientelist')
        context["action"] = 'searchdata'
        return context
    
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/createform.html'
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
                aviso = "¡El cliente se ha creado correctamente!"
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear nuevo cliente'
        context["entity"] = 'clientes'
        context["list_url"] = reverse_lazy('clientelist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear este cliente?'
        return context
    
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'CLientes/createform.html'
    success_url = reverse_lazy('clientelist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                aviso = "¡El cliente se ha editado correctamente!"
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un cliente'
        context["entity"] = 'Clientes'
        context["list_url"] = reverse_lazy('clientelist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar el cliente?'
        return context
    
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/deletecliente.html'
    success_url = reverse_lazy('mikrolist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = "¡El cliente se ha eliminado correctamente!"
            request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un cliente'
        context["entity"] = 'Clientes'
        context["list_url"] = reverse_lazy('clientelist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el cliente'
        return context


class ZonasListView(ListView):
    model = Zona
    template_name = 'clientes/listzonas.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Zona.objects.all():
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
            context["aviso"] = aviso
            del self.request.session['aviso'] 
        context["title"] = 'Listado de clientes'
        context["create_url"] = reverse_lazy('zonasadd')
        context["entity"] = 'Clientes'
        context["list_url"] = reverse_lazy('zonaslist')
        context["action"] = 'searchdata'
        return context
    
class ZonaCreateView(CreateView):
    model = Zona
    form_class = ZonaForm
    template_name = 'clientes/createform.html'
    success_url = reverse_lazy('zonaslist')

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
                aviso = "¡La Zona se ha creado correctamente!"
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear nueva Zona'
        context["entity"] = 'Zonas'
        context["list_url"] = reverse_lazy('zonaslist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear esta Zona?'
        return context

class ZonaUpdateView(UpdateView):
    model = Zona
    form_class = ZonaForm
    template_name = 'CLientes/createform.html'
    success_url = reverse_lazy('zonaslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                aviso = "¡La Zona se ha editado correctamente!"
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de una Zona'
        context["entity"] = 'Zonas'
        context["list_url"] = reverse_lazy('zonaslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar la zona?'
        return context

class ZonaDeleteView(DeleteView):
    model = Zona
    template_name = 'clientes/deletecliente.html'
    success_url = reverse_lazy('zonaslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = "¡La Zona se ha eliminado correctamente!"
            request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de una zona'
        context["entity"] = 'Zona'
        context["list_url"] = reverse_lazy('zonaslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar esta zona'
        return context
