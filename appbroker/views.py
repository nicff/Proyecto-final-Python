from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.db.models import Q
from appbroker.models import *
from appbroker.forms import *

def home(request):
    return render(request, 'index.html')

def crear_propiedad(request):
    
    if request.method == "POST":
        form = PropiedadesForm(request.POST)
        if form.is_valid():
            nueva_propiedad = form.save()
            return redirect('exito', objeto='propiedad', id=nueva_propiedad.id)
    else:
        form = PropiedadesForm()

    return render(request, 'crear_propiedad.html', {'form': form})

def crear_contrato(request):
    if request.method == "POST":
        form = ContratosForm(request.POST)
        if form.is_valid():
            nuevo_contrato = form.save(commit=False)
            nuevo_contrato.save()
            form.save_m2m
            return redirect('exito', objeto='contrato', id=nuevo_contrato.id)
    else:
        form = ContratosForm()

    return render(request, 'crear_contrato.html', {'form': form})

def crear_propietario(request):
    if request.method == "POST":
        form = PropietariosForm(request.POST)
        if form.is_valid():
            nuevo_propietario = form.save(commit=False)
            nuevo_propietario.save()
            form.save_m2m()
            return redirect('exito', objeto='propietario', id=nuevo_propietario.id)
    else:
        form = PropietariosForm()

    return render(request, 'crear_propietario.html', {'form': form})

def crear_inquilino(request):
    if request.method == "POST":
        form = InquilinosForm(request.POST)
        if form.is_valid():
            nuevo_inquilino = form.save(commit=False)
            nuevo_inquilino.save()
            form.save_m2m()
            return redirect('exito', objeto='inquilino', id=nuevo_inquilino.id)
    else:
        form = InquilinosForm()

    return render(request, 'crear_inquilino.html', {'form': form})

def exito(request, objeto, id):
    contexto = {'objeto': objeto}
    if objeto == 'propiedad' or objeto == 'propiedad_editada':
        contexto['propiedad'] = Propiedades.objects.get(id=id)
    elif objeto == 'inquilino':
        contexto['inquilino'] = Inquilinos.objects.get(id=id)
    elif objeto == 'propietario':
        contexto['propietario'] = Propietarios.objects.get(id=id)
    elif objeto == 'contrato':
        contexto['contrato'] = Contratos.objects.get(id=id)
    elif objeto == 'registrousuario':
        contexto['registrousuario'] = "Usuario registrado con éxito"

    return render(request, 'exito.html', contexto)

#def crear_compra(request):

#def crear_reclamo(request):

#def crear_reparacion(request):

def buscar_propietarios(request):
    form = PropietariosSearchForm(request.GET or None)
    resultados = None
    criterio_elegido = False

    if request.method == 'GET' and 'query' in request.GET:
        print("Formulario recibido:", request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            buscar_por = form.cleaned_data['search_in']
            if buscar_por:
                criterio_elegido = True
                q_objects = Q()

                if 'nombre' in buscar_por:
                    q_objects |= Q(nombre__icontains=query)
                if 'telefono' in buscar_por:
                    q_objects |= Q(telefono__icontains=query)
                if 'documento' in buscar_por:
                    q_objects |= Q(documento__icontains=query)
                if 'email' in buscar_por:
                    q_objects |= Q(email__icontains=query)

                resultados = Propietarios.objects.filter(q_objects)

    return render(request, 'buscar_propietarios.html', {'form': form, 'resultados': resultados, 'criterio_elegido': criterio_elegido})

def ver_propiedades(request):
    propiedades = Propiedades.objects.all()
    return render(request, 'propiedades.html', {'propiedades':propiedades})

def gestion_propiedades(request):
    propiedades = Propiedades.objects.all()
    return render(request, 'gestion_propiedades.html', {'propiedades':propiedades})

def eliminar_propiedad(request, prop_id):
    propiedad = Propiedades.objects.get(id=prop_id)
    propiedad.delete()
    
    propiedades = Propiedades.objects.all()
    return render(request, 'gestion_propiedades.html', {'propiedades':propiedades})

def editar_propiedad(request, prop_id):
    propiedad = Propiedades.objects.get(id=prop_id)
    
    if request.method == 'POST':
        formulario_edicion = PropiedadesForm(request.POST, instance=propiedad)
        
        if formulario_edicion.is_valid():
            formulario_edicion.save()
            
            return redirect('exito', objeto='propiedad_editada', id=propiedad.id)
    
    else:
        formulario_edicion = PropiedadesForm(instance=propiedad)
        
    return render(request, 'editar_propiedad.html', {'form': formulario_edicion, 'propiedad': propiedad})
class PropiedadDetalles(DetailView):
    
    model = Propiedades
    template_name = 'propiedad.html'
    
def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return redirect('exito', objeto='registrousuario', id=None)
    
    else:
        form = UserRegisterForm()
        
    return render(request, 'registro.html', {'form':form})

def login_request(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')
            
            user = authenticate(username=usuario, password=contrasena)
            
            if user is not None:
                login(request, user)
                return redirect('exito', objeto='loginusuario', id=None)
            
            else:
                return redirect('login.html', {'mensaje': 'Error, datos incorrectos'})
        
        else:
            return render(request, 'login.html', {'mensaje': 'Error, formulario erróneo'})
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form, 'mensaje':''})
        
        