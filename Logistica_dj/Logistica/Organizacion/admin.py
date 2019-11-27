from django.contrib import admin
from .models import *
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from .filters import *


class PuntoDeRecepcionResource(resources.ModelResource):
    class Meta:
        model = PuntoDeRecepcion
        exclude = 'punto_ptr, polymorphic_ctype'
    responsable = fields.Field(
        column_name='responsable',
        attribute='responsable',
        widget=ForeignKeyWidget(User, 'username')
    )
    # todo no me dejo poner vacia la observacion y no logre entender porque

class PuntoDeRecepcionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = PuntoDeRecepcion

    resource_class = PuntoDeRecepcionResource

    # def inventario(self, obj):
    # return mark_safe('<a class="btn btn-primary" href="/inventario">Inventario</a>')
    # inventario.short_description = 'Inventario'
    list_display = ['nombre', 'localidad', 'provincia', 'responsable', ]  # 'inventario']
    list_filter = [PuntoDeRecepcionNombreFilter, PuntoDeRecepcionProvinciaFilter, PuntoDeRecepcionLocalidadFilter,
                   PuntoDeRecepcionResponsableFilter]


class PuntoDeConsumoResource(resources.ModelResource):
    class Meta:
        model = PuntoDeConsumo
        exclude = 'punto_ptr, polymorphic_ctype'
    punto_de_recepcion = fields.Field(
        column_name='punto_de_recepcion',
        attribute='punto_de_recepcion',
        widget=ForeignKeyWidget(PuntoDeRecepcion, 'nombre')
    )

class PuntoDeConsumoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = PuntoDeConsumo

    resource_class = PuntoDeConsumoResource
    list_display = ['nombre', 'localidad', 'provincia', 'responsable']
    list_filter = [PuntoDeConsumoNombreFilter, PuntoDeConsumoProvinciaFilter, PuntoDeConsumoLocalidadFilter,
                   PuntoDeConsumoResponsableFilter]


admin.site.register(PuntoDeRecepcion, PuntoDeRecepcionAdmin)
admin.site.register(PuntoDeConsumo, PuntoDeConsumoAdmin)
