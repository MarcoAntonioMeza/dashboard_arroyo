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
        'plot': draw_plot(ingresos.index, ingresos.values, 'CANTIDAD DE INGRESOS EN VENTAS $','AÑO','INGRESOS $',True)
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

"""
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


def venta_detalle_producto_m():
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


def venta_detalle_productoP():
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

    # Crear la figura para el gráfico de líneas
    fig = go.Figure()

    # Añadir una línea para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Scatter(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            mode='lines+markers',
            name=f'{producto}',
            line=dict(color=COLORS[i % len(COLORS)], width=2),
            marker=dict(size=8)
        ))

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Tendencia Mensual de los Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
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


def venta_detalle_productodd():
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

    # Crear la figura para el gráfico de área apilada
    fig = go.Figure()

    # Añadir una traza para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Scatter(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            mode='lines',
            name=f'{producto}',
            stackgroup='one',  # Indica que es un gráfico apilado
            line=dict(width=0.5),
            fillcolor=COLORS[i % len(COLORS)],  # Asigna color de la lista COLORS
        ))

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Tendencia Acumulada de Ventas de los Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad Acumulada de Ventas',
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

def venta_detalle_productDo():
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

    # Crear la figura para el heatmap
    fig = go.Figure(data=go.Heatmap(
        z=ventas_por_mes_producto.T.values,  # Transponer los valores para que los productos sean las filas
        x=ventas_por_mes_producto.index.get_level_values('mes'),
        y=TOP_PRODUCTO,
        colorscale='Viridis',  # Escala de color
        colorbar=dict(title='Cantidad de Ventas')
    ))

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Mapa de Calor de Ventas Mensuales para los Top {TOP} Productos',
        xaxis_title='Mes',
        yaxis_title='Producto',
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

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }


def venta_detalle_productoC():
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

    # Agrupar por mes, año y producto para calcular las ventas totales
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().reset_index()

    # Filtrar para los años más recientes si es necesario (por ejemplo, los últimos 3 años)
    años_recientes = ventas_por_mes_producto['año'].unique()[-3:]
    ventas_por_mes_producto = ventas_por_mes_producto[ventas_por_mes_producto['año'].isin(años_recientes)]

    # Crear el mapa de calor
    fig = px.imshow(
        ventas_por_mes_producto.pivot_table(index='producto', columns='mes', values='cantidad', fill_value=0),
        labels=dict(x="Mes", y="Producto", color="Cantidad de Ventas"),
        x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y=TOP_PRODUCTO,
        color_continuous_scale='Viridis'
    )

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title="Mapa de Calor de Ventas Mensuales para los Top 5 Productos",
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        coloraxis_colorbar=dict(
            title="Cantidad de Ventas"
        )
    )

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }

def venta_detalle_productoCs():
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

    # Agrupar por mes, año y producto para calcular las ventas totales
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().reset_index()

    # Filtrar para los años más recientes si es necesario (por ejemplo, los últimos 3 años)
    años_recientes = ventas_por_mes_producto['año'].unique()[-3:]
    ventas_por_mes_producto = ventas_por_mes_producto[ventas_por_mes_producto['año'].isin(años_recientes)]

    # Crear el mapa de calor
    pivot_table = ventas_por_mes_producto.pivot_table(index='producto', columns='mes', values='cantidad', fill_value=0)
    
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Mes", y="Producto", color="Cantidad de Ventas"),
        x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        y=TOP_PRODUCTO,
        color_continuous_scale='Viridis'
    )
    
    # Añadir anotaciones
    fig.update_traces(
        text=pivot_table.values,
        texttemplate="%{text:.2f}",
        textfont={"size": 12},
        hoverinfo='text',
    )

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title="Mapa de Calor de Ventas Mensuales para los Top 5 Productos",
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        coloraxis_colorbar=dict(
            title="Cantidad de Ventas"
        )
    )

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    return {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO
    }
     
"""

def venta_detalle_producto_2():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else None]).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'media', 'mediana', 'moda']

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
    
    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'tendencia_central': tendencia_central.to_dict('records')  # Convertir a lista de diccionarios para fácil acceso en el template
    }
    
    return data

