from django import forms
from .models import Blog, Categoria

class BlogForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'text-white'}),
        required=False,
        label="Categorías"
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'categorias']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'text-gray-900 bg-white',  # Texto negro y fondo blanco
            }),
            'content': forms.Textarea(attrs={
                'class': 'text-gray-900 bg-white',
            }),
        }
