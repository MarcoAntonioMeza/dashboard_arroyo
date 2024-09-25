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

from django.db import connection

COLORS = ['#007bff', '#17a2b8', '#28a745', '#20c997', '#00bcd4', '#1e90ff', '#00fa9a', '#2e8b57', '#66cdaa', '#00ced1']
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def consulta_sql(sql='SELECT * FROM view_venta;'):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columnas = [col[0] for col in cursor.description]  # Obtener los nombres de las columnas
        resultados = cursor.fetchall()  # Obtener todos los resultados
    
    # Convertir los resultados en un DataFrame de pandas
    df = pd.DataFrame(resultados, columns=columnas)
    
    return df



def ventas_anio_totales(year):
    df = consulta_sql()
    
    
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s').dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    
    data = {
        'all':generate_grafica(df),
        'by_anio': generate_grafica_anio(df,year),
        'years': df['year'].unique()
    }
   
    return data



def generate_grafica(df):
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

    # Configurar la leyenda
    fig.update_layout(legend=dict(font=dict(color='#f8f9fa')))  # Color de la leyenda en blanco

    # Renderizar la gráfica y retornar el HTML
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    
    return graph_html


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
    
    # Filtrar el DataFrame para el año seleccionado
    df_year = df[df['year'] == year]
    data_por_mes = df_year.groupby(df_year['created_at'].dt.month).size()

    # Crear la figura con barras
    fig = go.Figure()

    # Añadir las barras con colores que corresponden al mes
    fig.add_trace(go.Bar(
        x=data_por_mes.index.astype(str),
        y=data_por_mes.values,
        marker_color=[COLORS[i % len(COLORS)] for i in range(len(data_por_mes))],  # Asignar color basado en el índice
        name='Ventas por Mes',
        text=[f'{val:,.0f}' for val in data_por_mes.values],  # Etiquetas de valor
        textposition='auto'
    ))

    # Añadir una línea de tendencia
    fig.add_trace(go.Scatter(
        x=data_por_mes.index.astype(str),
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
        tickvals=list(data_por_mes.index.astype(str)),
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