from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from tiendaApp import datos
from tiendaApp.forms import ContactoForm, ProductoForm
from tiendaApp.models import Producto

# Vista de inicio: envía las recetas (saladas y dulces) y el carrusel a la plantilla
def inicio(request):
    recetas = datos.obtener_recetas()
    carrusel = datos.obtener_carrusel(recetas)
    contexto = {
        # una receta nueva aparece en su categoría (con la etiqueta "Nueva")
        'recetas_saladas': [r for r in recetas if r['tipo'] == 's'],
        'postres': [r for r in recetas if r['tipo'] == 'p'],
        # la lista se repite dos veces para el efecto infinito del carrusel
        'carrusel': carrusel * 2,
        'total_carrusel': len(carrusel),
    }
    return render(request, 'tiendaApp/inicio.html', contexto)

# --- Receta completa ---
def receta_detalle(request, slug):
    receta = datos.obtener_receta(slug)
    if receta is None:
        raise Http404('Receta no encontrada')
    return render(request, 'tiendaApp/receta_detalle.html', {'receta': receta})

# --- Tienda de productos (ciclo for sobre la base de datos) ---
def tienda(request):
    productos = Producto.objects.select_related('categoria', 'personaje')
    return render(request, 'tiendaApp/tienda.html', {'productos': productos})

# --- Formulario de contacto ---
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            datos.guardar_contacto(form)
            messages.success(request, '¡Gracias! Recibimos tu mensaje.')
            return redirect('contacto')
    else:
        form = ContactoForm()
    return render(request, 'tiendaApp/contacto.html', {'form': form})

# --- VISTA PARA EL FORMULARIO DE PRODUCTOS ---
def crear_producto(request):
    if request.method == 'POST': # Verificamos que corresponda a un POST (envío de datos)
        form = ProductoForm(request.POST) # Recoge los valores del formulario
        if form.is_valid(): # Si cumple con las validaciones
            form.save() # Guardamos los valores en la base de datos
            return redirect('inicio') # Redirigimos a la página de inicio al terminar
    else:
        form = ProductoForm() # En caso de ser GET, muestra el formulario vacío
    
    # Retornamos el formulario para que se dibuje en el template
    return render(request, 'tiendaApp/productoAdd.html', {'form': form})
