from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField #esta la agregé
from django.utils.text import slugify

# modelo categoria
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True) # activado

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            while Categoria.objects.filter(slug=slug).exclude(id=self.id).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre



from django.db.models import Avg
# MODELOS

class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, blank=True, related_name='blogs')  # nueva línea
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
#se calcula el promedio de las puntuaciones de reviews del blog
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return 0
#se cuentan las reviews del blog
    @property
    def review_count(self):
        return self.reviews.count()

class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = RichTextUploadingField()  #comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()  #content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username}"