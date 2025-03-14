from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup_view"),
    path('dashboard/', views.dashboard_view, name="dashboard_view"),
    path('delete/<str:pk>', views.delete_view, name='delete_view'),
    path('create/', views.create_view, name='create_view'),
    path('edit/<str:pk>', views.edit_view, name='edit_view'),
    path('transfer/', views.transfer_view, name='transfer_view'),
    path('deposit/', views.deposit_view, name='deposit_view'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal_view'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
]