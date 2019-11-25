# encoding: utf-8

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from PyPDF2 import PdfFileMerger


def render_pdf(url_template, contexto={}):
    template = get_template(url_template)
    html = template.render(contexto)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Error Rendering PDF", status=400)

def render_multiple_pdf(url_template, contexto={}):
    merger = PdfFileMerger()
    salida = BytesIO()
    template = get_template(url_template)
    for egreso in contexto['egresos']:
        html = template.render(egreso)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            merger.append(result)
        else:
            return HttpResponse("Error Rendering PDF", status=400)
    merger.write(salida)
    return HttpResponse(salida.getvalue(), content_type="application/pdf")
