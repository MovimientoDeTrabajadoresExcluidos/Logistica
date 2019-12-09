from django.contrib import admin, messages
from .models import *
from Movimientos.models import LineaDeIng, DistribucionProducto, LineaDistribucionProducto
from Productos.models import VarianteProducto
from Organizacion.models import PuntoDeConsumo
import pandas as pd


# las columnas deben tener el nombre de la variante del producto
# todo agregar verificacion de proveedor (q esta en el ingreso) para que las variantes sean de él
# todo ver bien como mandar los mensajes para que sean mas claros y especificos (sobretodo los de error)
def make_importacion_lineas_ingreso(modeladmin, request, queryset):
    todo_ok = True
    ingresos_procesados = []
    try:
        for obj in queryset:
            excel_file = obj.documento
            lineas = pd.read_excel(excel_file)
            # columnas = [columna.lower() for columna in lineas.columns]
            lineas.columns = [l.lower() for l in lineas.columns]
            for linea in lineas.itertuples():
                nueva_linea_ing = LineaDeIng()
                nueva_linea_ing.movimiento = obj.ingreso
                nueva_linea_ing.cantidad = getattr(linea, 'cantidad')
                nueva_linea_ing.producto = VarianteProducto.objects.get(denominacion=getattr(linea, 'producto'))
                nueva_linea_ing.save()
            obj.delete()
            ingresos_procesados.append(obj)

    except AttributeError:
        todo_ok = False
        mensaje = 'Falta alguna de las columnas: Producto o Cantidad en el archivo cargado'

    except ImportacionLineaIngreso.DoesNotExist:
        todo_ok = False
        mensaje = 'Alguna variante de producto no esta registrada en las Variantes de Productos'

    except ValueError:
        todo_ok = False
        mensaje = 'El documento ha sido eliminado de la base de datos, por favor carguelo nuevamente'

    finally:
        if todo_ok:
            messages.add_message(request, messages.SUCCESS, 'Se han importado las lineas de los ingresos ' +
                                 ','.join([str(o.ingreso) for o in ingresos_procesados]))
        else:
            if ingresos_procesados.__len__() > 0:
                messages.add_message(request, messages.SUCCESS, 'Se han importado las lineas de los ingresos ' +
                                     ','.join([str(o.ingreso) for o in ingresos_procesados]))
            messages.add_message(request, messages.ERROR, mensaje)
make_importacion_lineas_ingreso.short_description = "Importar lineas de ingresos seleccionados"


def make_importacion_distribucion(modeladmin, request, queryset):
    todo_ok = True
    distribuciones_procesadas = []
    try:
        for obj in queryset:
            excel_file = obj.documento
            lineas = pd.read_excel(excel_file)
            # columnas = [columna.lower() for columna in lineas.columns]
            lineas.columns = [l.lower().strip().replace(' ', '_') for l in lineas.columns]
            lineas.drop(lineas.columns[lineas.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
            print(lineas.columns)
            # Hago un replace porque los espacios causan errores en el getattr()
            for columna in lineas.columns:
                if not str(columna).__eq__('punto_de_consumo'):
                    nueva_distribucion_producto = DistribucionProducto()
                    nueva_distribucion_producto.distribucion = obj.distribucion
                    nueva_distribucion_producto.producto = VarianteProducto.objects.get(denominacion__icontains=str(columna).replace('_', ' '))
                    nueva_distribucion_producto.save()
                    aux_ultima_linea = None
                    for linea in lineas.itertuples():
                        nueva_linea_distribucion_producto = LineaDistribucionProducto()
                        nueva_linea_distribucion_producto.distribucion = nueva_distribucion_producto
                        nueva_linea_distribucion_producto.pc = PuntoDeConsumo.objects.get(nombre__icontains=str(getattr(linea, 'punto_de_consumo')))
                        nueva_linea_distribucion_producto.porcentaje = getattr(linea, str(columna))
                        nueva_linea_distribucion_producto.save()
                        aux_ultima_linea = nueva_linea_distribucion_producto
                    nueva_distribucion_producto.total_asignado = aux_ultima_linea.traerTotalAsignado()
                    nueva_distribucion_producto.save()
            obj.delete()
            distribuciones_procesadas.append(obj)

    except AttributeError:
        todo_ok = False
        mensaje = 'Falta columna Punto de consumo en el documento'

    except VarianteProducto.DoesNotExist:
        todo_ok = False
        mensaje = 'Alguna variante de producto no esta registrada en las Variantes de Productos o su Denominacion en ' \
                  'el documento es incorrecta'

    except ValueError:
        todo_ok = False
        mensaje = 'El documento ha sido eliminado de la base de datos, por favor carguelo nuevamente'

    finally:
        if todo_ok:
            messages.add_message(request, messages.SUCCESS, 'Se han importado las lineas de los ingresos ' +
                                 ','.join([str(o.distribucion) for o in distribuciones_procesadas]))
        else:
            if distribuciones_procesadas.__len__() > 0:
                messages.add_message(request, messages.SUCCESS, 'Se han importado las lineas de los ingresos ' +
                                     ','.join([str(o.distribucion) for o in distribuciones_procesadas]))
            messages.add_message(request, messages.ERROR, mensaje)
make_importacion_distribucion.short_description = 'Importar distribuciones seleccionadas'


# Register your models here.
class ImportacionLineasIngresoAdmin(admin.ModelAdmin):
    class Meta:
        model = ImportacionLineaIngreso

    list_display = ['ingreso']
    actions = [make_importacion_lineas_ingreso]

    def delete_queryset(self, request, queryset):  # Esta es para cuando se eliminan muchas por seleccion
        for obj in queryset:
            obj.delete()


class ImportacionDistribucionAdmin(admin.ModelAdmin):
    class Meta:
        model = ImportacionDistribucion

    list_display = ['distribucion']
    actions = [make_importacion_distribucion]

    def delete_queryset(self, request, queryset):  # Este es para cuando se eliminan muchas por seleccion
        for obj in queryset:
            obj.delete()


admin.site.register(ImportacionDistribucion, ImportacionDistribucionAdmin)
admin.site.register(ImportacionLineaIngreso, ImportacionLineasIngresoAdmin)
