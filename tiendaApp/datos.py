"""Acceso a los datos del sitio.

FUENTE_DATOS (settings.py) decide de dónde salen recetas y contactos:
  'json'  -> archivos de la carpeta data/
  'mysql' -> base de datos (después de `python manage.py cargar_json`)
"""
import json

from django.conf import settings
from django.utils import timezone


def _usa_mysql():
    return settings.FUENTE_DATOS == 'mysql'


def _leer_json(nombre, defecto):
    try:
        with open(settings.DATA_DIR / nombre, encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return defecto


def _escribir_json(nombre, contenido):
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(settings.DATA_DIR / nombre, 'w', encoding='utf-8') as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=2)
        archivo.write('\n')


# --- Recetas -------------------------------------------------------------

def obtener_recetas():
    """Lista de recetas (dict) ordenadas por el campo 'orden'."""
    if _usa_mysql():
        from tiendaApp.models import Receta
        return [receta.como_dict() for receta in Receta.objects.all()]
    return sorted(_leer_json('recetas.json', []), key=lambda r: r['orden'])


def obtener_carrusel(recetas=None):
    """Recetas que aparecen en el carrusel, en el orden de 'orden_carrusel'."""
    recetas = obtener_recetas() if recetas is None else recetas
    return sorted((r for r in recetas if r['orden_carrusel']), key=lambda r: r['orden_carrusel'])


# --- Contactos -----------------------------------------------------------

def guardar_contacto(form):
    """Guarda un ContactoForm ya validado, en JSON o en MySQL según FUENTE_DATOS."""
    if _usa_mysql():
        form.save()
        return
    contactos = _leer_json('contactos.json', [])
    registro = dict(form.cleaned_data)
    registro['creado'] = timezone.localtime().isoformat()
    contactos.append(registro)
    _escribir_json('contactos.json', contactos)
