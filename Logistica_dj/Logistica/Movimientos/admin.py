from django.contrib import admin
from .models import EgresosPuntoDeRecepcion, IngresosAPuntosDeRecepcion, LineaDeEgr, LineaDeIng
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe


# Register your models here.

class MovimientosEgresosPRResource(resources.ModelResource):
    class Meta:
        model = EgresosPuntoDeRecepcion

class MovimientosIngresosPRResource(resources.ModelResource):
    class Meta:
        model = IngresosAPuntosDeRecepcion

class LineaIngPRResource(resources.ModelResource):
    class Meta:
        model = LineaDeIng

class LineaEgrPRResource(resources.ModelResource):
    class Meta:
        model = LineaDeEgr

class LineaDePedidoIngInLine(admin.TabularInline): #ImportExportModelAdmin
    class Meta:
        model = LineaDeIng
    model = LineaDeIng
#    resource_class = LineaIngPRResource
    #list_display = ['producto', 'cantidad']

class LineaDePedidoEgrInLine(admin.TabularInline): #ImportExportModelAdmin
    class Meta:
        model = LineaDeEgr
    model = LineaDeEgr
#    resource_class = LineaEgrPRResource
    #list_display = ['producto', 'cantidad']

class IngPRAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = IngresosAPuntosDeRecepcion

    model = IngresosAPuntosDeRecepcion
    inlines = [LineaDePedidoIngInLine]
    resource_class = MovimientosIngresosPRResource
    list_display = [id, 'fecha_y_hora_de_ingreso','origen', 'destino', 'estado']
    search_fields = [id, 'origen', 'destino', 'estado']


class EgrPRAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = EgresosPuntoDeRecepcion
    inlines = [LineaDePedidoEgrInLine]
    resource_class = MovimientosEgresosPRResource

    def obtener_remito(self, obj):
        return mark_safe('<a class="btn btn-primary" href="/remito/'+str(obj.id)+'">Remito</a>')
    obtener_remito.short_description = 'Generar Remito'
#    obtener_remitoallow_tags = True


    list_display = [id, 'fecha_y_hora_de_registro', 'origen', 'destino', 'estado' , 'obtener_remito'] #
    search_fields = [id, 'origen', 'destino', 'estado']

admin.site.register(IngresosAPuntosDeRecepcion, IngPRAdmin)
admin.site.register(EgresosPuntoDeRecepcion, EgrPRAdmin)



