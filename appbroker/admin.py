from django.contrib import admin
from .models import Propiedades, Inquilinos, Propietarios, Compradores, Contratos, Compras, Reclamos, Reparymant, Pagos

# Register your models here.
admin.site.register(Propiedades)
admin.site.register(Propietarios)
admin.site.register(Inquilinos)
admin.site.register(Compradores)
admin.site.register(Contratos)
admin.site.register(Compras)
admin.site.register(Reclamos)
admin.site.register(Pagos)
admin.site.register(Reparymant)