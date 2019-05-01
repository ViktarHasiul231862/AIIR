from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('params/', views.setParams, name="set-params"),
    path('reset/', views.reset, name="reset"),
    path('progress/', views.progress_bar, name="progress"),
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
]