from datetime import datetime
from django.forms import ModelForm, Select, DateInput
from .models import Sale

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['cliente'].widget.attrs['class'] = 'form-control select2'
        self.fields['cliente'].widget.attrs['autofocus'] = 'true'
        self.fields['cliente'].widget.attrs['style'] = 'width: 100%;'

        self.fields['date_joined'].widget.attrs = {
            'autocomplete':'off',
            'class':'form-control datetimepicker-input',
            'id':'date_joined',
            'data-target':'#date_joined',
            'data-toggle':'datetimepicker'
        }

        self.fields['subtotal'].widget.attrs = {
            'readonly': True,
            'class':'form-control',
        }
        self.fields['total'].widget.attrs = {
            'readonly': True,
            'class':'form-control',
        }
            
    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            ''
            'date_joined': DateInput(
                format='%d-%m-%y',
                attrs={
                    'value': datetime.now().strftime('%d-%m-%y'),
                    'class': 'form-control',
                }
            ),
        }
