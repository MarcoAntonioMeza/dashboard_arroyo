import time
import datetime
import pandas as pd
import pytz
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import seaborn as sns
import numpy as np
import locale
import plotly.express as px
import matplotlib.ticker as mtick
import warnings
import io
import base64
import plotly.graph_objs as go
from plotly.offline import plot
import random
from .sql import *

from django.db import connection

COLORS = ['#007bff', '#17a2b8', '#28a745', '#20c997', '#00bcd4', '#1e90ff', '#00fa9a', '#2e8b57', '#66cdaa', '#00ced1']
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


#def consulta_sql(sql = 'SELECT FROM_UNIXTIME(created_at) as created_at, total, id FROM view_venta'):
def consulta_sql(sql = VENTAS):
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columnas = [col[0] for col in cursor.description]
        resultados = cursor.fetchall()

    df = pd.DataFrame(resultados, columns=columnas)
    return df








def generate_grafica(df):
    
    total = f'{round(df["total"].sum()):,}'
    #data_por_anio = df.groupby('year').size()
    data_por_anio = df.groupby('year')['total'].sum()
    
    promedio = data_por_anio.mean()
    promedio = f'{round(promedio):,}'
      # Cambiado a comillas dobles
    std = f'{round(data_por_anio.std()):,}'


    # Crear la figura de la gráfica
    fig = go.Figure()

    # Colores para las barras
    bar_colors = [COLORS[i % len(COLORS)] for i in range(len(data_por_anio))]
    bar_colors = random.sample(COLORS, len(data_por_anio))

    # Añadir las barras
    fig.add_trace(go.Bar(
        x=data_por_anio.index,
        y=data_por_anio.values,
        marker_color=bar_colors,
        name='Número de Ventas',
        text=[f'{int(val):,}' for val in data_por_anio.values],
        textposition='auto'
    ))

   

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title='Número de Ventas por Año',
        xaxis_title='Año',
        yaxis_title='Número de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(data_por_anio.index),
        ticktext=list(map(str, data_por_anio.index)),
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Renderizar la gráfica y retornar el HTML
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    
     # Cálculo de estadísticas
   
    
    data = {
        'graph_html': graph_html,
        'promedio': promedio,
        'total': total,
        'desviacion': std
    }
    return data
    

# Ejemplo de uso
# df = ... # Tu DataFrame aquí
# html_output = generate_grafica(df)


def generate_grafica__(df):
    data_por_anio = df.groupby('year').size()

    # Crear la figura de la gráfica
    fig = go.Figure()

    # Colores personalizados en tonos de azul y verde
    

    # Añadir las barras con colores que corresponden al año
    fig.add_trace(go.Bar(
        x=data_por_anio.index,
        y=data_por_anio.values,
        marker_color=[COLORS[i % len(COLORS)] for i in range(len(data_por_anio))],  # Colores azul y verde
        name='Número de Ventas',
        text=[f'{int(val):,}' for val in data_por_anio.values],
        textposition='auto'
    ))

    # Añadir una línea de tendencia
    fig.add_trace(go.Scatter(
        x=data_por_anio.index,
        y=data_por_anio.values,
        mode='lines+markers',
        name='Tendencia',
        line=dict(color='#f8f9fa', width=2),  # Línea clara para coincidir con el modo oscuro
        marker=dict(size=8, color='#f8f9fa')  # Marcadores blancos
    ))

    # Añadir título y etiquetas
    fig.update_layout(
        title='Número de Ventas por Año',
        xaxis_title='Año',
        yaxis_title='Número de Ventas',
        template='plotly_dark',  # Cambiar a un tema oscuro
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),  # Texto blanco para el modo oscuro
        plot_bgcolor='#343a40',  # Fondo de la gráfica oscuro
        paper_bgcolor='#343a40',  # Fondo de la gráfica acorde al estilo de la web
        updatemenus=[dict(type='buttons', showactive=False,
                          buttons=[dict(label='Play',
                                         method='animate',
                                         args=[None, dict(frame=dict(duration=5000, redraw=True), mode='immediate')])])]
    )

    # Configurar el eje X para que muestre solo enteros
    fig.update_xaxes(
        tickvals=list(data_por_anio.index),
        ticktext=list(map(str, data_por_anio.index)),
        title_font=dict(color='#f8f9fa'),  # Color de las etiquetas en blanco
        tickfont=dict(color='#f8f9fa')  # Color de las etiquetas en blanco
    )

    # Configurar el eje Y
    fig.update_yaxes(
        title_font=dict(color='#f8f9fa'),  # Color de las etiquetas en blanco
        tickfont=dict(color='#f8f9fa')  # Color de las etiquetas en blanco
    )
    
     # Cálculo de estadísticas
    promedio = data_por_anio.id.count() / len(data_por_anio.values)
    promedio = f'{round(promedio):,}'
    total = f'{data_por_anio.id.count():,}'
    std = f'{round(data_por_anio.std()):,}'

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))  # Color de la leyenda en blanco

    # Renderizar la gráfica y retornar el HTML
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    
    data = {
        'graph_html': graph_html,
        'promedio': promedio,
        'total': total,
        'desviacion': std
    }
    return data
    
    #return graph_html


