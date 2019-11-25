from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import EgresosPuntoDeRecepcion, IngresosAPuntosDeRecepcion, LineaDeEgr, LineaDeIng, Distribucion, \
    DistribucionProducto, LineaDistribucionProducto, LineaListaDestinosEgreso, ListaDestinosEgreso
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from .filters import *
from django.contrib import messages


# Acciones adicionales
def make_remitos_en_masa(modeladmin, request, queryset):
    cadena = "/remito/remitos_en_masa/%s" % queryset[0].id
    for obj in queryset:
        if not obj.id == queryset[0].id:
            cadena += "," + str(obj.id)
    return redirect(cadena)
make_remitos_en_masa.attrs = {'target': '_blank'}
make_remitos_en_masa.short_description = "Generar Remitos"


def make_egresos_de_ingresos(modeladmin, request, queryset):
    for obj in queryset:
        if obj.estado == 'Validado': # ver como preguntar en funcion de IngresoPR.ESTADOS
            try:
                distribucion = Distribucion.objects.get(ingreso=obj)
            except Distribucion.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'No hay una distribucion asociada al ingreso ' + obj)

            distribuciones = DistribucionProducto.objects.filter(distribucion=distribucion)
            egresos = []
            for dist in distribuciones: # recorrro los productos de la distribucion
                # recorro los pc y genero un egreso para cada uno
                lineasDistribucionProducto = LineaDistribucionProducto.objects.filter(distribucion=dist)
                for pcs in lineasDistribucionProducto:
                    if pcs.pc not in [e.destino for e in egresos]: #si todavia no agregue el pc lo agrego
                        egreso = EgresosPuntoDeRecepcion()
                        egreso.destino = pcs.pc
                        egreso.origen = obj.destino # ver esto
                        egreso.save()
                        egresos.append(egreso)

            for egr in egresos: # recorro los egresos generados
                for dist in distribuciones: # recorro los productos de la distribucion
                    lineasDistribucionProducto = LineaDistribucionProducto.objects.filter(distribucion=dist)

                    try:
                        lineaIngreso = LineaDeIng.objects.get(movimiento=obj, producto=dist.producto)
                        for pcs in lineasDistribucionProducto: # recorro los pcs de la distribucion actual
                            if pcs.pc == egr.destino:
                                lineaEgreso = LineaDeEgr()
                                lineaEgreso.producto = dist.producto
                                lineaEgreso.movimiento = egr
                                lineaEgreso.cantidad = (pcs.porcentaje * lineaIngreso.cantidad) / 100
                                if lineaIngreso.cantidad > 0:
                                    lineaEgreso.save()
                    except LineaDeIng.DoesNotExist or LineaDeIng.MultipleObjectsReturned:
                        messages.add_message(request, messages.WARNING,
                                             'Hubo productos en la distribucion que no se encontraron en el ingreso')
            messages.add_message(request, messages.SUCCESS,
                                 'Se han generados los egresos asociados al ingreso ' + str(obj))
        else:
            messages.add_message(request, messages.ERROR, 'Debe validarse el ingreso para poder generar sus egresos')
make_egresos_de_ingresos.short_description = 'Generar egresos asociados'


def make_carga_productos_automatica(modeladmin, request, queryset):
    for obj in queryset:
        ingreso = IngresosAPuntosDeRecepcion.objects.get(id=obj.ingreso_id)
        lineasIngreso = LineaDeIng.objects.filter(movimiento=obj.ingreso)
        distribucionesExistentes = DistribucionProducto.objects.filter(distribucion_id=obj.id)
        lineasDistribucionExistentes = LineaDistribucionProducto.objects.filter(distribucion_id__in=[o.id for o in distribucionesExistentes])
        for linea in lineasIngreso:
            if linea.producto not in [o.producto for o in distribucionesExistentes]:
                nuevaDistribucion = DistribucionProducto()
                nuevaDistribucion.producto = linea.producto
                nuevaDistribucion.distribucion = obj
                nuevaDistribucion.save()
                listaEgreso = LineaListaDestinosEgreso.objects.filter(listaDeDestinos_id=ingreso.listaDeDestinos)
                for destino in listaEgreso:
                    if destino not in [o.pc for o in lineasDistribucionExistentes]:
                        nuevaLineaDistribucion = LineaDistribucionProducto()
                        nuevaLineaDistribucion.pc = destino.puntoDeConsumo
                        nuevaLineaDistribucion.distribucion = nuevaDistribucion
                        nuevaLineaDistribucion.save()
    messages.add_message(request, messages.SUCCESS, 'Se han generado los productos y destinos de las distribuciones seleccionadas')
make_carga_productos_automatica.short_description = 'Cargar Productos y Destinos desde ingreso asociado'


# Register your models here.
class MovimientosEgresosPRResource(resources.ModelResource):
    class Meta:
        model = EgresosPuntoDeRecepcion

class MovimientosIngresosPRResource(resources.ModelResource):
    class Meta:
        model = IngresosAPuntosDeRecepcion

class LineaIngPRResource(resources.ModelResource):
    class Meta:
        model = LineaDeIng

class LineaEgrPRResource(resources.ModelResource):
    class Meta:
        model = LineaDeEgr

