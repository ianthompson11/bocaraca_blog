from django.contrib import admin
from django import forms
from django.contrib.admin.sites import AdminSite
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
#from blogapp.views import custom_dashboard
from .models import Blog, Review, Comment, Category  # Importa tu modelo



# Custom Admin Site
class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración de Blog"
    site_title = "Blog Admin"
    index_title = "Bienvenido al Panel de Administración"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'admin/css/custom_admin.css'
        return context
       



admin.site = CustomAdminSite()

# Formularios personalizados para usar CKEditor
class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

class ReviewAdminForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Review
        fields = '__all__'

class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = '__all__'



# ModelAdmin personalizados
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    filter_horizontal = ('categories',)  # categorias

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm



# Registro de modelos en el admin
admin.site.register(Blog, BlogAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)

@staff_member_required
def custom_dashboard(request):
    # Lógica para estadísticas o datos personalizados
    context = {
        'total_posts': 100,  # Ejemplo de datos
        'total_users': 50,
    }
    return render(request, 'admin/custom_dashboard.html', context)

# Template content for 'admin/custom_dashboard.html'
"""
<h1>Dashboard Personalizado</h1>
<p>Total de publicaciones: {{ total_posts }}</p>
<p>Total de usuarios: {{ total_users }}</p>
"""

# URL patterns
urlpatterns = [
    path('admin/custom-dashboard/', custom_dashboard, name='custom_dashboard'),
    path('admin/', admin.site.urls),
]

def custom_dashboard_link(obj):
    url = reverse('custom_dashboard')
    return format_html('<a href="{}">Ir al Dashboard</a>', url)

custom_dashboard_link.short_description = "Dashboard Personalizado"
