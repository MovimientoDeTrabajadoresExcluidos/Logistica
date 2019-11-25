from django.shortcuts import render
from Movimientos.models import *
from Productos.models import *
from django.shortcuts import render

# Create your views here.

#Modificar para incluir otros PR

class Stock(request):

    ingresos = LineaDeIng.objects.all()
    egresos = LineaDeEgr.objects.all()
    productos = Producto.objects.all()


    def calculoProductosIngresos(producto):
        cantidad = 0
        for linea in ingresos:
            if linea.producto == producto:
                cantidad = cantidad + linea.cantidad
        return cantidad



    def calculoProductosEgresos(producto):
        cantidad = 0
        for linea in egresos:
            if linea.producto == producto:
                cantidad = cantidad + linea.cantidad
        return cantidad


    def stockProducto(producto):
        stock_producto = calculoProductosIngresos(producto) - calculoProductosEgresos(producto)
        return stock_producto

    def render_stock(request):
        return render(request, 'stock_template.html', {'productos': productos})
