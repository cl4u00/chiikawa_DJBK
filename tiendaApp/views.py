from django.contrib import messages
from django.shortcuts import render, redirect
from tiendaApp import datos
from tiendaApp.forms import ContactoForm, ProductoForm
from tiendaApp.models import Producto

# Tu vista de inicio que ya tenías (ahora envía recetas y carrusel a la plantilla)
def inicio(request):
    recetas = datos.obtener_recetas()
    carrusel = datos.obtener_carrusel(recetas)
    contexto = {
        'recetas_saladas': [r for r in recetas if r['tipo'] == 's' and not r.get('nueva')],
        'postres': [r for r in recetas if r['tipo'] == 'p' and not r.get('nueva')],
        'recetas_nuevas': [r for r in recetas if r.get('nueva')],
        # la lista se repite dos veces para el efecto infinito del carrusel
        'carrusel': carrusel * 2,
        'total_carrusel': len(carrusel),
    }
    return render(request, 'tiendaApp/inicio.html', contexto)

# --- Catálogo de productos (ciclo for sobre la base de datos) ---
def catalogo(request):
    productos = Producto.objects.select_related('categoria', 'personaje')
    return render(request, 'tiendaApp/catalogo.html', {'productos': productos})

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
