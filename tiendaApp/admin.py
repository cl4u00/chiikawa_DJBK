from django.contrib import admin
from tiendaApp.models import Categoria, Contacto, Personaje, Producto, Receta

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

class PersonajeAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'tamano', 'precio', 'categoria', 'personaje']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Personaje, PersonajeAdmin)
admin.site.register(Producto, ProductoAdmin)

class RecetaAdmin(admin.ModelAdmin):
    list_display = ['orden', 'nombre', 'tipo', 'orden_carrusel', 'nueva']

class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo', 'asunto', 'creado']

admin.site.register(Receta, RecetaAdmin)
admin.site.register(Contacto, ContactoAdmin)
