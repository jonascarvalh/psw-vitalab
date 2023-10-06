from django.urls import path
from . import views

urlpatterns = [
    path('request_exams/', views.request_exams, name="request_exams"),
    path('close_order/', views.close_order, name="close_order"),
    path('manage_orders/', views.manage_orders, name="manage_orders"),
    path('cancel_order/<int:order_id>', views.cancel_order, name="cancel_order"),
    path('manage_exams/', views.manage_exams, name="manage_exams"),
    path('allow_open_exam/<int:exam_id>', views.allow_open_exam, name='allow_open_exam'),
    path('request_password_exam/<int:exam_id>', views.request_password_exam, name='request_password_exam'),
]