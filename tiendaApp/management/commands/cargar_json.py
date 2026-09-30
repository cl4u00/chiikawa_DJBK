import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from tiendaApp.models import Contacto, Receta


class Command(BaseCommand):
    help = 'Carga data/recetas.json y data/contactos.json en MySQL (se puede repetir sin duplicar; las recetas se sobrescriben con lo que diga el JSON).'

    def handle(self, *args, **options):
        with open(settings.DATA_DIR / 'recetas.json', encoding='utf-8') as archivo:
            recetas = json.load(archivo)
        for r in recetas:
            Receta.objects.update_or_create(
                nombre=r['nombre'],
                defaults={
                    'tipo': r['tipo'],
                    'imagen': r['imagen'],
                    'alt': r['alt'],
                    'orden': r['orden'],
                    'orden_carrusel': r['orden_carrusel'],
                    'nueva': r.get('nueva', False),
                    'ingredientes': json.dumps(r['ingredientes'], ensure_ascii=False),
                    'preparacion': json.dumps(r['preparacion'], ensure_ascii=False),
                },
            )
        self.stdout.write(self.style.SUCCESS('Recetas cargadas: {}'.format(len(recetas))))

        try:
            with open(settings.DATA_DIR / 'contactos.json', encoding='utf-8') as archivo:
                contactos = json.load(archivo)
        except FileNotFoundError:
            contactos = []
        nuevos = 0
        for c in contactos:
            _, creado = Contacto.objects.get_or_create(
                nombre=c['nombre'], correo=c['correo'], asunto=c['asunto'], mensaje=c['mensaje'],
                creado=parse_datetime(c['creado']),
            )
            nuevos += creado
        self.stdout.write(self.style.SUCCESS('Contactos nuevos: {}'.format(nuevos)))
