from django.forms import *
from .models import *
from clientes.models import Cliente

class MikrotikForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Mikrotik
        fields = '__all__'
        labels = {
            'ip': 'Direción Ip',
            'puertoweb': 'Puerto Web',
            'puertoapi': 'Puerto API',
            'puertoapissl': 'Puerto API-SSL',
            'puertossh': 'Puerto SSH',
            'puertotelnet': 'Puerto Telnet',
            'puertowinbox': 'Puerto Winbox',
            'interfazWan': 'Interfaz Wan',
            'interfazlan': 'Interfaz LAN',
            'usuario': 'Usuario',
            'contraseña': 'Contraseña',
            'segmento' : 'Segmentos de red'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre del Mikrotik'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class GrupoCorteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = grupoCorte
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'afacturar': 'Fecha para facturar',
            'apagar': 'Fecha limite de pago',
            'acortar': 'Dia de corte',
            'periodocobrar': 'Periodo a cobrar',
            'hora': 'Hora del corte'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre del Grupo de corte'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class PlanesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = planVelocidad
        fields = '__all__'
        labels = {
            'nombre': 'Nombre del plan',
            'precio': 'Precio',
            'velocidad': 'Velocidad',
            'tipo': 'Tipo de plan',
            'max_limit' : 'Max limit, ejemplo: 10M/10M',
            'burst_limit_download' : 'burst limit download',
            'burst_limit_upload' : 'burst limit upload',
            'limit_at_upload' : 'limit at upload',
            'limit_at_download' : 'limit at download',
            'burst_threshold_upload' : 'burst threshold upload',
            'burst_threshold_download' : 'burst threshold download',
            'burst_time_upload' : 'burst_time_upload',
            'burst_time_download' : 'burst time download',
            'queue_type_upload' : 'queue type upload',
            'queue_type_download' : 'queue_type_upload',
            'parent' : 'parent',
            'priority': 'Priority'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre del Plan de Internet'
                }
            ),
            'velocidad': TextInput(
                attrs={
                    'placeholder': 'En formato: "10M/10M"'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class ServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        segmentos_ip = kwargs.pop('segmentos_ip',[])
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Servicio
        fields = '__all__'
        labels = {
            'cli': 'Cliente',
            'nombre': 'Nombre del servicio',
            'servidor':'Servidor',
            'grupocorte': 'Grupo de corte',
            'tipofactura': 'Tipo de factura',
            'estadoservicio':'Estado del servicio',
            'tiposervicio':'Tipo de servicio',
            'segmentoip' : 'Segmento de IP',
            'ip' : 'IP Address'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre del servicio'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class TestForm(Form):
    cliente = ModelChoiceField(queryset=Cliente.objects.all(), widget=Select(attrs={
        'class':'form-control',
    }))
    servicios = ModelChoiceField(queryset=Servicio.objects.none(), widget=Select(attrs={
        'class':'form-control',
    }))
