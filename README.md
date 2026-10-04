# Chiikawa_DJ

Proyecto Django "Mundo Chiikawa": recetas, tienda de productos, contacto, login y registro.

## Estructura

```
Chiikawa_DJ/
├── manage.py
├── requirements.txt
├── chiikawadjango/     # configuración del proyecto (settings, urls, wsgi)
├── tiendaApp/          # inicio, recetas, tienda, productos, contacto
├── cuentasApp/         # login, registro, logout
├── data/               # recetas.json, contactos.json
├── templates/          # base.html, includes/ y una carpeta por app
└── static/             # css/, js/, images/recetas/, images/iconos/
```

## Puesta en marcha (XAMPP con MySQL encendido)

```
pip install -r requirements.txt
python manage.py makemigrations tiendaApp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Datos: JSON primero, MySQL después

`FUENTE_DATOS` en `chiikawadjango/settings.py` decide de dónde salen las recetas y dónde se guardan los mensajes de contacto:

- `'json'` (por defecto): se usan los archivos de `data/`.
- `'mysql'`: se usa la base de datos. Antes ejecuta `python manage.py cargar_json`
  (pasa `data/recetas.json` y `data/contactos.json` a MySQL).

Los usuarios, los productos y el admin usan siempre MySQL.
Una receta marcada como **nueva** (en el admin o en el JSON) aparece en su categoría (saladas o postres) con la etiqueta "Nueva".

## Páginas

| Ruta | Descripción |
|------|-------------|
| `/` | Inicio: carrusel y recetas (saladas y postres) |
| `/receta/<slug>/` | Receta completa |
| `/tienda/` | Productos desde MySQL (`/catalogo/` redirige aquí) |
| `/contacto/` | Formulario de contacto |
| `/crear-producto/` | Mantenedor de productos |
| `/login/`, `/registro/`, `/logout/` | Cuentas |
| `/admin/` | Administración |
