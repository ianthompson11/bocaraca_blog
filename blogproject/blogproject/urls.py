"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('blogapp.urls')),  # Conecta las URLs de blogapp
    path("accounts/", include("accounts.urls")),  # new Se esta utilizando para la seccion de Sign Up
    path("accounts/", include("django.contrib.auth.urls")),  # new
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#Profiling - Todo lo que se encuentra en este espacio es completamente nuevo - En la fusion se puede aceptar esta
#            version ya que incluye ambas cosas
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')),
    ]
#Profiling - Fin ultima modificacion

