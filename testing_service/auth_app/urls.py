from django.urls import path

from auth_app import views

app_name = 'auth_app'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
]
