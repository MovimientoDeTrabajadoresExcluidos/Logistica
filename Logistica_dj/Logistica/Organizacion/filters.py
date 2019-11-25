from django.contrib import admin
from django.contrib.auth.models import User

from .models import PuntoDeConsumo, PuntoDeRecepcion

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

# si movemos nombre y localizacion a la entidad abstracta punto podemos usar un solo filtro por cada una
# Filtros de PC
class PuntoDeConsumoNombreFilter(InputFilter):
    parameter_name = 'PCNombre' # este es el identificador oculto del filtro. tienen q ser diferentes los de todos los filtros
    title = 'Nombre'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pc.id for pc in PuntoDeConsumo.objects.filter(nombre__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeConsumoLocalidadFilter(InputFilter):
    parameter_name = 'PCLocalidad'
    title = 'Localidad'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pc.id for pc in PuntoDeConsumo.objects.filter(localidad__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeConsumoProvinciaFilter(InputFilter):
    parameter_name = 'PCProvincia'
    title = 'Provincia'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pc.id for pc in PuntoDeConsumo.objects.filter(provincia__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeConsumoResponsableFilter(InputFilter):
    parameter_name = 'PCResponsable'
    title = 'Responsable'

    def queryset(self, request, queryset):
        if self.value() is not None:
            #TODO cambiar si el pc va a tener un usuario
            return queryset.filter(responsable__icontains=self.value())


# Filtros de PR
class PuntoDeRecepcionNombreFilter(InputFilter):
    parameter_name = 'PCNombre' # este es el identificador oculto del filtro. tienen q ser diferentes los de todos los filtros
    title = 'Nombre'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pr.id for pr in PuntoDeRecepcion.objects.filter(nombre__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeRecepcionLocalidadFilter(InputFilter):
    parameter_name = 'PCLocalidad'
    title = 'Localidad'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pr.id for pr in PuntoDeRecepcion.objects.filter(localidad__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeRecepcionProvinciaFilter(InputFilter):
    parameter_name = 'PCProvincia'
    title = 'Provincia'

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids_filtro = [pr.id for pr in PuntoDeRecepcion.objects.filter(provincia__icontains=self.value())]
            return queryset.filter(id__in=ids_filtro)


class PuntoDeRecepcionResponsableFilter(InputFilter):
    parameter_name = 'PRResponsable'
    title = 'Responsable'

    def queryset(self, request, queryset):
        if self.value() is not None:
            # la primera es la mas logica que funciona con nombre y apellido, la segunda es por usuario
            # ids_filtro = [u.id for u in User.objects.filter(first_name__icontains=self.value(), last_name__icontains=self.value())]
            ids_filtro = [u.id for u in User.objects.filter(username__icontains=self.value())]
            return queryset.filter(responsable_id__in=ids_filtro)
