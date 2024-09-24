from django.http import HttpResponse
from django.shortcuts import render

from process_data.process import *


def indexk(request):
    # Obtener la gráfica en formato base64
    image_base64 = ventas_anio_totales()
    
    # Incrustar la imagen en la plantilla HTML
    html = f'<img src="data:image/png;base64,{image_base64}" alt="Gráfica de Ventas">'
    
    return HttpResponse(html)



def index(request):
    
    graph_html = ventas_anio_totales()
    return render(request, 'ventas/index.html', {'graph_html': graph_html})