from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama & Profil
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),

    # Manajemen Berita (Post)
    path('berita/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Fitur Interaksi
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('logout/', views.custom_logout, name='logout'),
]