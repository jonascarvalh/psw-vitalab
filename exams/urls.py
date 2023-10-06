from django.urls import path
from . import views

urlpatterns = [
    path('request_exams/', views.request_exams, name="request_exams"),
    path('close_order/', views.close_order, name="close_order")
]