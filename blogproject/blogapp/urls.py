from django.urls import path
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView
#optimizacionORM - nplusone - Importacion libreria para correccion de error
from blogapp import views 
#optimizacionORM - nplusone  
app_name = 'blogapp'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    #optimizacionORM - nplusone - URL para vista de prueba de nplusone
    path('prueba/', views.vista_prueba_nplusone, name='vista_prueba_nplusone'), 
    #optimizacionORM - nplusone
]