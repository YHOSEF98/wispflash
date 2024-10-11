from django.shortcuts import render
import logging
from django.views import View
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

logger = logging.getLogger(__name__)

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

class SegmentosIPView(View):
    def get(self, request, *args, **kwargs):
        mikrotik_id = request.GET.get('mikrotik_id')

        if mikrotik_id is None:
            return JsonResponse({'error': 'No se proporcionó ID de Mikrotik'}, status=400)

        try:
            mikrotik_id = int(mikrotik_id)
        except ValueError:
            return JsonResponse({'error': 'ID de Mikrotik inválido'}, status=400)

        try:
            mikrotik = Mikrotik.objects.get(id=mikrotik_id)
            print(f"Mikrotik encontrado: {mikrotik}")
            segmentos = mikrotik.segmentos_ip
            if segmentos:
                segmentos_list = segmentos.split(',')
                choices = [(segmento.strip(), segmento.strip()) for segmento in segmentos_list]
            else:
                choices = []
            
            return JsonResponse({'choices': choices})  # Nota: 'choices', no 'choice'

        except Mikrotik.DoesNotExist:
            return JsonResponse({'error': 'Mikrotik no encontrado'}, status=404)


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
    template_name = 'mikrotik/createformselec.html'
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
                        'target': form.cleaned_data['ip_remote'],
                        'max-limit': plan_instance.velocidad,
                        'limit-at': f'{plan_instance.limit_at_upload}/{plan_instance.limit_at_download}',
                        'priority': plan_instance.priority,
                        'burst-limit': f'{plan_instance.burst_limit_upload}/{plan_instance.burst_limit_download}',
                        'burst-threshold': f'{plan_instance.burst_threshold_upload}/{plan_instance.burst_threshold_download}',
                        'burst-time': f'{plan_instance.burst_time_upload}/{plan_instance.burst_time_download}',
                        'queue': f'{plan_instance.queue_type_upload}/{plan_instance.queue_type_download}',
                        'parent': plan_instance.parent
                    }

                    secret_nuevo = {
                        'name': form.cleaned_data['userpppoe'],
                        'password': form.cleaned_data['passwordpppoe'],
                        'service': 'pppoe',
                        'profile': form.cleaned_data['perfil'],
                        'remote-address':form.cleaned_data['ip_remote'],
                        'local-address':form.cleaned_data['ip_local']
                    }

                    crear_servicio = apimikrotik(host, username, password, port, data)
                    # crear_servicio.create_queue(queue_params)
                    tipo_servicio = form.cleaned_data['tiposervicio']

                    servicio_creado = False
                    try:
                        if tipo_servicio == 'pppoe':
                            servicio_creado = crear_servicio.create_secret_pppoe(secret_nuevo)

                            if servicio_creado:
                                data = form.save()
                                aviso = 'Servicio creado correctamente'
                                self.request.session['aviso'] = aviso

                            else:
                                print("Fallo al crear servicio PPPoE")
                                error_msg = crear_servicio.data.get('error', 'Error desconocido al crear PPPoE')
                                print(f"Error detallado: {error_msg}")
                                data['error'] = error_msg

                                for key, value in crear_servicio.mensaje.items():
                                    print(f"Mensaje de fallo en creación de PPPoE - {key}: {value}")

                        elif tipo_servicio == 'estatica':
                            servicio_creado = crear_servicio.create_queue(queue_params)
                            print("servicio creado por estatica")

                            if servicio_creado:
                                data = form.save()
                                aviso = 'Servicio creado correctamente'
                                self.request.session['aviso'] = aviso

                        
                    
                    except Exception as e:
                        data['error'] = f'Error al crear el servicio: {str(e)}'
                    
                
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
    template_name = 'mikrotik/createformselec.html'
    success_url = reverse_lazy('serivcioslist')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def limpiar_nombre(self, nombre):
        return unidecode(nombre)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    servicio = self.get_object()
                    #datos antes del cambio
                    plan_anterior = servicio.plan
                    mikro_instance_anterior = servicio.servidor
                    host_a = mikro_instance_anterior.ip
                    username_a= mikro_instance_anterior.usuario
                    password_a= mikro_instance_anterior.contraseña
                    port_a = mikro_instance_anterior.puertoapi
                    queue_name_anterior = servicio.nombre
                    usuarioppp_anterior = servicio.userpppoe
                    tipo_servicio_anterior = servicio.tiposervicio
                    nombre_mkt_anterior = mikro_instance_anterior.nombre
                    servicio_eliminado = False
                    delete_servicio_anterior = apimikrotik(host=host_a, username=username_a, password=password_a, port=port_a, data=data)
                    
                    #datos para el cambio
                    mikro_instance = form.cleaned_data['servidor']
                    plan_instance = form.cleaned_data['plan']
                    host = mikro_instance.ip
                    nombre_mkt_nueva = mikro_instance.nombre
                    username = mikro_instance.usuario
                    password = mikro_instance.contraseña
                    port = mikro_instance.puertoapi
                    queue_name = servicio.nombre
                    usuarioppp = servicio.userpppoe
                    nombre_limpiado = self.limpiar_nombre(form.cleaned_data['nombre'])
                    form.instance.nombre = nombre_limpiado

                    if nombre_mkt_anterior !=   nombre_mkt_nueva:
                        try:
                            if tipo_servicio_anterior == "pppoe":
                                delete_servicio_anterior.eliminar_secret_ppp(usuarioppp=usuarioppp_anterior, data=data)
                            elif tipo_servicio_anterior == 'estatica':
                                delete_servicio_anterior.eliminar_queue(queue_name=queue_name_anterior)

                        except Exception as e:
                            aviso1 = 'el servicio no fue eliminado de la mikrotik'
                            self.request.session['aviso'] = aviso1
                    else:
                        pass


                    queue_params = {
                        'name': nombre_limpiado,
                        'target': form.cleaned_data['ip_remote'],
                        'max-limit': plan_instance.velocidad,
                        'limit-at': f'{plan_instance.limit_at_upload}/{plan_instance.limit_at_download}',
                        'priority': plan_instance.priority,
                        'burst-limit': f'{plan_instance.burst_limit_upload}/{plan_instance.burst_limit_download}',
                        'burst-threshold': f'{plan_instance.burst_threshold_upload}/{plan_instance.burst_threshold_download}',
                        'burst-time': f'{plan_instance.burst_time_upload}/{plan_instance.burst_time_download}',
                        'queue': f'{plan_instance.queue_type_upload}/{plan_instance.queue_type_download}',
                        'parent': plan_instance.parent
                    }
                    
                    secret_params = {
                        'name': form.cleaned_data['userpppoe'],
                        'password': form.cleaned_data['passwordpppoe'],
                        'service': 'pppoe',
                        'profile': form.cleaned_data['perfil'],
                        'remote-address':form.cleaned_data['ip_remote'],
                        'local-address':form.cleaned_data['ip_local']
                    }
                    servicio_editado = False
                    edit_service = apimikrotik(host, username, password, port, data)
                    tipo_servicio = form.cleaned_data['tiposervicio']
                    try:
                        if tipo_servicio == 'pppoe':
                            servicio_editado = edit_service.editar_secret_pppoe(usuarioppp, secret_params,data)

                            if servicio_editado:
                                form.save()
                                aviso = 'Servicio editado correctamente'
                                self.request.session['aviso'] = aviso

                            else:
                                print("Fallo al editar el servicio PPPoE")
                                data['error'] = "Fallo al editar el servicio PPPoE"

                                # for key, value in edit_service.mensaje.items():
                                #     print(f"Mensaje de fallo en creación de PPPoE - {key}: {value}")

                        elif tipo_servicio == 'estatica':
                            servicio_editado = edit_service.editar_queue(self, queue_name, queue_params, data)
                            print("servicio creado por estatica")

                            if servicio_editado:
                                form.save()
                                aviso = 'Servicio creado correctamente'
                                self.request.session['aviso'] = aviso
                            
                            else:
                                print("Fallo al editar el servicio")
                                data['error'] = "Fallo al editar el servicio"

                    except Exception as e:
                        data['error'] = str(e)

                    # form.save()
                    # aviso = 'Servicio editado correctamente'
                    # self.request.session['aviso'] = aviso

                else:
                    data['error'] = 'No se pudo actualizar el servicio'
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
                    servicio = self.get_object()
                    host = servicio.servidor.ip
                    username = servicio.servidor.usuario
                    password = servicio.servidor.contraseña
                    port = servicio.servidor.puertoapi
                    queue_name = servicio.nombre
                    tipo_servicio = servicio.tiposervicio
                    servicio_eliminado = False
                    usuarioppp = servicio.userpppoe

                    delete_service = apimikrotik(host, username, password, port, data)
                    try:
                        if tipo_servicio == "pppoe":
                            servicio_eliminado = delete_service.eliminar_secret_ppp(usuarioppp, data)

                            if servicio_eliminado:
                                self.object.delete()
                                aviso = 'Servicio eliminado correctamente'
                                self.request.session['aviso'] = aviso
                            else:
                                self.object.delete()
                                aviso = 'Servicio eliminado de la db pero no de la mikrotik'
                                self.request.session['aviso'] = aviso

                        elif tipo_servicio == "estatica":
                            servicio_eliminado = delete_service.eliminar_queue(queue_name)

                            if servicio_eliminado:
                                self.object.delete()
                                aviso = 'Servicio eliminado correctamente'
                                self.request.session['aviso'] = aviso

                            else:
                                self.object.delete()
                                aviso = 'Servicio eliminado de la db pero no de la mikrotik'
                                self.request.session['aviso'] = aviso


                    except Exception as e:
                        data['error'] = str(e)

                    # delete_queue = apimikrotik(host, username, password, port, data)
                    # delete_queue.eliminar_queue(queue_name)
                    # self.object.delete()
                    # aviso = 'Servicio eliminado correctamente'
                    # self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un servicio'
        context["entity"] = 'Grupo de corte'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'delete'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar este servicio'
        return context