def ventas_mes_df(anio):
    print('aniosdcsdvsdfvfsd',anio)
    #exit()
    df = consulta_sql()
    
    df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    
    df_year = df[df['year'] == anio]
    
    ingresos = df_year.groupby(df_year['created_at'].dt.month)['total'].sum()
    
    #if df_year.empty:
    #    # Si el DataFrame está vacío, usar valores por defecto
    #    ingresos = pd.Series([0] * 12, index=range(1, 13))
    #else:
    #    ingresos = df_year.groupby(df_year['created_at'].dt.month)['total'].sum()
    
    """
    ================================================
    MEDIDAS DE TENDENCIA CENTRAL DE TOTAL DE INGRESOS
    ================================================
    """
    total_ingresos =f'${round(df_year["total"].sum()):,}'
    promedio_ingresos = ingresos.mean()
    promedio_ingresos = f'${round(promedio_ingresos):,}'
    std_ingresos = f'${round(ingresos.std()):,}'
    
    
    INGRESOS = {
        'total': total_ingresos,
        'promedio': promedio_ingresos,
        'std': std_ingresos,
        'plot': draw_plot([MESES_ES[mes] for mes in ingresos.index], ingresos.values, f'CANTIDAD DE INGRESOS EN VENTAS $ EN {anio}','MESES','INGRESOS $',True)
    }
    
    return {
        'ingresos': INGRESOS,
        'anios':df['year'].unique(),
        'anio_seleccionado': anio
    }
    
    
    
    
    
    
    


