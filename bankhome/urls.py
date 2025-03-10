from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('read/<str:pk>', views.read, name='read')
]