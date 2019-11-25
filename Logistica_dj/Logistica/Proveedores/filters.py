from django.contrib import admin
from .models import Proveedor

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


class ProveedorNombreFilter(InputFilter):
    parameter_name = 'ProvNombre' # este es el identificador oculto del filtro. tienen q ser diferentes los de todos los filtros
    title = 'Nombre'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [p.id for p in Proveedor.objects.filter(nombre_compania_o_entidad__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class ProveedorProvinciaFilter(InputFilter):
    parameter_name = 'ProvProvincia' # este es el identificador oculto del filtro. tienen q ser diferentes los de todos los filtros
    title = 'Provincia'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [p.id for p in Proveedor.objects.filter(provincia__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)

