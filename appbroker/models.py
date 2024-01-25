from django.db import models
class Propiedades(models.Model):

    class haves(models.TextChoices):
        YES = 'si', 'Sí'
        NO = 'no', 'No'
    class disponible(models.TextChoices):
        EN_ALQUILER = 'en_alquiler', 'En alquiler'
        EN_VENTA = 'en_venta', 'En venta'
        VENDIDO = 'vendido', 'Vendido'
        ALQUILADO = 'alquilado', 'Alquilado'
        NO_DISPONIBLE = 'no_disponible', 'No disponible'
    class tipos(models.TextChoices):
        CASA = 'casa', 'Casa'
        DEPARTAMENTO = 'departamento', 'Departamento'
        LOCAL = 'local', 'Local comercial'
        OFICINA = 'oficina', 'Oficina'
        GALPON = 'galpon', 'Galpón'
        COCHERA = 'cochera', 'Cochera'
        TERRENO = 'terreno', 'Terreno'

    ubicacion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=disponible.choices, default=disponible.NO_DISPONIBLE)
    tipo = models.CharField(max_length=20, choices=tipos.choices)
    habitaciones = models.IntegerField(choices=[(i, str(i)) for i in range(11)], default=0)
    baños = models.IntegerField(choices=[(i, str(i)) for i in range(7)], default=1)
    balcon = models.CharField(max_length=2, choices=haves.choices, default=haves.NO)
    pileta = models.CharField(max_length=2, choices=haves.choices, default=haves.NO)
    garage = models.CharField(max_length=2, choices=haves.choices, default=haves.NO)
    valor_alquiler = models.CharField(max_length=20, blank=True, null=True)
    valor_venta = models.CharField(max_length=20, blank=True, null=True)
    expensas = models.CharField(max_length=20, blank=True, null=True)
    propietario = models.ForeignKey('Propietarios', blank=False, on_delete=models.CASCADE, related_name='propiedades_asignadas_al_propietario', related_query_name='propiedades_asignadas_a_propietario')


    def __str__(self):
        return f'{self.tipo.capitalize()} en {self.ubicacion}'
    class Meta:
        verbose_name_plural = 'Propiedades'
    
class Persona(models.Model):
    nombre = models.CharField(max_length=40)
    documento = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        abstract = True

class Inquilinos(Persona):
    propiedades = models.ManyToManyField(Propiedades)
    class Meta:
        verbose_name_plural = 'Inquilinos'
    pass

class Propietarios(Persona):
    propiedades_asignadas = models.ManyToManyField(Propiedades, related_name='propietario_asignado_a_propiedad', related_query_name='propietario_asignado_a_la_propiedad')
    def __str__(self):
        return f'{self.nombre} - Documento: {self.documento}'
    class Meta:
        verbose_name_plural = 'Propietarios'
    pass

class Compradores(Persona):
    propiedades = models.ManyToManyField(Propiedades)
    class Meta:
        verbose_name_plural = 'Compradores'
    pass

class Contratos(models.Model):
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    inquilino = models.ForeignKey(Inquilinos, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietarios, on_delete=models.CASCADE)
    inicio = models.DateField()
    final = models.DateField()
    valor_alquiler = models.CharField(max_length=20)
    def __str__(self):
        return f'Contrato de propiedad ID {self.propiedad}'
    class Meta:
        verbose_name_plural = 'Contratos'

class Compras(models.Model):
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Compradores, on_delete=models.CASCADE)
    valor_venta = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    def __str__(self):
        return f'Compra de propiedad ID {self.propiedad}'
    class Meta:
        verbose_name_plural = 'Compras'

class resuelto(models.TextChoices): # Defino el estado 'Resuelto' acá para usarlo en los modelo 'Reclamos' y 'Reparymant'
    RESUELTO = 'resuelto', 'Resuelto'
    NO_RESUELTO = 'no_resuelto', 'No resuelto'
    EN_PROCESO = 'en_proceso', 'En proceso'

class Pagos(models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return f'Pago de {self.monto} por {self.contrato.inquilino.nombre} el {self.fecha}'
    class Meta:
        verbose_name_plural = 'Pagos'
class Reclamos(models.Model):

    class tipo_reclamante(models.TextChoices):
        INQUILINO = 'inquilino', 'Inquilino'
        PROPIETARIO = 'propietario', 'Propietario'
        COMPRADOR = 'comprador', 'Comprador'

    descripcion = models.CharField(max_length=255)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=resuelto.choices)
    reclamante = models.CharField(max_length=20, choices=tipo_reclamante.choices, blank=True, null=True)
    def __str__(self):
        return f'Reclamo de {self.reclamante.lower()}, {self.estado.lower()}, con fecha {self.fecha}'
    class Meta:
        verbose_name_plural = 'Reclamos'

class Reparymant(models.Model):

    class reparaciones(models.TextChoices):
        PLOMERIA = 'plomeria', 'Plomería'
        ELECTRICIDAD = 'electricidad', 'Electricidad'
        GAS = 'gas', 'Gas'
        ESTRUCTURA = 'estructura', 'Estructura'
        VARIOS =  'varios', 'Varios'

    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=reparaciones.choices, blank=True, null=True)
    descripcion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=resuelto.choices)
    costo = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    def __str__(self):
        return f'Reparación de propiedad ID {self.propiedad}'
    class Meta:
        verbose_name_plural = 'Reparaciones y mantenimiento'