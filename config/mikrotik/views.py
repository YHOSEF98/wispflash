from django.shortcuts import render
from .utils import aplicar_reglas, reiniciar_mikro, create_queue, editar_queue, eliminar_queue, deshabilitar_servicio, apimikrotik
from .utils import apimikrotik
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from unidecode import unidecode
from .models import *
from .forms import *
# Create your views here.

class MikrotikListView(ListView):
    model = Mikrotik
    template_name = 'mikrotik/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Mikrotik.objects.all():
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
            context['aviso'] = aviso
            del self.request.session['aviso']
        context["title"] = 'Listado de servidores MIkrotik'
        context["create_url"] = reverse_lazy('mikroadd')
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'searchdata'
        return context
    
class MikrotikCreateView(CreateView):
    model = Mikrotik
    form_class = MikrotikForm
    template_name = 'mikrotik/createform.html'
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
                aviso = 'Mikrotik creada correctamente'
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear servidor MIkrotik'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear este servidor Mikrotik?'
        return context
    
class MikrotikUpdateView(UpdateView):
    model = Mikrotik
    form_class = MikrotikForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('mikrolist')

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
                aviso = 'La Mikrotik fue actualizada correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un servidor MIkrotik'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar el Servidor Mikrotk?'
        return context
    
