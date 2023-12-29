from django.shortcuts import render, redirect
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


