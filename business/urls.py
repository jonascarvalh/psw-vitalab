from django.urls import path
from . import views

urlpatterns = [
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("customer/<int:customer_id>", views.customer, name="customer"),
]