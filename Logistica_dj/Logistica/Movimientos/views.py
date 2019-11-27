# Create your views here.

from __future__ import unicode_literals
from django.shortcuts import render
from .utileria import render_pdf, render_multiple_pdf
from django.views.generic import View
from django.http import HttpResponse
from .models import EgresosPuntoDeRecepcion, LineaDeEgr
from Organizacion.models import PuntoDeConsumo


class PDF(View):
    def get(self, request, id_context, *args, **kwargs):
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id=id_context)[0]
        fecha = movimiento.fecha_y_hora_de_egreso
        origen = movimiento.origen
        destino = movimiento.destino
        pc = PuntoDeConsumo.objects.get(id=destino.id)
        lineas = LineaDeEgr.objects.filter(movimiento=id_context)
        parametros = {
            'fecha': fecha,
            'origen': origen,
            'destino': destino,
            'responsable': pc.responsable,
            'lineas': lineas
        }
        pdf = render_pdf("template_html_a_pdf.html", {"parametros": parametros})
        return HttpResponse(pdf, content_type="application/pdf")


class PDF_Multiple(View):
    def get(self, request, id_context, *args, **kwargs):
        ids = id_context.split(",")
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id__in=[int(i) for i in ids])
        egresos = []
        for m in movimiento:
            fecha = m.fecha_y_hora_de_egreso
            origen = m.origen
            destino = m.destino
            pc = PuntoDeConsumo.objects.get(id=destino.id)
            lineas = LineaDeEgr.objects.filter(movimiento=m.id)
            egresos.append({'parametros': {
                'fecha': fecha,
                'origen': origen,
                'destino': destino,
                'responsable': pc.responsable,
                'lineas': lineas
            }
            })
        pdf = render_multiple_pdf("template_html_a_pdf.html", {"egresos": egresos})
        return HttpResponse(pdf, content_type="application/pdf")


