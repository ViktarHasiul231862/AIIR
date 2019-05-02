from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('execute/', views.execute_algorithm, name="execute"),
    path('reset/', views.reset, name="reset"),
    path('progress/', views.progress_bar, name="progress"),
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
    path('taskManager/', views.task_manager, name="task-manager"),
    path('task/', views.task, name="task")
]