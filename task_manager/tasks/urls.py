from django.urls import path
from task_manager.tasks import views

app_name = 'tasks'
urlpatterns = [
    path('',
         views.TaskListView.as_view(),
         name='list'),
    path('<int:pk>/',
         views.TaskCardView.as_view(),
         name='card'),
    path('create/',
         views.TaskCreateView.as_view(),
         name='create'),
    path('<int:pk>/update/',
         views.TaskUpdateView.as_view(),
         name='update'),
    path('<int:pk>/delete/',
         views.TaskDeleteView.as_view(),
         name='delete'),
]
