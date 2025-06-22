# **Optimizacion del ORM** #
Para poder realizar esta optimizacion primero es importante ver las secciones de codigo en las que puede estarse usando las llamadas a la base de datos de manera poco optimizada agregando el siguiente codigo al `settings.py`
``` Python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'nplusone': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

Poteriormente es importante la instalacion de la libreria debug-toolbar para ver ejecuciones de querys y ese tipo de cosas en el 
codigo
`pip install django-debug-toolbar`

Se realizaron ciertas modificaciones en `url.py` y `settings.py` para hacer uso de esta libreria dentro del codigo al final esto genera una barra lateral con temas de ciertas cosas que se consumen en la ejecucion

### **Uso de  `nplusone`** ###

Primero se debe instalar la libreria
`pip install nplusone`

Esta libreria permitira detectar errores del tipo N+1 dentro del codigo.
Lo ideal para realizar pruebas iniciales de funcionamiento es crear una vista falsa con errores a proposito y que asi se puedan corregir

A continuacion se modifica el `views.py` anadiendo el codigo siguiente para agregar cambios pertinentes e informacion sobre la nueva vista

``` Python
def vista_prueba_nplusone(request):
    # Vista diseñada para generar un problema N+1
    blogs = Blog.objects.all()
    datos = []
    for blog in blogs:
        # Acceder a la relación M2M 'categorias' en un bucle genera consultas N+1
        categorias_nombres = [categoria.nombre for categoria in blog.categorias.all()]
        datos.append({
            'titulo': blog.title,
            'categorias': categorias_nombres,
        })
    return render(request, 'blogapp/vista_prueba.html', {'datos': datos})
```

Se crea un archivo html para las vistas pruebas el cual se encontrara en `blogapp/templates/blogapp`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Vista de Prueba N+1</title>
</head>
<body>
    <h1>Blogs y Categorías</h1>
    <ul>
    {% for item in datos %}
        <li>{{ item.titulo }} - Categorías: {{ item.categorias|join:", " }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```
Se agrega una url al `urls.py` de blogapp mediante

```Python
path('prueba/', views.vista_prueba_nplusone, name='vista_prueba_nplusone'),
```
Tambien se anadio la importacion de una libreria en el mismo archivo por un error que se producia
`from blogapp import views`

Ahora bien en cuanto al archivo settings se anadieron las siguientes lineas por que no esta siendo capas de detectar los errores 
```Python
NPLUSONE_RAISE = False  # para que no levante excepción, solo loguee
NPLUSONE_LOGGER = True  # para que loguee en consola o archivo
```

NO funciono asi que se agrego en settings.py
`import logging #TEMPORAL` 
Se cambio el NPLUSONE LOGGER POR
`NPLUSONE_LOGGER = logging.getLogger('nplusone')`

Como los cambios funcionaron se remplazo temporal con #optimizacionORM - nplusone
En este punto aun se pueden hacer pruebas respecto a errores de N+1





