from django.contrib import admin, messages
from Organizacion.models import PuntoDeConsumo, PuntoDeRecepcion
from Proveedores.models import Proveedor
from .models import *

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

# ----------------------------------------------- FILTROS DE EGRESOS --------------------------------------------------#
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


class IngresoEgrFilter(InputFilter):
    parameter_name = 'IngresoEgr'
    title = '# de Ingreso'

    def queryset(self, request, queryset):
        if self.value() is not None:
            try:
                ids_filtros = [e.id for e in EgresosPuntoDeRecepcion.objects.filter(ingreso_asociado=int(self.value()))]
                return queryset.filter(id__in=ids_filtros)
            except:
                messages.add_message(request, messages.ERROR, 'El # de ingreso debe ser un numero entero')


# --------------------------------------------- FILTROS DE INGRESOS ---------------------------------------------------#
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


# ------------------------------------------------ FILTROS DE DISTRIBUCION --------------------------------------------#
class IngresoDistribucionFilter(InputFilter):
    parameter_name = 'DenoDist'
    title = 'Denominacion'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtros = [d.id for d in Distribucion.objects.filter(denominacion__icontains=self.value())]
            return queryset.filter(id__in=ids_filtros)


class PuntoDeRecepcionDistribucionFilter(InputFilter):
    parameter_name = 'PRDFilter'
    title = 'Punto de Recepcion'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_pr = [pr.id for pr in PuntoDeRecepcion.objects.filter(nombre__icontains=self.value())]
            ids_filtros = [d.id for d in Distribucion.objects.filter(punto_de_recepcion_asociado_id__in=ids_pr)]
            return queryset.filter(id__in=ids_filtros)

