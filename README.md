# Logistica

=================ACTIVAR ENTORNO VIRTUAL=====================

cd /venv
source bin/activate

============INSTALACION DE PAQUETES REQUERIDOS=================

pip install -r requirements.txt

======================CORRER SERVIDOR====================== 

python manage.py runserver 


<h3> TODO </h3> 
<ul>
<li> Ver funcionamiento import/export </li>
<li> import/export en inline </li>
<li> Restringir en Línea de ingreso los productos por Proveedor ! (Variantes) </li>
<li> ListaDeDestinos --> Punto de Recepción por default </li>
<li> Evitar duplicado por registro de variante de producto en lineas de ingreso y egreso </li>
<li> Evitar duplicado por registro de Lineas de Distribucion de Productos.PuntoDeConsumo </li> 
<li> Restricción: Solamente puede </li>
<li> Excepción no controlada: Al asignar un mismo ingreso a PR a dos distribuciones distintas </li>
</ul>
