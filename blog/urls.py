
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('test-403/', views.test_403, name='test_403'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path(
        'register/',
        views.RegistrationView.as_view(),
        name='register'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # CRUD
    path(
        'posts/',
        views.post_list,
        name='post_list'
    ),

    path(
        'posts/create/',
        views.post_create,
        name='post_create'
    ),

    path(
        'posts/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),

    path(
        'posts/<slug:slug>/edit/',
        views.post_update,
        name='post_update'
    ),

    path(
        'posts/<slug:slug>/delete/',
        views.post_delete,
        name='post_delete'
    ),
]
path('test-403/', views.test_403, name='test_403'),
path('test-403/', views.test_403, name='test_403'),