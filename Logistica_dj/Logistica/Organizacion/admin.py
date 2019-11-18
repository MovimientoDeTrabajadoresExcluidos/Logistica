from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe


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


    list_display = [id, 'nombre', 'localidad', 'provincia', 'responsable' , 'inventario'] #
    search_fields = [id, 'nombre', 'localidad', 'provincia', 'responsable']



class PuntoDeConsumoResource(resources.ModelResource):
    class Meta:
        model = PuntoDeConsumo

class PuntoDeConsumoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = PuntoDeConsumo

    resource_class = PuntoDeConsumoResource
    list_display = [id, 'nombre', 'localidad', 'provincia']  #
    search_fields = [id, 'nombre', 'localidad', 'provincia', 'responsable']


admin.site.register(PuntoDeRecepcion, PuntoDeRecepcionAdmin)
admin.site.register(PuntoDeConsumo, PuntoDeConsumoAdmin)