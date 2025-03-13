from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup_view"),
    path('dashboard/', views.dashboard_view, name="dashboard_view"),
    path('delete/<str:pk>', views.delete_view, name='delete_view'),
    path('create/', views.create_view, name='create_view'),
    path('read/<str:pk>', views.read_view, name='read_view'),
    path('edit/<str:pk>', views.edit_view, name='edit_view'),
    path('transfer/', views.transfer_view, name='transfer_view'),
]