def venta_detalle_producto_2():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Convertir la cantidad a toneladas si la unidad de medida es 'Kilos'
    df_vD['cantidad'] = df_vD.apply(
        lambda row: row['cantidad'] / 1000 if row['unidad_medida'] == 'Kilos' else row['cantidad'],
        axis=1
    )
    df_vD['unidad_medida'] = df_vD['unidad_medida'].replace({'Kilos': 'Toneladas'})

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto', 'unidad_medida'])['cantidad'].agg(
        media=lambda x: round(x.mean(), 2),
        mediana=lambda x: round(x.median(), 2),
        moda=lambda x: round(x.mode().iloc[0], 2) if not x.mode().empty else None
    ).reset_index()

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
        yaxis_title='Cantidad (en Toneladas o Piezas)',
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
    
    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'tendencia_central': tendencia_central.to_dict('records')  # Convertir a lista de diccionarios para fácil acceso en el template
    }
    
    return data

def venta_detalle_producto_3():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central y la suma total por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(['sum', 'mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else None]).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'media', 'mediana', 'moda']

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

    # Definir colores para los productos
    #COLORS = ['#007bff', '#17a2b8', '#28a745', '#20c997', '#00bcd4']

    # Añadir una barra apilada para cada producto
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=f'{producto}',
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico con el fondo oscuro
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )
    
    # Configuración adicional del eje X y Y
    fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')
    
    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'tendencia_central': tendencia_central.to_dict('records')  # Convertir a lista de diccionarios para fácil acceso en el template
    }
    
    return data

def venta_detalle_producto_4():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else None]).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'media', 'mediana', 'moda']

    # Redondear los resultados a 2 decimales
    tendencia_central[['media', 'mediana']] = tendencia_central[['media', 'mediana']].round(2)

    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

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

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'tendencia_central': tendencia_central.to_dict('records')  # Convertir a lista de diccionarios para fácil acceso en el template
    }

    return data

def venta_detalle_producto_5():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        ['sum', 'mean', 'std']).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'promedio', 'desviacion_estandar']

    # Redondear los resultados a 2 decimales
    tendencia_central[['promedio', 'desviacion_estandar']] = tendencia_central[['promedio', 'desviacion_estandar']].round(2)
    tendencia_central['total_vendido'] = tendencia_central['total_vendido'].round(2)

    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

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

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Preparar los datos para la tabla de estadísticas generales
    stats_generales = tendencia_central.groupby(['año', 'mes']).agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()
    stats_generales['total_vendido'] = stats_generales['total_vendido'].round(2)
    stats_generales['promedio'] = stats_generales['promedio'].round(2)
    stats_generales['desviacion_estandar'] = stats_generales['desviacion_estandar'].round(2)

    # Convertir el mes a nombre en la tabla de estadísticas generales
    #stats_generales['mes'] = stats_generales['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])
# Convertir el mes a nombre en la tabla de estadísticas generales
    stats_generales['mes'] = stats_generales['mes'].apply(lambda x: int(x) if isinstance(x, str) and x.isdigit() else x)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'stats_generales': stats_generales.to_dict('records')
    }

    return data

def venta_detalle_producto_6():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        ['sum', 'mean', 'std']).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'promedio', 'desviacion_estandar']

    # Redondear los resultados a 2 decimales
    tendencia_central[['promedio', 'desviacion_estandar']] = tendencia_central[['promedio', 'desviacion_estandar']].round(2)
    tendencia_central['total_vendido'] = tendencia_central['total_vendido'].round(2)

    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

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

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Preparar los datos para la tabla de estadísticas generales
    stats_generales = tendencia_central.groupby('año').agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()
    
    # Redondear los resultados a 2 decimales
    stats_generales['total_vendido'] = stats_generales['total_vendido'].round(2)
    stats_generales['promedio'] = stats_generales['promedio'].round(2)
    stats_generales['desviacion_estandar'] = stats_generales['desviacion_estandar'].round(2)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'stats_generales': stats_generales.to_dict('records')
    }

    return data

