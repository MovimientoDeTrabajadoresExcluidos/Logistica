from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import EgresosPuntoDeRecepcion, IngresosAPuntosDeRecepcion, LineaDeEgr, LineaDeIng, Distribucion, \
    DistribucionProducto, LineaDistribucionProducto
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe


# Acciones adicionales
def make_egresos_de_ingresos(modeladmin, request, queryset):
    for obj in queryset:
        if obj.estado == 'Validado': # ver como preguntar en funcion de IngresoPR.ESTADOS
            try:
                distribucion = Distribucion.objects.get(ingreso=obj)
            except Distribucion.DoesNotExist:
                pass
                return #aca deberia mandar un mensaje de que no hay distribuciones para ese ingreso y salir

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
                        # traigo linea de ingreso de ese producto
                        # mensaje de error hay dos productos iguales en distintas lineas en el ingreso puede
                        # arreglarse sobrecargando el formset_save() de ingresos
                        for pcs in lineasDistribucionProducto: # recorro los pcs de la distribucion actual
                            if pcs.pc == egr.destino:
                                lineaEgreso = LineaDeEgr()
                                lineaEgreso.producto = dist.producto
                                lineaEgreso.movimiento = egr
                                lineaEgreso.cantidad = (pcs.porcentaje * lineaIngreso.cantidad) / 100
                                if lineaIngreso.cantidad > 0:
                                    lineaEgreso.save()
                    except LineaDeIng.DoesNotExist or LineaDeIng.MultipleObjectsReturned:
                        pass
        else:
            pass# aca deberia ir un mensaje de que se debe validar el ingreso para poder generar los egresos

make_egresos_de_ingresos.short_description = 'Generar egresos asociados'


def make_carga_productos_automatica(modeladmin, request, queryset):
    for obj in queryset:
        lineasIngreso = LineaDeIng.objects.filter(movimiento=obj.ingreso)
        for linea in lineasIngreso:
            nuevaLineaDistribucion = DistribucionProducto()
            nuevaLineaDistribucion.producto = linea.producto
            nuevaLineaDistribucion.distribucion = obj
            nuevaLineaDistribucion.save()

make_carga_productos_automatica.short_description = 'Cargar Productos desde ingreso asociado'


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
#    resource_class = LineaIngPRResource
    #list_display = ['producto', 'cantidad']

class LineaDePedidoEgrInLine(admin.TabularInline): #ImportExportModelAdmin
    class Meta:
        model = LineaDeEgr
    model = LineaDeEgr
#    resource_class = LineaEgrPRResource
    #list_display = ['producto', 'cantidad']

class IngPRAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    class Meta:
        model = IngresosAPuntosDeRecepcion

    model = IngresosAPuntosDeRecepcion
    inlines = [LineaDePedidoIngInLine]
    resource_class = MovimientosIngresosPRResource
    list_display = [id, 'fecha_y_hora_de_ingreso','origen', 'destino', 'estado']
    search_fields = [id, 'origen', 'destino', 'estado']
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


    list_display = [id, 'fecha_y_hora_de_registro', 'origen', 'destino', 'estado' , 'obtener_remito'] #
    search_fields = [id, 'origen', 'destino', 'estado']


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
    list_display = ['id', 'producto']
    search_fields = ['id', 'producto']
    readonly_fields = ['total_asignado']

    # con esta funcion oculto el acceso a via menu pero permito que se modifique directamente
    # def get_model_perms(self, request):
    #   return {}

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


admin.site.register(Distribucion, DistribucionAdmin)
admin.site.register(DistribucionProducto, DistribucionProductoAdmin)

admin.site.register(IngresosAPuntosDeRecepcion, IngPRAdmin)
admin.site.register(EgresosPuntoDeRecepcion, EgrPRAdmin)



