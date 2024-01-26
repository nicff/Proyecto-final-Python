from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
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
            'propietario': forms.Select(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super(PropiedadesForm, self).__init__(*args, **kwargs)
            self.fields['propietario'].queryset = Propietarios.objects.all()

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
            widgets = PersonaForm.Meta.widgets

        def __init__(self, *args, **kwargs):
            super(PropietariosForm, self).__init__(*args, **kwargs)

class InquilinosForm(PersonaForm):
    class Meta(PersonaForm.Meta):
        model = Inquilinos
        widgets = PersonaForm.Meta.widgets

class PropietariosSearchForm(forms.Form):
    query = forms.CharField(label='Buscar', required=False)
    search_in = forms.MultipleChoiceField(
        label='Buscar por:',
        choices=[
            ('nombre', 'Nombre'),
            ('telefono', 'Teléfono'),
            ('documento', 'Documento'),
            ('email', 'Email')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class UserRegisterForm(UserCreationForm):
    
    username = forms.CharField(label='Nombre de Usuario')
    tipo_usuario = forms.ChoiceField(choices=Usuario.tipo_usuario_opciones)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)
    telefono = forms.IntegerField(label='Teléfono', help_text='Ingresar únicamente números')
    
    
    class Meta:
        model = Usuario
        fields = ['tipo_usuario', 'username', 'email', 'telefono', 'password1', 'password2']
        