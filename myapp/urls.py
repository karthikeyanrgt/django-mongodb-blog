from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blog_list_create, name='blog-list-create'),
    path('blogs/<str:blog_id>/', views.blog_detail, name='blog-detail'),
]