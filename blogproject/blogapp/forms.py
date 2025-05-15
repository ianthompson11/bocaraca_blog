from django import forms
from .models import Blog, Categoria

class BlogForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # O usa forms.SelectMultiple
        required=False,
        label="Categorías"
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'categorias']
