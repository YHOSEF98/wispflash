from django.forms import *
from .models import *

class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'tipodocu': 'Tipo de documento',
            'pais': 'País',
            'codigopostal': 'Codigo postal',
            'correoelectronico': 'Correo electrónico',
            'telefoo': 'Teléfono'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre del Cliente'
                }
            ),
            'correoelectronico': TextInput(
                attrs={
                    'placeholder': 'Correo electrónico'
                }
            ),
            'telefoo': TextInput(
                attrs={
                    'placeholder': 'Teléfono'
                }
            ),
            'celular': TextInput(
                attrs={
                    'placeholder': 'Celular, whatsapp'
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
    
class ZonaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Zona
        fields = '__all__'
        labels = {
            'nombre': 'Nombre'
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Nombre de la Zona'
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
