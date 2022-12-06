from django.urls import path

from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.TestingListView.as_view(), name='list_test'),
    path('<int:pk>/', views.TestingDetailView.as_view(), name='detail_test'),
    path('result/<int:pk>/', views.ResultDetailView.as_view(), name='result'),
    path('results/', views.ResultListView.as_view(), name='result_list'),
]