def venta_detalle_producto_7():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        ['sum', 'mean', 'std']).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'promedio', 'desviacion_estandar']

    # Redondear los resultados a 2 decimales
    tendencia_central[['promedio', 'desviacion_estandar']] = tendencia_central[['promedio', 'desviacion_estandar']].round(2)
    tendencia_central['total_vendido'] = tendencia_central['total_vendido'].round(2)

    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

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

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Preparar los datos para la tabla de estadísticas generales por producto
    productos_estadisticas = tendencia_central.groupby('producto').agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()

    # Redondear los resultados a 2 decimales
    productos_estadisticas['total_vendido'] = productos_estadisticas['total_vendido'].round(2)
    productos_estadisticas['promedio'] = productos_estadisticas['promedio'].round(2)
    productos_estadisticas['desviacion_estandar'] = productos_estadisticas['desviacion_estandar'].round(2)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records')  # Cambiado para incluir estadísticas por producto
    }

    return data

def venta_detalle_producto_8():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        ['sum', 'mean', 'std']).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'promedio', 'desviacion_estandar']

    # Redondear los resultados a 2 decimales
    tendencia_central[['promedio', 'desviacion_estandar']] = tendencia_central[['promedio', 'desviacion_estandar']].round(2)
    tendencia_central['total_vendido'] = tendencia_central['total_vendido'].round(2)

    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()

    # Definir colores para los productos
    COLORS = ['#007bff', '#17a2b8', '#28a745', '#20c997', '#00bcd4']

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

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )

    # Configurar el eje X
    fig_acumulado.update_xaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig_acumulado.update_yaxes(
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Mostrar el gráfico de total acumulado
    PLOT_ACUMULADO = plot(fig_acumulado, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Preparar los datos para la tabla de estadísticas generales
    stats_generales = tendencia_central.groupby('año').agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()

    # Redondear los resultados a 2 decimales
    stats_generales['total_vendido'] = stats_generales['total_vendido'].round(2)
    stats_generales['promedio'] = stats_generales['promedio'].round(2)
    stats_generales['desviacion_estandar'] = stats_generales['desviacion_estandar'].round(2)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'stats_generales': stats_generales.to_dict('records'),
        'plot_acumulado': PLOT_ACUMULADO  # Añadir el gráfico acumulado al contexto
    }

    return data

def venta_detalle_producto_9():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central por año, mes y producto
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        ['sum', 'mean', 'std']).reset_index()
    tendencia_central.columns = ['año', 'mes', 'producto', 'total_vendido', 'promedio', 'desviacion_estandar']

    # Redondear los resultados a 2 decimales
    tendencia_central[['promedio', 'desviacion_estandar']] = tendencia_central[['promedio', 'desviacion_estandar']].round(2)
    tendencia_central['total_vendido'] = tendencia_central['total_vendido'].round(2)
    
    # Aplicar formato numérico
    #tendencia_central['total_vendido'] = tendencia_central['total_vendido'].apply(lambda x: f"{x:,.2f}")
    #tendencia_central['promedio'] = tendencia_central['promedio'].apply(lambda x: f"{x:,.2f}")
    #tendencia_central['desviacion_estandar'] = tendencia_central['desviacion_estandar'].apply(lambda x: f"{x:,.2f}")


    # Convertir el número del mes en nombre
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][x-1])

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

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,  # Esto hace que sea un gráfico de anillo
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',  # Mostrar porcentaje y etiqueta en el gráfico
        insidetextorientation='radial',
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

  
    #productos_estadisticas = tendencia_central.groupby('producto').agg(
    #    total_vendido=('total_vendido', 'sum'),
    #    promedio=('promedio', 'mean'),
    #    desviacion_estandar=('desviacion_estandar', 'mean')
    #).reset_index()
    productos_estadisticas = tendencia_central.groupby(['producto', 'año']).agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()

    
    # Ordenar por 'total_vendido' en orden descendente
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)
    
    # Redondear los resultados a 2 decimales
    productos_estadisticas['total_vendido'] = productos_estadisticas['total_vendido'].round(2)
    productos_estadisticas['promedio'] = productos_estadisticas['promedio'].round(2)
    productos_estadisticas['desviacion_estandar'] = productos_estadisticas['desviacion_estandar'].round(2)
    
    # Formatear los números para que tengan comas cada tres dígitos
    productos_estadisticas['total_vendido'] = productos_estadisticas['total_vendido'].apply(lambda x: f"{x:,.2f}")
    productos_estadisticas['promedio'] = productos_estadisticas['promedio'].apply(lambda x: f"{x:,.2f}")
    productos_estadisticas['desviacion_estandar'] = productos_estadisticas['desviacion_estandar'].apply(lambda x: f"{x:,.2f}")
    

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        #'plot_acumulado': PLOT_ACUMULADO,  # Añadir el gráfico acumulado al contexto
        'plot_pie': PLOT_PIE  # Añadir el gráfico de pastel al contexto
    }

    return data