class DeshabilitarServicioView2(UpdateView):
    template_name = 'mikrotik/serviciodesh.html'
    model = Servicio
    fields = ['estadoservicio']
    success_url = reverse_lazy('serivcioslist')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']
            if action == 'desh':
                form = self.get_form()
                if form.is_valid():
                    servicio = self.get_object()
                    instance_mikro = servicio.servidor
                    host = instance_mikro.ip
                    username = instance_mikro.usuario
                    password = instance_mikro.contraseña
                    port = instance_mikro.puertoapi
                    target_ip = servicio.ip_remote
                    queue_name = servicio.nombre
                    deshabilitar_S = apimikrotik(host, username, password, port, data)
                    # deshabilitar_servicio(self, target_ip, target_ip)
                    servicio_desh = False
                    address_list = "Morosos"
                    estado_servicio = servicio.estadoservicio
                    print(estado_servicio)
                    if estado_servicio == "Activo":
                        servicio_desh=deshabilitar_S.deshabilitar_servicio(target_ip, queue_name, address_list)

                        if servicio_desh:
                            servicio.estadoservicio = "Inactivo"
                            servicio.save()
                            aviso = 'Servicio deshabilitado correctamente'
                            self.request.session['aviso'] = aviso

                        else:
                            aviso = 'Error al deshabilitar el servicio'
                            self.request.session['aviso'] = aviso

                    elif estado_servicio == "Inactivo":
                        servicio.estadoservicio = "Inactivo"
                        servicio.save()
                        aviso = 'El servicio ya se encuentra deshabilitado'
                        self.request.session['aviso'] = aviso  
                    
                    else:
                        aviso = 'El servicio no se encuentra en el estado activo o inactivo y no se deshabilito'
                        self.request.session['aviso'] = aviso
        
        except Exception as e:
            data['error'] = f'Error al deshabilitar el servicio: {str(e)}'

        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Deshabilitar contrato'
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'desh'
        context["content_jqueryConfirm"] = '¿Estas seguro de deshabilitar este serivicio?'
        return context
    
