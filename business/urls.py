from django.urls import path
from . import views

urlpatterns = [
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("customer/<int:customer_id>", views.customer, name="customer"),
    path("exam_customer/<int:exam_id>", views.exam_customer, name="exam_customer"),
    path("proxy_pdf/<int:exam_id>", views.proxy_pdf, name="proxy_pdf"),
    path("gen_password/<int:exam_id>", views.gen_password, name="gen_password"),
    path("change_exam_data/<int:exam_id>", views.change_exam_data, name="change_exam_data")
]