def venta_detalle_producto_10():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum', promedio='mean', desviacion_estandar='std').reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular estadísticas
    productos_estadisticas = tendencia_central.groupby('producto').agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'mean')
    ).reset_index()

    # Ordenar y redondear resultados
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)
    productos_estadisticas = productos_estadisticas.round(2)

    # Formatear números
    for col in ['total_vendido', 'promedio', 'desviacion_estandar']:
        productos_estadisticas[col] = productos_estadisticas[col].apply(lambda x: f"{x:,.2f}")

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE
    }

    return data

def venta_detalle_producto_11():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular estadísticas
    productos_estadisticas = tendencia_central.groupby('producto').agg(
        total_vendido=('total_vendido', 'sum'),
        promedio=('promedio', 'mean'),
        desviacion_estandar=('desviacion_estandar', 'std')  # Cambié 'mean' a 'std' para reflejar correctamente la variabilidad
    ).reset_index()

    # Ordenar y redondear resultados
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)
    productos_estadisticas = productos_estadisticas.round(2)

    # Formatear números
    for col in ['total_vendido', 'promedio', 'desviacion_estandar']:
        productos_estadisticas[col] = productos_estadisticas[col].apply(lambda x: f"{x:,.2f}")

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE
    }

    return data



def venta_detalle_producto_13():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    print(df_top)

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular estadísticas
    #productos_estadisticas = df_top.groupby('producto').agg(
    #    total_vendido=('cantidad', 'sum'),
    #    promedio=('cantidad', 'mean'),
    #    desviacion_estandar=('cantidad', 'std')
    #).reset_index()
    #
    ## Redondear resultados
    #productos_estadisticas = productos_estadisticas.round(2)
    
    # Calcular estadísticas
    productos_estadisticas = df_top.groupby('producto').agg(
        total_vendido=lambda x: x.sum(),
        promedio=lambda x: x.mean(),
        desviacion_estandar=lambda x: x.std()
    ).reset_index()
    
    # Calcular el promedio y la desviación estándar anual por producto
    estadisticas_anuales = df_top.groupby(['producto', 'año'])['cantidad'].agg(
        promedio_anual=lambda x: x.mean(),
        desviacion_estandar_anual=lambda x: x.std()
    ).reset_index()
    
    # Calcular el promedio y la desviación estándar de estos valores por producto
    promedio_anual = estadisticas_anuales.groupby('producto')['promedio_anual'].mean().reset_index()
    promedio_anual.columns = ['producto', 'promedio_anual']
    
    desviacion_estandar_anual = estadisticas_anuales.groupby('producto')['desviacion_estandar_anual'].mean().reset_index()
    desviacion_estandar_anual.columns = ['producto', 'desviacion_estandar_anual']
    
    # Unir las estadísticas con el promedio y desviación estándar anuales
    productos_estadisticas = productos_estadisticas.merge(promedio_anual, on='producto', how='left')
    productos_estadisticas = productos_estadisticas.merge(desviacion_estandar_anual, on='producto', how='left')
    
    # Redondear resultados
    productos_estadisticas = productos_estadisticas.round(2)
    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE
    }

    return data


