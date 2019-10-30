# Create your views here.

from __future__ import unicode_literals
from django.shortcuts import render
from .utileria import render_pdf
from django.views.generic import View
from django.http import HttpResponse
from .models import EgresosPuntoDeRecepcion, LineaDeEgr


class PDF(View):

    def get(self, request, id_context, *args, **kwargs):
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id=id_context)[0]
        fecha = movimiento.fecha_y_hora_de_egreso
        origen = movimiento.origen
        destino = movimiento.destino
        lineas = LineaDeEgr.objects.filter(movimiento=id_context)
        parametros = {
            'fecha': fecha,
            'origen': origen,
            'destino': destino,
            'lineas': lineas
        }
        pdf = render_pdf("template_html_a_pdf.html", {"parametros": parametros})
        return HttpResponse(pdf, content_type="application/pdf")