def generate_grafica_anio(df, year):
    # Filtrar el DataFrame para el año seleccionado
    df_year = df[df['year'] == year]
    data_por_mes = df_year.groupby(df_year['created_at'].dt.month).size()

    # Crear la figura con barras
    fig = go.Figure()

    # Añadir las barras con colores que corresponden al mes
    fig.add_trace(go.Bar(
        x=[MESES_ES[mes] for mes in data_por_mes.index],  # Convertir los índices a nombres de mes
        y=data_por_mes.values,
        marker_color=[COLORS[i % len(COLORS)] for i in range(len(data_por_mes))],  # Asignar color basado en el índice
        name='Ventas por Mes',
        text=[f'{val:,.0f}' for val in data_por_mes.values],  # Etiquetas de valor
        textposition='auto'
    ))

    # Añadir una línea de tendencia
    fig.add_trace(go.Scatter(
        x=[MESES_ES[mes] for mes in data_por_mes.index],  # Usar nombres de mes en lugar de índices numéricos
        y=data_por_mes.values,
        mode='lines+markers',
        name='Tendencia',
        line=dict(color='#f8f9fa', width=2),  # Línea clara para el modo oscuro
        marker=dict(size=8, color='#f8f9fa')  # Marcadores blancos
    ))

    # Cálculo de estadísticas
    promedio = df_year.id.count() / len(data_por_mes.values)
    promedio = f'{round(promedio):,}'
    total = f'{df_year.id.count():,}'
    std = f'{round(data_por_mes.std()):,}'

    # Añadir título y etiquetas
    fig.update_layout(
        title=f'Ventas por Mes en {year}',  # Promedio, Total, Desviación
        xaxis_title='Mes',
        yaxis_title='Número de Ventas',
        template='plotly_dark',  # Cambiar a un tema oscuro
        showlegend=True,
        margin=dict(l=40, r=40, t=60, b=40),
        title_x=0.5,  # Centrar título
        font=dict(color='#f8f9fa'),  # Texto blanco para el modo oscuro
        plot_bgcolor='#343a40',  # Fondo de la gráfica oscuro
        paper_bgcolor='#343a40'  # Fondo de la gráfica acorde al estilo de la web
    )

    # Estilo del gráfico
    fig.update_xaxes(
        tickvals=[MESES_ES[mes] for mes in data_por_mes.index],  # Usar nombres de mes en lugar de números
        title_font=dict(color='white'),
        tickfont=dict(color='#f8f9fa')  # Color de las etiquetas en blanco
    )
    fig.update_yaxes(
        gridcolor='rgba(200, 200, 200, 0.5)', 
        zeroline=False,
        title_font=dict(color='white'),
        tickfont=dict(color='#f8f9fa')  # Color de las etiquetas en blanco
    )

    # Configuración de la leyenda
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=12, color='white')  # Color de la leyenda en blanco
    ))

    # Renderizar la gráfica y retornar el HTML
    graph_html = plot(fig, include_plotlyjs=False, output_type='div')
    data = {
        'graph_html': graph_html,
        'promedio': promedio,
        'total': total,
        'desviacion': std,
        'anio': year
    }
    return data


def vetas_totales():
    df = consulta_sql()
    df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    
    ingresos = df.groupby('year')['total'].sum()
    ventas = df.groupby('year').size()
    
    """
    ================================================
    MEDIDAS DE TENDENCIA CENTRAL DE TOTAL DE VENTAS
    ================================================
    """
    total_ventas =f'{round(df["total"].count()):,}'
    promedio_ventas = ventas.mean()
    promedio_ventas = f'{round(promedio_ventas):,}'
    std_ventas = f'{round(ventas.std()):,}'
    
    """
    ================================================
    MEDIDAS DE TENDENCIA CENTRAL DE TOTAL DE INGRESOS
    ================================================
    """
    total_ingresos =f'${round(df["total"].sum()):,}'
    promedio_ingresos = ingresos.mean()
    promedio_ingresos = f'${round(promedio_ingresos):,}'
    std_ingresos = f'${round(ingresos.std()):,}'
    
    INGRESOS = {
        'total': total_ingresos,
        'promedio': promedio_ingresos,
        'std': std_ingresos,
        'plot': draw_plot(ingresos.index, ingresos.values, 'CANTIDAD DE INGRESOS EN VENTAS $','AÑO','INGRESOS $',False)
    }
    
    
    VENTAS = {
        'total': total_ventas,
        'promedio': promedio_ventas,
        'std': std_ventas,
        'plot': draw_plot(ventas.index, ventas.values, 'CANTIDAD DE VENTAS','AÑO','tOTAL DE VENTAS',False)
    }
    
    return {
        'ingresos': INGRESOS,
        'ventas': VENTAS
    }


def venta_detalle_producto_():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])  # Asegura que 'fecha' es datetime
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

    # Añadir una barra apilada para cada producto
    for producto in TOP_PRODUCTO:
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            #x=[f'{año}-{mes:02d}' for año, mes in zip(ventas_por_mes_producto.index.get_level_values('año'), ventas_por_mes_producto.index.get_level_values('mes'))],
            y= ventas_por_mes_producto[producto],
            name=f'{producto}'
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        barmode='stack',
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis=dict(
            title='Mes',
            tickvals=list(range(1, 13)),
            ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        ),
        yaxis=dict(
            title='Cantidad de Ventas',
            tickformat=','
        ),
        legend_title_text='Producto'
    )

    PLOT =  plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }

