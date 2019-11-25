from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .filters import *
# Register your models here.


class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor

class ProveedorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = Proveedor

    model = Proveedor
    resource_class = ProveedorResource
    list_display = ['nombre_compania_o_entidad','tipo_de_proveedor', 'provincia']
    # search_fields = ['nombre_compania_o_entidad','tipo_de_proveedor', 'provincia']
    list_filter = [ProveedorNombreFilter, ProveedorProvinciaFilter, 'tipo_de_proveedor']

admin.site.register(Proveedor, ProveedorAdmin)

