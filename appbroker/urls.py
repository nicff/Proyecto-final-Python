from django.urls import path
from appbroker.views import *

urlpatterns = [
    path('nuevo/propiedad', crear_propiedad, name='crear_propiedad'),
    path('exito/<objeto>/<id>', exito, name='exito'),
    #path('compra/', crear_compra),
    path('nuevo/contrato/', crear_contrato, name='crear_contrato'),
    path('nuevo/inquilino', crear_inquilino, name='crear_inquilino'),
    path('nuevo/propietario', crear_propietario, name='crear_propietario'),
    #path('reclamo/', crear_reclamo),
    #path('reparacion/', crear_reparacion),
    path('buscar_propietarios', buscar_propietarios, name='buscar_propietarios'),
    path('propiedades', ver_propiedades, name='ver_propiedades'),
    path('propiedad/<pk>', PropiedadDetalles.as_view(), name='detalles'),
    path('gestion_propiedades', gestion_propiedades, name='gestion_propiedades'),
    path('eliminar/propiedad/<prop_id>', eliminar_propiedad, name='eliminar_propiedad'),
    path('editar/propiedad/<prop_id>', editar_propiedad, name='editar_propiedad'),
    path('registro', register, name='registro'),
    path('login', login_request, name='login'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout')
]