from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Blog, Review, Comment, Categoria

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

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm

# Registro de modelos en el admin
admin.site.register(Blog, BlogAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Categoria)