class HabilitarServicioView(UpdateView):
    template_name = 'mikrotik/serviciodesh.html'
    model = Servicio
    fields = ['estadoservicio']
    success_url = reverse_lazy('serivcioslist')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']
            if action == 'hab':
                form = self.get_form()
                if form.is_valid():
                    servicio = self.get_object()
                    instance_mikro = servicio.servidor
                    host = instance_mikro.ip
                    username = instance_mikro.usuario
                    password = instance_mikro.contraseña
                    port = instance_mikro.puertoapi
                    target_ip = servicio.ip_remote
                    queue_name = servicio.nombre
                    address_list = "Servicios_autorizados"
                    habilitar_S = apimikrotik(host, username, password, port, data)
                    # deshabilitar_servicio(self, target_ip, target_ip)
                    servicio_hab = False
                    estado_servicio = servicio.estadoservicio
                    print(estado_servicio)
                    if estado_servicio == "Inactivo":
                        servicio_hab=habilitar_S.habilitar_servicio(target_ip, queue_name, address_list)

                        if servicio_hab:
                            servicio.estadoservicio = "Activo"
                            servicio.save()
                            habilitar_S.close()
                            aviso = 'Servicio habilitado correctamente'
                            self.request.session['aviso'] = aviso

                        else:
                            aviso = 'Error al habilitar el servicio'
                            self.request.session['aviso'] = aviso

                    elif estado_servicio == "Activo":
                        servicio.estadoservicio = "Activo"
                        servicio.save()
                        aviso = 'El servicio ya se encuentra habilitado'
                        self.request.session['aviso'] = aviso  
                    
                    else:
                        aviso = 'El servicio no se encuentra en el estado activo o inactivo y no se deshabilito'
                        self.request.session['aviso'] = aviso
        
        except Exception as e:
            data['error'] = f'Error al deshabilitar el servicio: {str(e)}'

        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Habilitar contrato'
        context["entity"] = 'Servicios'
        context["list_url"] = reverse_lazy('serivcioslist')
        context["action"] = 'hab'
        context["content_jqueryConfirm"] = '¿Estas seguro de habilitar este serivicio?'
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


