from django.contrib import admin
from Organizacion.models import PuntoDeConsumo, PuntoDeRecepcion
from Proveedores.models import Proveedor

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


class DestinoEgrFilter(InputFilter):
    parameter_name = 'DestinoEgr'
    title = 'Destino'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtros = [punto.id for punto in PuntoDeConsumo.objects.filter(nombre__icontains=self.value())]
            return queryset.filter(destino_id__in=ids_filtros)


class OrigenEgrFilter(InputFilter):
    parameter_name = 'OrigenEgr'
    title = 'Origen'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtros = [punto.id for punto in PuntoDeRecepcion.objects.filter(nombre__icontains=self.value())]
            #TODO la linea anterior deberia cambiar si el origen puede ser un PR
            return queryset.filter(origen_id__in=ids_filtros)


class DestinoIngFilter(InputFilter):
    parameter_name = 'DestinoIng'
    title = 'Destino'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtros = [punto.id for punto in PuntoDeRecepcion.objects.filter(nombre__icontains=self.value())]
            return queryset.filter(destino_id__in=ids_filtros)


class OrigenIngFilter(InputFilter):
    parameter_name = 'OrigenIng'
    title = 'Origen'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtros = [punto.id for punto in Proveedor.objects.filter(nombre_compania_o_entidad__icontains=self.value())]
            # TODO la linea anterior deberia cambiar si el origen puede ser un PR
            return queryset.filter(origen_id__in=ids_filtros)
