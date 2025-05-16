# blogapp/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment, Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import BlogForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.contrib import messages


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_slug = self.request.GET.get('categoria')
        if categoria_slug:
            queryset = queryset.filter(categorias__slug=categoria_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_list = self.get_queryset()
        paginator = Paginator(blog_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context['blogs'] = blogs
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


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        blog_id = self.kwargs['pk']
        if Review.objects.filter(reviewer=request.user, blog_id=blog_id).exists():
            messages.error(request, "Ya has creado una reseña para este blog.")
            return redirect('blogapp:blog_detail', pk=blog_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})


# The last of us

def inicio(request):
    contexto = {
        "titulo": "The Last of Us: Supervivientes",
        "frase": "Cuando estás perdido en la oscuridad, busca la luz.",
        "personaje": "Ellie Williams",
        "imagen": "images/ellie.jpg",
    }
    return render(request, "index.html", contexto)