def venta_detalle_producto_14():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    
    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular estadísticas
    productos_estadisticas = df_top.groupby('producto').agg(
        total_vendido=('cantidad', 'sum'),
        promedio=('cantidad', 'mean'),
        desviacion_estandar=('cantidad', 'std')
    ).reset_index()

    # Calcular el promedio y la desviación estándar anual por producto
    estadisticas_anuales = df_top.groupby(['producto', 'año'])['cantidad'].agg(
        promedio_anual='mean',
        desviacion_estandar_anual='std'
    ).reset_index()

    # Calcular el promedio y la desviación estándar de estos valores por producto
    promedio_anual = estadisticas_anuales.groupby('producto')['promedio_anual'].mean().reset_index()
    promedio_anual.columns = ['producto', 'promedio_anual']
    
    desviacion_estandar_anual = estadisticas_anuales.groupby('producto')['desviacion_estandar_anual'].mean().reset_index()
    desviacion_estandar_anual.columns = ['producto', 'desviacion_estandar_anual']
    
    # Unir las estadísticas con el promedio y desviación estándar anuales
    productos_estadisticas = productos_estadisticas.merge(promedio_anual, on='producto', how='left')
    productos_estadisticas = productos_estadisticas.merge(desviacion_estandar_anual, on='producto', how='left')
    
    # Redondear resultados
    productos_estadisticas = productos_estadisticas.round(2)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE
    }

    return data




def venta_detalle_producto_main():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    print(df_top)

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular estadísticas
    #productos_estadisticas = df_top.groupby('producto')['cantidad'].agg(
    #    total_vendido='sum',
    #    promedio='mean',
    #    desviacion_estandar='std'
    #).reset_index()
    #print(productos_estadisticas)
    
    # Calcular estadísticas por producto y año
    #productos_estadisticas = df_top.groupby(['producto', 'año'])['cantidad'].agg(
    #    total_vendido='sum',
    #    promedio='mean',
    #    desviacion_estandar='std'
    #).reset_index()
    
    # Calcular el total vendido por producto y año
    total_vendido_por_año = df_top.groupby(['producto', 'año'])['cantidad'].sum().reset_index()

# Calcular el total vendido general y el promedio total vendido por producto
    productos_estadisticas = total_vendido_por_año.groupby('producto')['cantidad'].agg(
        total_vendido='sum',         # Total vendido
        promedio='mean',             # Promedio total vendido
        desviacion_estandar='std'    # Desviación estándar
    ).reset_index()

    # Redondear resultados
    productos_estadisticas = productos_estadisticas.round(2)

    # Ordenar por total vendido
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)

    # Formatear números
    for col in ['total_vendido', 'promedio', 'desviacion_estandar']:
        productos_estadisticas[col] = productos_estadisticas[col].apply(lambda x: f"{x:,.2f}")

    # Mostrar el DataFrame de estadísticas
    print(productos_estadisticas)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE
    }

    return data


def venta_detalle_producto_main_1():
    TOP = 5
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    print(df_top)

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico de barras apiladas
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular el total vendido por producto y año
    total_vendido_por_año = df_top.groupby(['producto', 'año'])['cantidad'].sum().reset_index()

    # Calcular el total vendido general y el promedio total vendido por producto
    productos_estadisticas = total_vendido_por_año.groupby('producto')['cantidad'].agg(
        total_vendido='sum',         # Total vendido
        promedio='mean',             # Promedio total vendido
        desviacion_estandar='std'    # Desviación estándar
    ).reset_index()

    # Redondear resultados
    productos_estadisticas = productos_estadisticas.round(2)

    # Ordenar por total vendido
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)

    # Formatear números
    for col in ['total_vendido', 'promedio', 'desviacion_estandar']:
        productos_estadisticas[col] = productos_estadisticas[col].apply(lambda x: f"{x:,.2f}")

    # Mostrar el DataFrame de estadísticas
    print(productos_estadisticas)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'plot_pie': PLOT_PIE,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        
    }

    
    return data

