from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('params/', views.setParams, name="set-params"),
    path('reset/', views.reset, name="reset"),
    path('progress/', views.progress_bar, name="progress"),
    path('start1/', views.start_count1, name="start_count1"),
    path('start2/', views.start_count2, name="start_count2")

]