class MikrotikDeleteView(DeleteView):
    model = Mikrotik
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('mikrolist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'La Mikrotik ha sido eliminada'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un servidor MIkrotik'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el Servidor Mikrotik'
        return context

class MikrotikDetailView(DetailView):
    model = Mikrotik
    template_name = 'base/detailmikro.html'
    # success_url = reverse_lazy('mikrolist')

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         self.object.delete()
    #     except Exception as e:
    #         data['error'] = str(e)    
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Detalles del servidor MIkrotik'
        context["entity"] = 'Detalles Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'detail'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el Servidor Mikrotik'
        return context

class MikrotikreglasView(DetailView):
    template_name = 'mikrotik/mikroreglas.html'
    model = Mikrotik
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            mikrotik = self.get_object()
            host = mikrotik.ip
            username = mikrotik.usuario
            password = mikrotik.contraseña
            port = mikrotik.puertoapi
            aplicar_reglas(host, username, password, port, data)            
        except Exception as e:
            data['error'] = str(e)    
        return HttpResponseRedirect(reverse('mikrodetail', kwargs={'pk': kwargs['pk']})) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear regla de corte'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de aplicar las reglas de corte?'
        return context

    # def post(self, request, *args, **kwargs):
    #     mikrotik = self.get_object()
    #     host = mikrotik.ip
    #     username = mikrotik.usuario
    #     password = mikrotik.contraseña
    #     port = mikrotik.puertoapi
    #     crear_regla_corte(host, username, password, port)
    #     return HttpResponseRedirect(reverse('detailmikro', kwargs={'pk': kwargs['pk']}))    

class MikrotikreinicioView(DetailView):
    template_name = 'mikrotik/reiniciomikro.html'
    model = Mikrotik
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            reiniciar=apimikrotik()
            mikrotik = self.get_object()
            host = mikrotik.ip
            nombre = mikrotik.nombre
            username = mikrotik.usuario
            password = mikrotik.contraseña
            port = mikrotik.puertoapi
            #reiniciar.reiniciar_mikro(host, username, password, port, data)
            reiniciar_mikro(host, username, password, port, data)
            aviso = f'La Mikrotik {nombre} a sido reiniciada'
            self.request.session['aviso'] = aviso       
        except Exception as e:
            data['error'] = str(e)    
        return HttpResponseRedirect(reverse('mikrodetail', kwargs={'pk': kwargs['pk']})) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Reinicio'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('mikrolist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro reiniciar el Servidor?'
        return context


class GrupoCorteListView(ListView):
    model = grupoCorte
    template_name = 'mikrotik/listgrupoc.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in grupoCorte.objects.all():
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
        context["title"] = 'Listado de grupos de corte'
        context["create_url"] = reverse_lazy('grupocorteadd')
        context["entity"] = 'Grupos de corte'
        context["list_url"] = reverse_lazy('grupocortelist')
        context["action"] = 'searchdata'
        return context
    
class GrupoCorteCreateView(CreateView):
    model = grupoCorte
    form_class = GrupoCorteForm
    template_name = 'mikrotik/createform.html'
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
        context["title"] = 'Crear un nuevo grupo de corte'
        context["entity"] = 'Grupo de corte'
        context["list_url"] = reverse_lazy('grupocortelist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear este Grupo de corte?'
        return context
    
class GrupoCUpdateView(UpdateView):
    model = grupoCorte
    form_class = GrupoCorteForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('grupocortelist')

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
                aviso = 'Grupo de corte actualizado'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un Grupo de corte'
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('grupocortelist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar el Grupo de corte?'
        return context
    
class GrupoCorteDeleteView(DeleteView):
    model = grupoCorte
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('grupocortelist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'El grupo de corte ha sido eliminado'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un grupo de corte'
        context["entity"] = 'Grupo de corte'
        context["list_url"] = reverse_lazy('grupocortelist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el grupo de corte'
        return context


class PlanesListView(ListView):
    model = planVelocidad
    template_name = 'mikrotik/listplanes.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in planVelocidad.objects.all():
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
        context["title"] = 'Listado de planes de velocidad'
        context["create_url"] = reverse_lazy('planesadd')
        context["entity"] = 'Planes'
        context["list_url"] = reverse_lazy('planeslist')
        context["action"] = 'searchdata'
        return context

class PlanesCreateView(CreateView):
    model = planVelocidad
    form_class = PlanesForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('planeslist')

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
                aviso = 'Plan creado correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear un nuevo Plan'
        context["entity"] = 'Planes'
        context["list_url"] = reverse_lazy('planeslist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear plan de servicio?'
        return context    
    
class PlanesUpdateView(UpdateView):
    model = planVelocidad
    form_class = PlanesForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('planeslist')

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
                aviso = 'Plan actualizado correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un plan de internet'
        context["entity"] = 'PLanes'
        context["list_url"] = reverse_lazy('planeslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro este plan?'
        return context
 
class planesDeleteView(DeleteView):
    model = planVelocidad
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('planeslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'Plan eliminado correctamente'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un plan de servicio'
        context["entity"] = 'Grupo de corte'
        context["list_url"] = reverse_lazy('planeslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar este plan'
        return context
    

class ServiciosListView(ListView):
    model = Servicio
    template_name = 'mikrotik/listservicios.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Servicio.objects.all():
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
        context["title"] = 'Listado de serivicios de internet'
        context["create_url"] = reverse_lazy('serivcioadd')
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'searchdata'
        return context

class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServiciosForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('serivcioslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def limpiar_nombre(self, nombre):
        return unidecode(nombre)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    mikro_instance = form.cleaned_data['servidor']
                    plan_instance = form.cleaned_data['plan']
                    host = mikro_instance.ip
                    port = mikro_instance.puertoapi
                    username = mikro_instance.usuario
                    password = mikro_instance.contraseña

                    nombre_limpiado = self.limpiar_nombre(form.cleaned_data['nombre'])
                    form.instance.nombre = nombre_limpiado
                    
                    queue_params = {
                        'name': nombre_limpiado,
                        'target': form.cleaned_data['ip'],
                        'max-limit': plan_instance.velocidad,
                        'limit-at': f'{plan_instance.limit_at_upload}/{plan_instance.limit_at_download}',
                        'priority': plan_instance.priority,
                        'burst-limit': f'{plan_instance.burst_limit_upload}/{plan_instance.burst_limit_download}',
                        'burst-threshold': f'{plan_instance.burst_threshold_upload}/{plan_instance.burst_threshold_download}',
                        'burst-time': f'{plan_instance.burst_time_upload}/{plan_instance.burst_time_download}',
                        'queue': f'{plan_instance.queue_type_upload}/{plan_instance.queue_type_download}',
                        'parent': plan_instance.parent
                    }

                    crear_servicio = apimikrotik(host, username, password, port, data)
                    crear_servicio.create_queue(queue_params)
                    # if form.instance.tiposervicio =='IP estatica':
                    #     crear_servicio.create_queue(queue_params)
                    # else:
                    #     crear_servicio.create_secret_pppoe(secret_nuevo)
                    
                    data = form.save()
                    aviso = 'Servicio creado correctamente'
                    self.request.session['aviso'] = aviso
                
                else:
                    data['error'] = 'El formulario no es válido'

            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear un nuevo Servicio'
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de Crear el nuevo servicio?'
        return context    

class ServicioUpdateView(UpdateView):
    model = Servicio
    form_class = ServiciosForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('serivcioslist')

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
                if form.is_valid():
                    servicio = self.get_object()
                    mikro_instance = form.cleaned_data['servidor']
                    plan_instance = form.cleaned_data['plan']
                    host = mikro_instance.ip
                    username = mikro_instance.usuario
                    password = mikro_instance.contraseña
                    port = mikro_instance.puertoapi
                    queue_name = servicio.nombre
                    target_ip = form.cleaned_data['ip']
                    max_limit = plan_instance.velocidad
                    burst_limit = plan_instance.burst_limit
                    limit_at = plan_instance.limit_at
                    burst_threshold = plan_instance.burst_threshold
                    burst_time = plan_instance.burst_time
                    priority = plan_instance.priority
                    new_name = form.cleaned_data['nombre']
                    
                    editar_queue(host, username, password, port, queue_name, new_name, target_ip, max_limit, burst_limit, limit_at, burst_threshold, burst_time,priority, data)

                    form.save()
                    aviso = 'Servicio editado correctamente'
                    self.request.session['aviso'] = aviso

                else:
                    data['error'] = 'No se pudo actualizar el queue'
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un servicio de internet'
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar este servicio?'
        return context

class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('serivcioslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            servicio = self.get_object()
            host = servicio.servidor.ip
            username = servicio.servidor.usuario
            password = servicio.servidor.contraseña
            port = servicio.servidor.puertoapi
            queue_name = servicio.nombre

            if eliminar_queue(host, username, password, port, queue_name, data):
                self.object.delete()
                aviso = 'Servicio eliminado correctamente'
                self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un servicio'
        context["entity"] = 'Grupo de corte'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar este servicio'
        return context

class DeshabilitarServicioView(DetailView):
    template_name = 'mikrotik/serviciodesh.html'
    model = Servicio
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            servicio = self.get_object()
            host = servicio.servidor.ip
            username = servicio.servidor.usuario
            password = servicio.servidor.contraseña
            port = servicio.servidor.puertoapi
            target_ip = servicio.ip
            queue_name = servicio.nombre
            deshabilitar_servicio(host, username, password, port, target_ip, queue_name, data)            
        except Exception as e:
            data['error'] = str(e)    
        return HttpResponseRedirect(reverse('serivcioslist'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Deshabilitar contrato'
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de deshabilitar este serivcio?'
        return context

class test(TemplateView):
    template_name = 'mikrotik/selec.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_servicio_id':
                data = []
                for i in Servicio.objects.filter(cli_id=request.POST['id']):
                    data.append({'id': i.id, 'nombre': i.nombre})
            else:
                    data['error'] = 'A ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aviso = self.request.session.get('aviso')
        context["title"] = 'Prueba de selec'
        context["action"] = 'search_servicio_id'
        context["form"] = TestForm()
        return context
    