class NodoCreateView(CreateView):
    model = Nodo
    form_class = NodoForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('nodo_list')

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
                aviso = 'Nodo creado correctamente'
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear nuevo nodo'
        context["entity"] = 'Nodo'
        context["list_url"] = reverse_lazy('nodo_list')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de crear este nodo?'
        return context

class NodoUpdateView(UpdateView):
    model = Nodo
    form_class = NodoForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('nodo_list')

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
                aviso = 'El nodo fue actualizada correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un Nodo'
        context["entity"] = 'Nodo'
        context["list_url"] = reverse_lazy('nodo_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar el Nodo?'
        return context

class NodoListView(ListView):
    model = Nodo
    template_name = 'mikrotik/nodo/nodolist.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Nodo.objects.all():
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
        context["create_url"] = reverse_lazy('nodo_list')
        context["entity"] = 'Mikrotik'
        context["list_url"] = reverse_lazy('nodo_list')
        context["action"] = 'searchdata'
        return context

class NodoDeleteView(DeleteView):
    model = Nodo
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('nodo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'El nodo ha sido eliminado'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un servidor nodo'
        context["entity"] = 'Nodo'
        context["list_url"] = reverse_lazy('nodo_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el Nodo'
        return context


class AccespointCreateView(CreateView):
    model = Accesspoint
    form_class = AccesspointForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('accespoint_list')

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
                aviso = 'Acces point creado correctamente'
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear nuevo Acces Point'
        context["entity"] = 'Access Point'
        context["list_url"] = reverse_lazy('accespoint_list')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de crear este Access Point?'
        return context

class AccespointListView(ListView):
    model = Accesspoint
    template_name = 'mikrotik/nodo/accespointlist.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Nodo.objects.all():
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
        context["title"] = 'Listado de Access Point'
        context["create_url"] = reverse_lazy('accespoint_add')
        context["entity"] = 'Access point'
        context["list_url"] = reverse_lazy('accespoint_list')
        context["action"] = 'searchdata'
        return context

class AccespointUpdateView(UpdateView):
    model = Accesspoint
    form_class = AccesspointForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('accespoint_list')

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
                aviso = 'El access point fue actualizada correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de un Accespoint'
        context["entity"] = 'Access Point'
        context["list_url"] = reverse_lazy('accespoint_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar el access point?'
        return context

class AccespointDeleteView(DeleteView):
    model = Accesspoint
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('accespoint_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'El acces point ha sido eliminado'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de un servidor Acces Point'
        context["entity"] = 'Access point'
        context["list_url"] = reverse_lazy('accespoint_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar el Access Point'
        return context


class TorreListView(ListView):
    model = Torre
    template_name = 'mikrotik/nodo/torreslist.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Nodo.objects.all():
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
        context["title"] = 'Listado de Torres'
        context["create_url"] = reverse_lazy('torre_add')
        context["entity"] = 'Torres'
        context["list_url"] = reverse_lazy('torres_list')
        context["action"] = 'searchdata'
        return context

class TorreCreateView(CreateView):
    model = Torre
    form_class = TorreForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('torres_list')

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
                aviso = 'Torre creada correctamente'
                request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Crear nuevo Acces Point'
        context["entity"] = 'Nodo'
        context["list_url"] = reverse_lazy('torres_list')
        context["action"] = 'add'
        context["content_jqueryConfirm"] = '¿Estas seguro de crear esta torre?'
        return context

class TorreUpdateView(UpdateView):
    model = Torre
    form_class = TorreForm
    template_name = 'mikrotik/createform.html'
    success_url = reverse_lazy('torres_list')

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
                aviso = 'La torre fue actualizada correctamente'
                self.request.session['aviso'] = aviso
            else:
                data['error']= 'No entro por ninguna opcion'
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de una Torre'
        context["entity"] = 'Torres'
        context["list_url"] = reverse_lazy('torres_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = '¿Estas seguro de editar la torre?'
        return context

class TorreDeleteView(DeleteView):
    model = Torre
    template_name = 'mikrotik/deletemikrotik.html'
    success_url = reverse_lazy('torres_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            aviso = 'La torre ha sido eliminada'
            self.request.session['aviso'] = aviso
        except Exception as e:
            data['error'] = str(e)    
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Eliminacion de una Torre'
        context["entity"] = 'Torres'
        context["list_url"] = reverse_lazy('torres_list')
        context["action"] = 'edit'
        context["content_jqueryConfirm"] = 'Estas seguro de eliminar la torre'
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
    


