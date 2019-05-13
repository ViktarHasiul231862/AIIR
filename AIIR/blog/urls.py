from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('params/', views.execute_algorithm, name="execute"),
    path('progress/', views.progress_bar, name="progress"),
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
    path('taskManager/', views.task_manager, name="task-manager"),
    path('task/', views.task, name="task"),
    path('generate_fractal/', views.generate_fractal, name="generate_fractal")
]