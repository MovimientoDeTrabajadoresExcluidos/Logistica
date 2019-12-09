from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import EgresosPuntoDeRecepcion, IngresosAPuntosDeRecepcion, LineaDeEgr, LineaDeIng, Distribucion, \
    DistribucionProducto, LineaDistribucionProducto
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from .filters import *
from django.contrib import messages


# Acciones adicionales
# TODO autocompletado de pc segun pr asociado a distribucion
def duplicar_distribucion(modeladmin, request, queryset):
    for obj in queryset:
        nueva_dist = Distribucion()
        nueva_dist.denominacion = obj.denominacion + ' - Copia'
        nueva_dist.punto_de_recepcion_asociado = obj.punto_de_recepcion_asociado
        nueva_dist.save()
        for linea_dist in DistribucionProducto.objects.filter(distribucion_id=obj.id):
            nueva_linea_dist = DistribucionProducto()
            nueva_linea_dist.distribucion = nueva_dist
            nueva_linea_dist.producto = linea_dist.producto
            nueva_linea_dist.total_asignado = linea_dist.total_asignado
            nueva_linea_dist.save()
            for linea_dist_producto in LineaDistribucionProducto.objects.filter(distribucion_id=linea_dist.id):
                nueva_linea_producto = LineaDistribucionProducto()
                nueva_linea_producto.distribucion = nueva_linea_dist
                nueva_linea_producto.pc = linea_dist_producto.pc
                nueva_linea_producto.porcentaje = linea_dist_producto.porcentaje
                nueva_linea_producto.save()
    messages.add_message(request, messages.SUCCESS, 'Se ha dupĺicado la distribucion')
duplicar_distribucion.short_description = 'Duplicar Distribucion'

def make_remitos_en_masa(modeladmin, request, queryset):
    cadena = "/remito/remitos_en_masa/%s" % queryset[0].id
    for obj in queryset:
        if not obj.id == queryset[0].id:
            cadena += "," + str(obj.id)
    return redirect(cadena)


make_remitos_en_masa.short_description = "Generar Remitos"


def make_egresos_de_ingresos(modeladmin, request, queryset):
    for obj in queryset:
        if obj.estado == 'Validado':  # ver como preguntar en funcion de IngresoPR.ESTADOS
            try:
                distribucion = Distribucion.objects.get(id=obj.distribucion_id)
            except Distribucion.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'No hay una distribucion asociada al ingreso ' + obj)

            distribuciones = DistribucionProducto.objects.filter(distribucion=distribucion)
            egresos = []
            for dist in distribuciones:  # recorrro los productos de la distribucion
                # recorro los pc y genero un egreso para cada uno
                lineasDistribucionProducto = LineaDistribucionProducto.objects.filter(distribucion=dist)
                for pcs in lineasDistribucionProducto:
                    if pcs.pc not in [e.destino for e in egresos]:  # si todavia no agregue el pc lo agrego
                        egreso = EgresosPuntoDeRecepcion()
                        egreso.destino = pcs.pc
                        egreso.origen = obj.destino
                        egreso.ingreso_asociado = obj
                        egreso.save()
                        egresos.append(egreso)

            for egr in egresos:  # recorro los egresos generados
                for dist in distribuciones:  # recorro los productos de la distribucion
                    lineasDistribucionProducto = LineaDistribucionProducto.objects.filter(distribucion=dist)

                    try:
                        lineaIngreso = LineaDeIng.objects.get(movimiento=obj, producto=dist.producto)
                        for pcs in lineasDistribucionProducto:  # recorro los pcs de la distribucion actual
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


class LineaDePedidoIngInLine(admin.TabularInline):  # ImportExportModelAdmin
    class Meta:
        model = LineaDeIng

    model = LineaDeIng
    resource_class = LineaIngPRResource


class LineaDePedidoEgrInLine(admin.TabularInline):  # ImportExportModelAdmin
    class Meta:
        model = LineaDeEgr

    model = LineaDeEgr
    resource_class = LineaEgrPRResource


class IngPRAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = IngresosAPuntosDeRecepcion

    model = IngresosAPuntosDeRecepcion
    inlines = [LineaDePedidoIngInLine]
    resource_class = MovimientosIngresosPRResource
    list_display = ['miNombre', 'origen', 'destino', 'fecha_y_hora_de_ingreso', 'estado']
    list_filter = ['fecha_y_hora_de_ingreso', OrigenIngFilter, DestinoIngFilter, 'estado']
    actions = [make_egresos_de_ingresos]

    def miNombre(self, obj):
        return str(obj)
    miNombre.short_description = 'Ingreso'


class EgrPRAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    class Meta:
        model = EgresosPuntoDeRecepcion

    inlines = [LineaDePedidoEgrInLine]
    resource_class = MovimientosEgresosPRResource
    list_display = ['origen', 'destino', 'ingreso_asociado', 'fecha_y_hora_de_registro', 'estado', 'obtener_remito']
    list_filter = ('fecha_y_hora_de_registro', OrigenEgrFilter, DestinoEgrFilter, IngresoEgrFilter, 'estado')
    actions = [make_remitos_en_masa]

    def obtener_remito(self, obj):
        return mark_safe('<a class="btn btn-primary" href="/remito/' + str(obj.id) + '">Remito</a>')
    obtener_remito.short_description = 'Generar Remito'


# distribucion de productos ------
class LineaDeDistribucionProductoInLine(admin.TabularInline):
    class Meta:
        model = LineaDistribucionProducto

    model = LineaDistribucionProducto
    list_display = ['id', 'pc', 'porcentajeFormateado']

    def porcentajeFormateado(self, obj):
        return str(obj.porcentaje) + '%'


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
    fields = ['id', 'edit_link', 'producto', 'totalAsignadoFormateado']
    readonly_fields = ['edit_link', 'totalAsignadoFormateado']

    def totalAsignadoFormateado(self, obj):
        return str(obj.total_asignado) + '%'

    totalAsignadoFormateado.short_description = 'Total Asignado'


class DistribucionProductoAdmin(admin.ModelAdmin):
    class Meta:
        model = DistribucionProducto

    inlines = [LineaDeDistribucionProductoInLine]
    fields = ['producto', 'distribucion', 'totalAsignadoFormateado']
    list_display = ['id', 'producto', 'distribucion', 'totalAsignadoFormateado']
    search_fields = ['id', 'producto']
    readonly_fields = ['totalAsignadoFormateado']

    def totalAsignadoFormateado(self, obj):
        return str(obj.total_asignado) + '%'
    totalAsignadoFormateado.short_description = 'Total Asignado'

    def response_post_save_change(self, request, obj):
        id_distribucion = Distribucion.objects.get(id=obj.distribucion_id).id
        return redirect(
            "/Movimientos/distribucion/%s/change/" % (
                id_distribucion))


class DistribucionAdmin(admin.ModelAdmin):
    class Meta:
        model = Distribucion

    inlines = [DistribucionProductoInLine]
    list_display = ['denominacion', 'punto_de_recepcion_asociado', 'fecha_de_creacion']
    list_filter = ['fecha_de_creacion', IngresoDistribucionFilter, PuntoDeRecepcionDistribucionFilter, ]
    actions = [duplicar_distribucion] # todo agregar cargado automatico de pc segun pr


admin.site.register(Distribucion, DistribucionAdmin)
admin.site.register(DistribucionProducto, DistribucionProductoAdmin)
admin.site.register(IngresosAPuntosDeRecepcion, IngPRAdmin)
admin.site.register(EgresosPuntoDeRecepcion, EgrPRAdmin)