def venta_detalle_producto():
    TOP = 8
    # Obtener los datos de ventas
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    #print(df_top)

    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0)

    # Calcular medidas de tendencia central
    tendencia_central = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].agg(
        total_vendido='sum',
        promedio='mean',
        desviacion_estandar='std'
    ).reset_index()

    # Redondear los resultados a 2 decimales
    tendencia_central = tendencia_central.round(2)

    # Convertir el número del mes en nombre
    meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
                     'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    tendencia_central['mes'] = tendencia_central['mes'].apply(lambda x: meses_nombres[x - 1])

    # Crear la figura para el gráfico de barras apiladas
    fig = go.Figure()
    for i, producto in enumerate(TOP_PRODUCTO):
        fig.add_trace(go.Bar(
            x=ventas_por_mes_producto.index.get_level_values('mes'),
            y=ventas_por_mes_producto[producto],
            name=producto,
            marker_color=COLORS[i % len(COLORS)]
        ))

    # Configurar el layout del gráfico de barras apiladas
    fig.update_layout(
        title=f'Top {TOP} Productos Más Vendidos',
        xaxis_title='Mes',
        yaxis_title='Cantidad de Ventas',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Configurar el eje X
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        title_font=dict(color='#f8f9fa'),
        tickfont=dict(color='#f8f9fa')
    )

    # Configurar el eje Y
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))

    # Mostrar el gráfico
    PLOT = plot(fig, include_plotlyjs=True, output_type='div')

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']

    # Crear la figura para el gráfico de total acumulado
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Bar(
        x=total_acumulado['producto'],
        y=total_acumulado['total_acumulado'],
        marker_color='#ff5733'
    ))

    # Configurar el layout del gráfico de total acumulado
    fig_acumulado.update_layout(
        title='Total Acumulado Vendido por Producto',
        xaxis_title='Producto',
        yaxis_title='Total Vendido (kg/piezas)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Crear el gráfico de pastel para los productos más vendidos
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        hole=.3,
        marker=dict(colors=COLORS[:TOP]),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    # Configurar el layout del gráfico de pastel
    fig_pie.update_layout(
        title='Distribución de Ventas de los Productos Más Vendidos',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    # Mostrar el gráfico de pastel
    PLOT_PIE = plot(fig_pie, include_plotlyjs=True, output_type='div')

    # Preparar los datos para el contexto, organizando por producto
    productos_data = {
        producto: tendencia_central[tendencia_central['producto'] == producto].to_dict('records')
        for producto in TOP_PRODUCTO
    }

    # Calcular el total vendido por producto y año
    total_vendido_por_año = df_top.groupby(['producto', 'año'])['cantidad'].sum().reset_index()

    # Calcular el total vendido general y el promedio total vendido por producto
    productos_estadisticas = total_vendido_por_año.groupby('producto')['cantidad'].agg(
        total_vendido='sum',         # Total vendido
        promedio='mean',             # Promedio total vendido
        desviacion_estandar='std'    # Desviación estándar
    ).reset_index()

    # Redondear resultados
    productos_estadisticas = productos_estadisticas.round(2)

    # Ordenar por total vendido
    productos_estadisticas = productos_estadisticas.sort_values(by='total_vendido', ascending=False)

    # Formatear números
    for col in ['total_vendido', 'promedio', 'desviacion_estandar']:
        productos_estadisticas[col] = productos_estadisticas[col].apply(lambda x: f"{x:,.2f}")

    # Mostrar el DataFrame de estadísticas
    print(productos_estadisticas)

    #cantidad_vendida_por_año = total_vendido_por_año.pivot(index='año', columns='producto', values='cantidad').fillna(0)

# Redondear resultados a 2 decimales
    #cantidad_vendida_por_año = cantidad_vendida_por_año.round(2)
    
    # Crear la tabla con la cantidad de productos vendidos por año de cada uno de los top productos
    cantidad_vendida_por_año = total_vendido_por_año.pivot(index='año', columns='producto', values='cantidad').fillna(0)

    # Redondear resultados
    cantidad_vendida_por_año = cantidad_vendida_por_año.round(2)

    # Convertir a DataFrame con un índice reset para que 'año' sea una columna
    cantidad_vendida_por_año.reset_index(inplace=True)

# Mostrar la tabla de cantidad vendida por año en la consola para verificar
    print(cantidad_vendida_por_año)

    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'plot_pie': PLOT_PIE,
        'cantidad_vendida_por_año': cantidad_vendida_por_año.to_dict('records')  # Agregar aquí la nueva tabla
    }

    return data


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