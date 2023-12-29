from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
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
            print("Propiedades guardadas:", nuevo_propietario.propiedades.all())
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
    if objeto == 'propiedad':
        contexto['propiedad_nueva'] = Propiedades.objects.get(id=id)
    elif objeto == 'inquilino':
        contexto['inquilino_nuevo'] = Inquilinos.objects.get(id=id)
    elif objeto == 'propietario':
        contexto['propietario_nuevo'] = Propietarios.objects.get(id=id)
        contexto['propiedades_del_propietario'] = contexto['propietario_nuevo'].propiedades.all()
    elif objeto == 'contrato':
        contexto['contrato_nuevo'] = Contratos.objects.get(id=id)

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