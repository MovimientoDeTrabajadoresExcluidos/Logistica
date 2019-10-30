from django import forms
from django_superform import SuperModelForm, InlineFormSetField
from Movimientos.models import LineaDePedido, EgresosPuntoDeRecepcion, IngresosAPuntosDeRecepcion


class LineaPedidoForm(forms.ModelForm):
    class Meta:
        model = LineaDePedido
        fields = ('producto', 'cantidad',)

LineaPedidoFormSet = modelformset_factory(LineaPedidoForm)


class IngresosAPuntosDeRecepcionForm(SuperModelForm):

    lineas_de_pedido = InlineFormSetField(formset_class=LineaPedidoFormSet)

    class Meta:
        model = IngresosAPuntosDeRecepcion
        fields = ('origen, destino, estado, fecha_y_hora_de_registro',)


class EgresosPuntoDeRecepcionForm(SuperModelForm):

    lineas_de_pedido = InlineFormSetField(formset_class=LineaPedidoFormSet)

    class Meta:
        model = EgresosPuntoDeRecepcion
        fields = ('origen, destino, estado, fecha_y_hora_de_registro',)