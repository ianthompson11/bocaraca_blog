# blogapp/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment, Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import BlogForm


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_nombre = self.request.GET.get('categoria')
        if categoria_nombre:
            queryset = queryset.filter(categorias__nombre=categoria_nombre)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'





class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)  # ← AQUÍ guardamos el objeto blog sin M2M
        self.object.save()                     # ← guardamos el blog en la BD
        form.save_m2m()                        # ← ahora sí guardamos las categorías
        return redirect(self.get_success_url())  # ← redirigimos correctamente

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})




class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

#The last of us

def inicio(request):
    contexto = {
        "titulo": "The Last of Us: Supervivientes",
        "frase": "Cuando estás perdido en la oscuridad, busca la luz.",
        "personaje": "Ellie Williams",
        "imagen": "images/ellie.jpg",
    }
    return render(request, "index.html", contexto)
