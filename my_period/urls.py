from django.urls import path

from . import views

app_name='my_period'
urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('', views.PeriodsView.as_view(), name='main'),
    path('form/', views.FormVeiw.as_view(), name='form'),
    path('<int:pk>/', views.PeriodsDetailView.as_view(), name='detail'),
    path('chat/', views.ChatAssistantView.as_view(), name='chat')
]