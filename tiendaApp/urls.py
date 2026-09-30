from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear-producto/', views.crear_producto, name='crear_producto'), # Agregamos la ruta del formulario
]
