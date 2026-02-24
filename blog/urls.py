from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),

    # Blog
    path('', views.home, name='home'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),

    # IMPORTANT: post/create/ must come BEFORE post/<slug:slug>/
    path('post/create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    #robots.txt 
    path('robots.txt',views.robots_txt,name="robots_txt"),

    
    

   
]