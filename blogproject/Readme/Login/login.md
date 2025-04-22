# LOGIN
Para poder modificar el login primero fue necesario asegurarnos de que en `blogproject/settings.py`en la sección de INSTALLED_APPS se encontrara la opción relacionada con auth ya instalada

``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogapp',
    'widget_tweaks',
    # se agrega despues "accounts",  # new
] 
```

Ahora para utilizar el `auth` es necesario agregarlo a `blogproject/urls.py` para ello es necesario agregar arriba un `include` de `from django.urls import path, include` y crear una nueva URL en `accounts/`. Ahora bien tomando en cuenta que ya existe la linea de include asi que solo seria necesario agregar la URL. 

```python
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
]
```

Ahora con esto ya habremos agregado algunas vistas para manejar el login, logout, cambio de contraseña entre otros. 

## PÁGINA DE LOGIN 

Ahora bien, Django normalmente va a intentar buscar un folder llamado `registration` dentro de `templates` para encontrar las plantillas de autentificacion. En este caso la plantilla de autentificacion es llamada `login.html`.

Ahora bien, actualmente en el codigo original no existe la ruta `templates/registration` asi que será necesario crearla a nivel de raiz, es decir en donde se encuentran otras carpetas como `blogapp` o `blogproject`

Posteriormente requeriremos tambien la creacion de un archivo login en `templates/registration/login.html` 

A este codigo `login.html` sera necesario agregarle lo siguiente

```html
<!-- templates/registration/login.html -->
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Log In</button>
</form>
```

Este código es un formulario estándar de Django que utiliza el método `POST` para enviar datos. También usa la etiqueta `{% csrf_token %}` por motivos de seguridad, específicamente para prevenir un ataque CSRF (Cross-Site Request Forgery).

El contenido del formulario se muestra usando `{{ form }}`, y luego se añade un botón de "submit" para enviar la información.

Ahora, necesitamos modificar el archivo `settings.py` que se encuentra a nivel de proyecto para que busque el folder `templates` a nivel de proyecto. en este caso modificaremos especificamente `DIRS` en `TEMPLATES`. Solo se realizara en una linea del archivo. 

``` python
# django_project/settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'blogapp/templates/blogapp'],
        ...
    },
]
```
Ahora bien cabe recalcar que lo unico que se agrego fue `"DIRS": [BASE_DIR / "templates"],` sin embargo como ya existia a nivel proyecto informacion agregada en DIRS era necesario separar con comas la nueva de la preexistente ya que simplemente estamos agregando mas informacion a la linea de `DIRS`. Anteriormente solo existia `'DIRS': [ BASE_DIR / 'blogapp/templates/blogapp'],`

Esta línea dentro de la configuración TEMPLATES de Django le dice al proyecto dónde buscar las plantillas HTML personalizadas que creemos.

Una vez hecho esto, la funcionalidad deberia funcionar parcialmente basado en los objetivos del proyecto pero requerimos realizar otra modificacion en `settings.py` para que el usuario pueda ir al inicio una vez realizado un Login exitoso, para ello sera necesario usar `LOGIN_REDIRECT_URL` al final del archivo `blogproject/settings.py`

```python
# django_project/settings.py
LOGIN_REDIRECT_URL = "/"  # new
```

UNa vez realizada esta modificacion podemos acceder a `http://127.0.0.1:8000/accounts/login/` y veremos una paguina de login bastante simple pero que es capas de controlar el acceso al sitio. 

Ahora bien. Cabe recalcar que sino hemos creado un usuario no podremos iniciar sesion. Para ello es necesario colocar en el terminal de anaconda `python manage.py createsuperuser` para crear un usuario y contraseña con el que iniciar sesión. Cabe recalcar que este usuario tendra permisos elevados dentro del blog y podra entrar a la pagina de admin. 

## LOGIN Obligatorio antes de entrar

