from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from .filters import *


class PuntoDeRecepcionResource(resources.ModelResource):
    class Meta:
        model = PuntoDeRecepcion

class PuntoDeRecepcionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = PuntoDeRecepcion

    resource_class = PuntoDeRecepcionResource

    def inventario(self, obj):
        return mark_safe('<a class="btn btn-primary" href="/inventario">Inventario</a>')

    inventario.short_description = 'Inventario'
    list_display = ['nombre', 'localidad', 'provincia', 'responsable' , 'inventario']
    # search_fields = ['nombre', 'localidad', 'provincia', 'responsable']
    list_filter = [PuntoDeRecepcionNombreFilter, PuntoDeRecepcionProvinciaFilter, PuntoDeRecepcionLocalidadFilter,
                   PuntoDeRecepcionResponsableFilter]


class PuntoDeConsumoResource(resources.ModelResource):
    class Meta:
        model = PuntoDeConsumo

class PuntoDeConsumoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = PuntoDeConsumo

    resource_class = PuntoDeConsumoResource
    list_display = ['nombre', 'localidad', 'provincia', 'responsable']  #
    # search_fields = [id, 'nombre', 'localidad', 'provincia', 'responsable']
    list_filter = [PuntoDeConsumoNombreFilter, PuntoDeConsumoProvinciaFilter, PuntoDeConsumoLocalidadFilter,
                   PuntoDeConsumoResponsableFilter]

admin.site.register(PuntoDeRecepcion, PuntoDeRecepcionAdmin)
admin.site.register(PuntoDeConsumo, PuntoDeConsumoAdmin)