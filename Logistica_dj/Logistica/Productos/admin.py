from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto

class ProductoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = Producto

    model = Producto
    resource_class = ProductoResource
    list_display = ['tipo','denominacion', 'unidad_de_medida', 'cantidad']
    search_fields = ['tipo','denominacion']

admin.site.register(Producto, ProductoAdmin)