def venta_detalle_producto__():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])  # Asegura que 'fecha' es datetime
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

   
   

    # Añadir una barra apilada para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=f'{producto}',
            marker_color=COLORS[i % len(COLORS)]  # Asigna color de la lista COLORS
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        barmode='stack',
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis=dict(
            title='Mes',
            tickvals=list(range(1, 13)),
            ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        ),
        yaxis=dict(
            title='Cantidad de Ventas',
            tickformat=','
        ),
        legend_title_text='Producto'
    )

    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }
  
def venta_detalle_producto____():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])  # Asegura que 'fecha' es datetime
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

    # Definir colores para los productos
    COLORS = ['#007bff', '#17a2b8', '#28a745', '#20c997', '#00bcd4', '#1e90ff', '#00fa9a', '#2e8b57', '#66cdaa', '#00ced1']

    # Añadir una barra apilada para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=f'{producto}',
            marker_color=COLORS[i % len(COLORS)]  # Asigna color de la lista COLORS
        ))

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )
    
    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
    # Configurar el eje Y
    fig.update_yaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }


def venta_detalle_producto():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])  # Asegura que 'fecha' es datetime
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

    # Definir colores oscuros para los productos
    #COLORS = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b']  # Ejemplo de colores oscuros

    # Añadir una barra apilada para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=f'{producto}',
            marker_color=COLORS[i % len(COLORS)]  # Asigna color de la lista COLORS
        ))
    
    # Añadir una barra apilada para cada producto
    #for producto in TOP_PRODUCTO:
    #    for año in ventas_por_mes_producto.index.get_level_values('año').unique():
    #        # Filtrar solo las ventas del producto y año específico
    #        cantidad_ventas = ventas_por_mes_producto.loc[(año, slice(None)), producto]
    #        
    #        # Crear el texto para mostrar (mes y cantidad con el año)
    #        texto_segmentos = [f'{mes} {año}<br>{cant:.2f}' for mes, cant in zip(ventas_por_mes_producto.index.get_level_values('mes'), cantidad_ventas)]
    #
    #        fig.add_trace(go.Bar(
    #            x=ventas_por_mes_producto.index.get_level_values('mes'),
    #            y=cantidad_ventas,
    #            name=f'{producto} {año}',  # Incluye el año en el nombre
    #            text=texto_segmentos,  # Asignar texto personalizado
    #            textposition='inside'   # Posición del texto
    #        ))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        barmode='stack',  # Mantener las barras apiladas
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',  # Fondo del gráfico
        paper_bgcolor='#343a40',  # Fondo de papel
    )
    
    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
    # Configurar el eje Y
    fig.update_yaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }



def draw_plot(x, y, title,xlabel='Año', ylabel='Cantidad',add_trendline=True):
    title= title.upper()
    xlabel=xlabel.upper()
    ylabel=ylabel.upper()
    fig = go.Figure()
   # Colores para las barras
    if len(x) > len(COLORS):
        # Si hay más barras que colores, repetir los colores
        bar_colors = [COLORS[i % len(COLORS)] for i in range(len(x))]
    else:
        # Si hay suficientes colores, usar una muestra aleatoria
        bar_colors = random.sample(COLORS, len(x))
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        marker_color=bar_colors,
        name=title,
        text=[f'{int(val):,}' for val in y],
        textposition='auto'
    ))
    
    if add_trendline:
        # Añadir una línea de tendencia
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name='Tendencia',
            line=dict(color='#f8f9fa', width=2),
            marker=dict(size=8, color='#f8f9fa')
        ))
        
    #Configurar el diseño de la gráfica
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )
    
    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(x),
        ticktext=list(map(str, x)),
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
     # Configurar el eje Y
    fig.update_yaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )
    
    
    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))
    
    # Renderizar la gráfica y retornar el HTML
    return  plot(fig, include_plotlyjs=True, output_type='div')