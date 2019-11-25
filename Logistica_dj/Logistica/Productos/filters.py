from django.contrib import admin
from Organizacion.models import PuntoDeConsumo, PuntoDeRecepcion
from Proveedores.models import Proveedor
from .models import ProductoGenerico, VarianteProducto

# Filtros
class InputFilter(admin.SimpleListFilter):
    template = 'input_filter.html'
    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class TipoProductoFilter(InputFilter):
    parameter_name = 'TipoProd'
    title = 'Tipo de Producto'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [producto.id for producto in ProductoGenerico.objects.filter(tipo__icontains=self.value())]
            return queryset.filter(id__in = ids_filtro)


class TipoProductoEnVarianteProductoFilter(InputFilter):
    parameter_name = 'TipoProd'
    title = 'Tipo de Producto'

    def queryset(self, request, queryset):
        if self.value() is not None:
            # traigo los ids de los productos que cumplen con el texto ingresado
            ids_filtro = [producto.id for producto in ProductoGenerico.objects.filter(tipo__icontains=self.value())]
            return queryset.filter(tipo_id__in=ids_filtro) # devuelvo el queryset filtrado

class ProveedorEnVarianteProductoFilter(InputFilter):
    parameter_name = 'ProveedorVariante'
    title = 'Proveedor'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [p.id for p in Proveedor.objects.filter(nombre_compania_o_entidad__icontains=self.value())]
            return queryset.filter(proveedor_id__in= ids_filtro)

class DenominacionEnVarianteProductoFilter(InputFilter):
    parameter_name = 'DenominacionVariante'
    title = 'Denominacion del Proveedor'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [p.id for p in VarianteProducto.objects.filter(denominacion__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)