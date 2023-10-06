from django.urls import path
from . import views

urlpatterns = [
    path('request_exams/', views.request_exams, name="request_exams"),
    path('close_order/', views.close_order, name="close_order"),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order')
]