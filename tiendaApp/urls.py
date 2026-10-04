from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('receta/<slug:slug>/', views.receta_detalle, name='receta_detalle'),
    path('tienda/', views.tienda, name='tienda'),
    # El antiguo /catalogo/ redirige a la tienda (el footer aún enlaza con este nombre)
    path('catalogo/', RedirectView.as_view(pattern_name='tienda', permanent=False), name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
]
