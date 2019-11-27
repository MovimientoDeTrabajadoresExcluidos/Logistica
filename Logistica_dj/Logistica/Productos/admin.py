from django.contrib import admin
from .models import *
from Proveedores.models import Proveedor
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .filters import TipoProductoFilter, DenominacionEnVarianteProductoFilter, ProveedorEnVarianteProductoFilter, \
    TipoProductoEnVarianteProductoFilter


# Register your models here.

class ProductoGenericoResource(resources.ModelResource):
    class Meta:
        model = ProductoGenerico


class VarianteProductoResource(resources.ModelResource):
    class Meta:
        model = VarianteProducto

    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(ProductoGenerico, 'tipo')
    )
    proveedor = fields.Field(
        column_name='proveedor',
        attribute='proveedor',
        widget=ForeignKeyWidget(Proveedor, 'nombre_compania_o_entidad')
    )


class VarianteProductoInLine(admin.TabularInline):
    class Meta:
        model = VarianteProducto

    model = VarianteProducto
    resource_class = VarianteProductoResource
    list_display = ['proveedor', 'denominacion', 'cantidad_formateada', 'pack']

    def cantidad_formateada(self, obj):
        cadena = 'N/D'
        try:
            prod = ProductoGenerico.objects.get(id=obj.tipo)
            cadena = prod.unidad_de_medida
        except:
            pass
        finally:
            return str(obj.cantidad) + ' ' + cadena

class VarianteProductoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = VarianteProducto

    model = VarianteProducto
    skip_unchanged = True
    resource_class = VarianteProductoResource
    list_display = ['proveedor', 'denominacion', 'cantidad_formateada', 'pack']
    list_filter = [TipoProductoEnVarianteProductoFilter, ProveedorEnVarianteProductoFilter,
                   DenominacionEnVarianteProductoFilter]

    # todo preguntar si se quiere ver formateado asi
    def cantidad_formateada(self, obj):
        cadena = 'N/D'
        try:
            prod = ProductoGenerico.objects.get(id=obj.tipo_id)
            cadena = prod.get_unidad_de_medida_display()
        except:
            pass
        finally:
            return str(obj.cantidad) + ' - ' + cadena

    cantidad_formateada.__name__ = 'Cantidad'


class ProductoGenericoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = ProductoGenerico

    model = ProductoGenerico
    skip_unchanged = True
    inlines = [VarianteProductoInLine]
    resource_class = ProductoGenericoResource
    list_display = ['tipo', 'categoria', 'unidad_de_medida']
    list_filter = [TipoProductoFilter, 'categoria', 'unidad_de_medida', ]


admin.site.register(ProductoGenerico, ProductoGenericoAdmin)
admin.site.register(VarianteProducto, VarianteProductoAdmin)
