from django.urls import path
from . import views

urlpatterns = [
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("customer/<int:customer_id>", views.customer, name="customer"),
    path("exam_customer/<int:exam_id>", views.exam_customer, name="exam_customer"),
    path("proxy_pdf/<int:exam_id>", views.proxy_pdf, name="proxy_pdf")
]