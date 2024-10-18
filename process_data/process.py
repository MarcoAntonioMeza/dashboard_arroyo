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

"""
====================================================
          CONSULTAS SQL
=====================================================
"""
def consulta_sql(sql = VENTAS):
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columnas = [col[0] for col in cursor.description]
        resultados = cursor.fetchall()

    df = pd.DataFrame(resultados, columns=columnas)
    return df




"""
====================================================
            VENTAS $ POR MES/AÑO
====================================================
"""
def ventas_mes_df(anio):
    
    df = consulta_sql()
    
    df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    
    df_year = df[df['year'] == anio]
    
    ingresos = df_year.groupby(df_year['created_at'].dt.month)['total'].sum()
    
   
    
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
    
    
"""
====================================================
            VENTAS $ GENERALES
====================================================
"""
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
    #total_ventas =f'{round(df["total"].count()):,}'
    #promedio_ventas = ventas.mean()
    #promedio_ventas = f'{round(promedio_ventas):,}'
    #std_ventas = f'{round(ventas.std()):,}'
    
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
    
    
    #VENTAS = {
    #    'total': total_ventas,
    #    'promedio': promedio_ventas,
    #    'std': std_ventas,
    #    'plot': draw_plot(ventas.index, ventas.values, 'CANTIDAD DE VENTAS','AÑO','tOTAL DE VENTAS',False)
    #}
    
    return {
        'ingresos': INGRESOS,
        #'ventas': VENTAS
    }



"""
====================================================
        VENTAS POR PRODUCTO
====================================================
"""
def venta_detalle_producto():
    TOP = 8
    df_vD = consulta_sql(VENTA_DETALLE)
    df_vD['fecha'] = pd.to_datetime(df_vD['fecha'])
    df_vD['año'] = df_vD['fecha'].dt.year
    df_vD['mes'] = df_vD['fecha'].dt.month

    # Identificar los productos más vendidos
    productos_mas_vendidos = df_vD.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
    TOP_PRODUCTO = productos_mas_vendidos.head(TOP).index.tolist()
    df_top = df_vD[df_vD['producto'].isin(TOP_PRODUCTO)]
    
    # Agrupar por año, mes y producto para calcular las ventas
    ventas_por_mes_producto = df_top.groupby(['año', 'mes', 'producto'])['cantidad'].sum().unstack(fill_value=0).reset_index()
    
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
    
    # Ordenar el DataFrame por año y mes
    ventas_por_mes_producto = ventas_por_mes_producto.sort_values(['mes'],ascending=[True])
    # Crear una nueva columna con el nombre del mes
    ventas_por_mes_producto['mes'] = ventas_por_mes_producto['mes'].apply(lambda x: meses_nombres[x - 1])

    


    PLOT = crear_grafico_barras(
        data=ventas_por_mes_producto,
        x='mes',
        y=TOP_PRODUCTO,
        nombres=TOP_PRODUCTO,
        colores=COLORS,
        titulo=f'Top {TOP} Productos Más Vendidos',
        x_titulo='Mes',
        y_titulo='Cantidad de Ventas',
        es_apilado=False
    )

    # Calcular total acumulado vendido por producto
    total_acumulado = df_vD.groupby('producto')['cantidad'].sum().reset_index()
    total_acumulado.columns = ['producto', 'total_acumulado']


    PLOT_PIE = crear_grafico_pie(
        labels=TOP_PRODUCTO,
        values=productos_mas_vendidos[TOP_PRODUCTO],
        colores=COLORS[:TOP],
        titulo='Distribución de Ventas de los Productos Más Vendidos'
    )
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

  
    
    # Crear la tabla con la cantidad de productos vendidos por año de cada uno de los top productos
    cantidad_vendida_por_año = total_vendido_por_año.pivot(index='año', columns='producto', values='cantidad').fillna(0)

    # Redondear resultados
    cantidad_vendida_por_año = cantidad_vendida_por_año.round(2)

    # Convertir a DataFrame con un índice reset para que 'año' sea una columna
    cantidad_vendida_por_año.reset_index(inplace=True)

    # Mostrar la tabla de cantidad vendida por año en la consola para verificar
    #print(cantidad_vendida_por_año)

   
    
    
    # Preparar los datos para el contexto
    data = {
        'plot': PLOT,
        'top_productos': TOP_PRODUCTO,
        'plot_pie': PLOT_PIE,
        
        
        'productos_data': productos_data,
        'productos_estadisticas': productos_estadisticas.to_dict('records'),
        'cantidad_vendida_por_año': cantidad_vendida_por_año.to_dict('records')  # Agregar aquí la nueva tabla
    }

    return data











"""
==========================================
        GRAFICAR
==========================================
"""

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


def crear_grafico_barras(data, x, y, nombres, colores, titulo, x_titulo, y_titulo, es_apilado=False):
    """
    Crea un gráfico de barras reutilizable.
    :param data: Datos para la gráfica.
    :param x: Datos del eje X.
    :param y: Lista de nombres de las series para el eje Y.
    :param nombres: Lista de nombres de las series.
    :param colores: Lista de colores para las series.
    :param titulo: Título del gráfico.
    :param x_titulo: Título del eje X.
    :param y_titulo: Título del eje Y.
    :param es_apilado: Booleano para apilar las barras.
    """
    fig = go.Figure()
    for i, nombre in enumerate(nombres):
        fig.add_trace(go.Bar(
            x=data[x],
            y=data[nombre],
            name=nombre,
            marker_color=colores[i % len(colores)]
        ))

    fig.update_layout(
        title=titulo,
        xaxis_title=x_titulo,
        yaxis_title=y_titulo,
        
        barmode='stack' if es_apilado else 'group',
        template='plotly_dark',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    fig.update_xaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))
    fig.update_yaxes(title_font=dict(color='#f8f9fa'), tickfont=dict(color='#f8f9fa'))
    
    return plot(fig, include_plotlyjs=True, output_type='div')

def crear_grafico_pie(labels, values, colores, titulo):
    """
    Crea un gráfico de pastel reutilizable.
    :param labels: Etiquetas para las porciones del gráfico.
    :param values: Valores para cada porción.
    :param colores: Lista de colores para las porciones.
    :param titulo: Título del gráfico.
    """
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker=dict(colors=colores),
        textinfo='percent+label',
        insidetextorientation='radial'
    ))

    fig.update_layout(
        title=titulo,
        template='plotly_dark',
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )

    return plot(fig, include_plotlyjs=True, output_type='div')

def crear_grafico_barras_acumuladas(data, x, y, color, titulo, x_titulo, y_titulo):
    """
    Crea un gráfico de barras acumuladas reutilizable.
    :param data: Datos para la gráfica.
    :param x: Datos del eje X.
    :param y: Datos del eje Y.
    :param color: Color de las barras.
    :param titulo: Título del gráfico.
    :param x_titulo: Título del eje X.
    :param y_titulo: Título del eje Y.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[x],
        y=data[y],
        marker_color=color
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title=x_titulo,
        yaxis_title=y_titulo,
        template='plotly_dark',
        font=dict(color='#f8f9fa'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40'
    )
    
    return plot(fig, include_plotlyjs=True, output_type='div')
