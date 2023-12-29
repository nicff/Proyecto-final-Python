from django.urls import path
from appbroker.views import *

urlpatterns = [
    path('propiedad/', crear_propiedad, name='crear_propiedad'),
    path('exito/<str:objeto>/<int:id>/', exito, name='exito'),
    #path('compra/', crear_compra),
    path('contrato/', crear_contrato, name='crear_contrato'),
    path('inquilino', crear_inquilino, name='crear_inquilino'),
    path('propietario', crear_propietario, name='crear_propietario'),
    #path('reclamo/', crear_reclamo),
    #path('reparacion/', crear_reparacion),
]