from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('signup', views.signup_view, name="signup_view"),
    path('dashboard/', views.dashboard_view, name="dashboard_view"),
    path('read/<str:pk>', views.read_view, name='read_view')
]