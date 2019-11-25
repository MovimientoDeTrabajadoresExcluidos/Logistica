from django.contrib import admin
from .models import *
from import_export import resources
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


class VarianteProductoInLine(admin.TabularInline):
    class Meta:
        model = VarianteProducto
    model = VarianteProducto
    resource_class = VarianteProductoResource
    list_display = ['proveedor', 'denominacion', 'cantidad', 'pack']

class VarianteProductoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = VarianteProducto
    model = VarianteProducto
    skip_unchanged = True
    resource_class = VarianteProductoResource
    list_display = ['proveedor', 'denominacion', 'cantidad', 'pack']
    list_filter = [TipoProductoEnVarianteProductoFilter, ProveedorEnVarianteProductoFilter, DenominacionEnVarianteProductoFilter]


class ProductoGenericoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = ProductoGenerico
    model = ProductoGenerico
    skip_unchanged = True
    inlines = [VarianteProductoInLine]
    resource_class = ProductoGenericoResource
    list_display = ['tipo','categoria', 'unidad_de_medida']
    list_filter = [TipoProductoFilter, 'categoria', 'unidad_de_medida',]


admin.site.register(ProductoGenerico, ProductoGenericoAdmin)
admin.site.register(VarianteProducto, VarianteProductoAdmin)