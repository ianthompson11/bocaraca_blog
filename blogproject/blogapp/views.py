# blogapp/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BlogForm  # Clase para blogForm

class BlogListView(LoginRequiredMixin, ListView): # Se realizo una modificacion para requeriar Login antes de ver el blog
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.save_m2m()  # necesario para guardar relaciones ManyToMany
        return response

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
