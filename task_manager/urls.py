from django.contrib import admin
from django.urls import path, include

from task_manager import views

urlpatterns = [
    path('', views.home.HomeView.as_view(), name='home'),
    path('login/',
         views.auth.LoginView.as_view(),
         name='login'),
    path('logout/',
         views.auth.LogoutView.as_view(),
         name='logout'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]