Este aspecto esta relacionado con lo anterior, de manera que se asegura de que los usuarios no puedan acceder a funcionalidades sin que lo tengan permitido para ello nos iremos al archivo `blogapp/views.py` para agregar una opcion que obligue a ir a la pagina de login primero. en este caso es el `LoginRequiredMixin` 

```python
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
```
lo unico que se modifica es aquelllo que esta entre parentesis dentro en `BlogListView(LoginRequiredMixin, ListView)` alli originalmente se encontraba como `BlogListView(LoginRequiredMixin)` sin solicitar un Login

## Boton de LOGOUT

Para ello requerimos modificar el archivo `blogapp/templates/base.html`. Agregamos una seccion para hacer una solicitud HTTP de tipo `POST` usando un `FORM`. 

La modificacion se realizara en esta seccion del codigo original

```html
        {% if user.is_authenticated %}
          <a href="{% url 'blogapp:add_blog' %}" class="bg-blue-500 hover:bg-blue-600 text-white dark:bg-blue-600 dark:hover:bg-blue-700 dark:text-white font-medium py-2 px-4 rounded transition-all duration-500 ease-in-out">New Blog</a>
        {% endif %}
```
Esta seccion se encuentra aproximadamente en la linea 58 del codigo original`

```html

        {% if user.is_authenticated %}
          <a href="{% url 'blogapp:add_blog' %}" class="bg-blue-500 hover:bg-blue-600 text-white dark:bg-blue-600 dark:hover:bg-blue-700 dark:text-white font-medium py-2 px-4 rounded transition-all duration-500 ease-in-out">New Blog</a>
          <form action="{% url 'logout' %}" method="post"> 
            {% csrf_token %}
            <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded transition-all duration-500 ease-in-out">
              Log Out 
            </button>
          </form>
        {% endif %}
```
Esta configuracion tambien incluye la estetica del nuevo boton.

Ahora es necesario hacer que despues de cerrar sesion el usuario sea redireccionado, esto se hace modificando `blogproject/settings.py` agregando una linea similar a la redireccion necesaria despues de iniciar sesión. Esta linea debe estar al final del archivo

```python
# django_project/settings.py
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"  # new
```

## Pagina de Sign Up

Necesitamos crear una app llamada `accounts`. Para esto utilizaremos el terminal, en donde escribiremos el siguiente comando: 

```powershell
(.venv) $ python manage.py startapp accounts
```

Ahora debemos agregar la nueva app en la seccion `INSTALLED_APPS` de `blogproject/settings.py`

```python
# django_project/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",  # new
]
```

Ahora sera necesario agregar una URL path en `blogproject/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')), 
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")), 
]
```

Ahora creamos un archivo llamado `accounts/urls.py` y con el siguiente código

```python
# accounts/urls.py
from django.urls import path

from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```
Y posteriormente el archivo `accounts/views.py`

```python
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

Ahora creamos una plantilla, `templates/registration/signup.html` y le colocamos el siguiente codigo

```html
<!-- templates/registration/signup.html -->

{% block title %}Sign Up{% endblock %}

{% block content %}
<h2>Sign up</h2>
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Sign Up</button>
</form>
{% endblock %}
```

Posteiormente modificamos el login para que incluya la opcion de crear un usuario, esta debe redirigir al Sign Up

```html
<!-- templates/registration/login.html -->
 <h2>Log In</h2>
 <form method="post">
   {% csrf_token %}
   {{ form }}
   <button type="submit">Log In</button>
   
 <p>Don't have an account? <a href="{% url 'signup' %}">Sign up here</a></p>
 </form>
```

Hasta esta seccion se han añadido funcionalidades necesarias en el codigo principal. Ahora bien posteriormente se hicieron modificaciones en el diseño relacionadas con el codigo principal que cambian algunas secciones de este codigo. 
Esta guia solo incluira aquello no relacionado con el diseño. En otra guia podria añadirse informacion sobre modificaciones pertinentes al diseño. 














