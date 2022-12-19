from django.urls import path
from task_manager.auth import views

app_name = 'auth'
urlpatterns = [
    path('login/',
         views.LoginView.as_view(),
         name='login'),
    path('logout/',
         views.LogoutView.as_view(),
         name='logout'),
]
