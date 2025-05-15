from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Blog, Review, Comment, Categoria

# -------- Personalización de formularios con CKEditor --------
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

# -------- Admin personalizado para Blog --------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'author', 'created_at', 'get_categorias')
    list_filter = ('created_at', 'categorias')
    search_fields = ('title', 'author__username')
    filter_horizontal = ('categorias',)
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'categorias', 'content'),
            'classes': ('wide', 'collapse', 'animate-fade-in'),
        }),
    )

    def get_categorias(self, obj):
        return ", ".join([c.nombre for c in obj.categorias.all()])
    get_categorias.short_description = 'Categorías'
# -------- Admin personalizado para Review --------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('reviewer', 'blog', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer__username', 'blog__title')

# -------- Admin personalizado para Comment --------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ('commenter', 'review', 'created_at')
    search_fields = ('commenter__username', 'review__blog__title')

# -------- Admin para Categoría --------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# -------- Personalización global del panel admin --------
admin.site.site_header = "Panel de Supervivencia - The Last of Us 🧟‍♀️"
admin.site.site_title = "Administración del Refugio"
admin.site.index_title = "Control de Contenido y Reseñas"

