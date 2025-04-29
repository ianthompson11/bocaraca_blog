from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})



class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        reviewer = self.request.user
        # Verificar si el usuario ya ha creado una review para este blog
        existing_review = Review.objects.filter(blog=blog, reviewer=reviewer).exists()
        if existing_review:
            messages.error(self.request, "You have already reviewed this blog.")
            return self.form_invalid(form)
        form.instance.blog = blog
        form.instance.reviewer = reviewer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


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
