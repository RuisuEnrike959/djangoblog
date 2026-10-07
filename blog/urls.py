from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # CRUD
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/edit/', views.post_update, name='post_update'),
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),
]
