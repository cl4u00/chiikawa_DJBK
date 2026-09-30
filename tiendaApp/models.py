import json
from django.db import models
from django.utils import timezone
from tiendaApp.choices import tamanos, tipos_receta

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Categoría')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Personaje(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Personaje')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'personaje'
        verbose_name = 'Personaje'
        verbose_name_plural = 'Personajes'

class Producto(models.Model):
    sku = models.CharField(max_length=20, verbose_name='Código SKU')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Producto')
    # Hacemos que la descripción sea opcional
    descripcion = models.CharField(max_length=250, verbose_name='Descripción', blank=True, null=True) 
    tamano = models.CharField(max_length=1, choices=tamanos, default='m')
    precio = models.PositiveIntegerField(default=10000, verbose_name='Precio')
    fecha_lanzamiento = models.DateField(blank=True, null=True, verbose_name='Fecha de Lanzamiento')
    
    categoria = models.ForeignKey(Categoria, null=False, on_delete=models.RESTRICT)
    personaje = models.ForeignKey(Personaje, null=True, on_delete=models.CASCADE)
    # Evitamos que Django exija este campo en las validaciones
    creado = models.DateTimeField(default=timezone.now, editable=False) 

    def __str__(self):
        return "{} - {}".format(self.sku, self.nombre)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['personaje', 'nombre']


class Receta(models.Model):
    """Receta del sitio. Su contenido nace en data/recetas.json y se carga a MySQL con `cargar_json`."""
    nombre = models.CharField(max_length=150, unique=True, verbose_name='Nombre de la Receta')
    tipo = models.CharField(max_length=1, choices=tipos_receta, default='s')
    imagen = models.CharField(max_length=150, verbose_name='Imagen (ruta dentro de static)')
    alt = models.CharField(max_length=200, verbose_name='Texto alternativo de la imagen')
    ingredientes = models.TextField(verbose_name='Ingredientes (JSON)')
    preparacion = models.TextField(verbose_name='Preparación (JSON)')
    orden = models.PositiveSmallIntegerField(default=0, verbose_name='Orden en la página')
    orden_carrusel = models.PositiveSmallIntegerField(default=0, verbose_name='Posición en el carrusel (0 = no aparece)')
    nueva = models.BooleanField(default=False, verbose_name='Mostrar en "Nuevas Recetas Añadidas"')
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def como_dict(self):
        """Mismo formato que una receta de recetas.json, para que la plantilla no distinga la fuente."""
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'imagen': self.imagen,
            'alt': self.alt,
            'orden': self.orden,
            'orden_carrusel': self.orden_carrusel,
            'nueva': self.nueva,
            'ingredientes': json.loads(self.ingredientes),
            'preparacion': json.loads(self.preparacion),
        }

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['orden']


class Contacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    correo = models.EmailField(verbose_name='Correo')
    asunto = models.CharField(max_length=150, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return "{} - {}".format(self.nombre, self.asunto)

    class Meta:
        db_table = 'contacto'
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-creado']