class LineaDePedidoIngInLine(admin.TabularInline): #ImportExportModelAdmin
    class Meta:
        model = LineaDeIng
    model = LineaDeIng
    resource_class = LineaIngPRResource
    #list_display = ['producto', 'cantidad']

class LineaDePedidoEgrInLine(admin.TabularInline): #ImportExportModelAdmin
    class Meta:
        model = LineaDeEgr
    model = LineaDeEgr
    resource_class = LineaEgrPRResource
    #list_display = ['producto', 'cantidad']

class IngPRAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = IngresosAPuntosDeRecepcion

    model = IngresosAPuntosDeRecepcion
    inlines = [LineaDePedidoIngInLine]
    resource_class = MovimientosIngresosPRResource
    list_display = ['id', 'fecha_y_hora_de_ingreso','origen', 'destino', 'estado']
    # search_fields = ['id']
    list_filter = ['fecha_y_hora_de_ingreso', OrigenIngFilter, DestinoIngFilter, 'estado']
    actions = [make_egresos_de_ingresos]


class EgrPRAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = EgresosPuntoDeRecepcion
    inlines = [LineaDePedidoEgrInLine]
    resource_class = MovimientosEgresosPRResource

    def obtener_remito(self, obj):
        return mark_safe('<a class="btn btn-primary" href="/remito/'+str(obj.id)+'">Remito</a>')
    obtener_remito.short_description = 'Generar Remito'
#    obtener_remitoallow_tags = True
    list_display = ['id', 'fecha_y_hora_de_registro', 'origen', 'destino', 'estado', 'obtener_remito']
    # search_fields = ['origen']
    list_filter = ('fecha_y_hora_de_registro', OrigenEgrFilter, DestinoEgrFilter, 'estado')
    actions = [make_remitos_en_masa]

# distribucion de productos ------
class MovimientosDistribucionResource(resources.ModelResource):
    class Meta:
        model = Distribucion


class MovimientosDistribucionProductoResource(resources.ModelResource):
    class Meta:
        model = DistribucionProducto


class LineaDeDistribucionProductoResource(resources.ModelResource):
    class Meta:
        model = LineaDistribucionProducto


class LineaDeDistribucionProductoInLine(admin.TabularInline):
    class Meta:
        model = LineaDistribucionProducto

    model = LineaDistribucionProducto
    # fields = ['id', 'producto', 'porcentaje']
    list_display = ['id', 'pc', 'porcentaje']


class EditLinkToInlineObject(object):
    # clase para obtener link de edicion a menu admin inline
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">Editar</a>'.format(u=url))
        else:
            return ''


class DistribucionProductoInLine(EditLinkToInlineObject, admin.TabularInline):
    # estas son las lineas de cada distribucion a pc
    class Meta:
        model = DistribucionProducto
    model = DistribucionProducto
    fields = ['id', 'edit_link', 'producto', 'total_asignado']
    readonly_fields = ['edit_link', 'total_asignado']


class DistribucionProductoAdmin(admin.ModelAdmin):
    # estas son las distribuciones, debe haber solo una por cada ingreso
    class Meta:
        model = DistribucionProducto
    inlines = [LineaDeDistribucionProductoInLine]
    resource_class = MovimientosDistribucionProductoResource
    fields = ['producto', 'distribucion', 'total_asignado']
    list_display = ['id', 'producto', 'distribucion', 'total_asignado']
    search_fields = ['id', 'producto']
    readonly_fields = ['total_asignado']

    #con esta funcion oculto el acceso a via menu pero permito que se modifique directamente
    #def get_model_perms(self, request):
        #return {}

    def response_post_save_change(self, request, obj):
        id_distribucion = Distribucion.objects.get(id=obj.distribucion_id).id
        return redirect(
            "/Movimientos/distribucion/%s/change/" % (id_distribucion))  # Preguntar si esto esta bien o es una mala practica
        # arreglar para q si se elimina tambien devuelva al menu distribucion o que no muestre el boton eliminar a la
        # derecha debajo de los guardar


class DistribucionAdmin(admin.ModelAdmin):
    class Meta:
        model = Distribucion

    inlines = [DistribucionProductoInLine]
    resource_class = MovimientosDistribucionResource
    list_display = ['id', 'ingreso']
    search_fields = ['id', 'ingreso']
    actions = [make_carga_productos_automatica]


class LineaDestinosEgresoInLine(admin.TabularInline):
    class Meta:
        model = LineaListaDestinosEgreso
    model = LineaListaDestinosEgreso
    fields = ['id', 'puntoDeConsumo']


class ListaDestinosEgresoAdmin(admin.ModelAdmin):
    class Meta:
        model = ListaDestinosEgreso
    inlines = [LineaDestinosEgresoInLine]
    list_display = ['id', 'denominacion', 'puntoDeRecepcion']
    search_fields = ['denominacion']


admin.site.register(ListaDestinosEgreso, ListaDestinosEgresoAdmin)
admin.site.register(Distribucion, DistribucionAdmin)
admin.site.register(DistribucionProducto, DistribucionProductoAdmin)
admin.site.register(IngresosAPuntosDeRecepcion, IngPRAdmin)
admin.site.register(EgresosPuntoDeRecepcion, EgrPRAdmin)



