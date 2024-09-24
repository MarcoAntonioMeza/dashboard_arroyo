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


def consulta_sql(sql='SELECT * FROM view_venta;'):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columnas = [col[0] for col in cursor.description]  # Obtener los nombres de las columnas
        resultados = cursor.fetchall()  # Obtener todos los resultados
    
    # Convertir los resultados en un DataFrame de pandas
    df = pd.DataFrame(resultados, columns=columnas)
    
    return df


def ventas_anio_totales_():
    df = consulta_sql()
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s').dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    data_por_anio = df.groupby('year').size().reset_index(name='ventas')
    
    
     # Crear el gráfico
    # Crear el gráfico
    fig = px.bar(data_por_anio, x='year', y='ventas', 
                 title='Número de Ventas por Año',
                 labels={'year': 'Año', 'ventas': 'Número de Ventas'})
    
    # Convertir a HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html



def ventas_anio_totales():
    df = consulta_sql()
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s').dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')
    df['year'] = df['created_at'].dt.year
    data_por_anio = df.groupby('year').size()

    # Crear la figura de la gráfica
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_por_anio.index,
        y=data_por_anio.values,
        marker_color='skyblue',
        name='Número de Ventas',
        #text=data_por_anio.values,
        text=[f'{int(val):,}' for val in data_por_anio.values],
        textposition='auto'
    ))

    # Añadir una línea de tendencia
    fig.add_trace(go.Scatter(
        x=data_por_anio.index,
        y=data_por_anio.values,
        mode='lines+markers',
        name='Tendencia',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))

    # Añadir título y etiquetas
    fig.update_layout(
        title='Número de Ventas por Año',
        xaxis_title='Año',
        yaxis_title='Número de Ventas',
        template='plotly_white',
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Configurar el eje X para que muestre solo enteros
    fig.update_xaxes(tickvals=list(data_por_anio.index), ticktext=list(map(str, data_por_anio.index)))

    # Renderizar la gráfica y retornar el HTML
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    return graph_html