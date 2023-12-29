from django import forms
from appbroker.models import *

class PropiedadesForm(forms.ModelForm):
    class Meta:
        model = Propiedades
        fields = '__all__'
        widgets = {
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'baños': forms.NumberInput(attrs={'class': 'form-control'}),
            'balcon': forms.Select(attrs={'class': 'form-control'}),
            'pileta': forms.Select(attrs={'class': 'form-control'}),
            'garage': forms.Select(attrs={'class': 'form-control'}),
            'valor_alquiler': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_venta': forms.TextInput(attrs={'class': 'form-control'}),
            'expensas': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContratosForm(forms.ModelForm):
    class Meta:
        model = Contratos
        fields = '__all__'
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-control'}),
            'inquilino': forms.Select(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_alquiler': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs): # Cargo los datos existentes de propiedades, inquilinos y propietarios para elegir en el formulario
        super(ContratosForm, self).__init__(*args, **kwargs)
        self.fields['propiedad'].queryset = Propiedades.objects.all()
        self.fields['inquilino'].queryset = Inquilinos.objects.all()
        self.fields['propietario'].queryset = Propietarios.objects.all()

class PersonaForm(forms.ModelForm): # Ya que inquilinos, propietarios y compradores son personas, creo este formulario y luego a los otros les agrego el field [propiedades] para que cada uno tenga sus propiedades vinculadas
    class Meta:
        model = Persona
        fields = ['nombre', 'documento', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PropietariosForm(PersonaForm):
        class Meta(PersonaForm.Meta):
            model = Propietarios
            fields = PersonaForm.Meta.fields + ['propiedades']
            widgets = PersonaForm.Meta.widgets
            widgets.update({
                'propiedades': forms.SelectMultiple(attrs={'class': 'form-control'}), # Permito la selección de 1 o más propiedades que pueda poseer el propietario
            })

        def __init__(self, *args, **kwargs):
            super(PropietariosForm, self).__init__(*args, **kwargs)
            self.fields['propiedades'].queryset = Propiedades.objects.all() # Cargo las propiedades existentes en la base de datos

class InquilinosForm(PersonaForm):
    class Meta(PersonaForm.Meta):
        model = Inquilinos
        widgets = PersonaForm.Meta.widgets