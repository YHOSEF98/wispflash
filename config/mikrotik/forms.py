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
            'contraseña': 'Contraseña'
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
            'nombre': 'Nombre',
            'precio': 'Precio',
            'velocidad': 'Velocidad',
            'tipo': 'Tipo de plan',
            'burst_limit': 'Burst limit',
            'limit_at': 'Limit at',
            'burst_threshold': 'Burst threshold',
            'burst_time': 'Burst time',
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
            'tipofactura': 'Tipo de factura'
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
