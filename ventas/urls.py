from django.urls import path
import ventas.views  as v

urlpatterns = [
     path('',v.index, name='ventas_index'),
]