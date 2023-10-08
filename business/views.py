from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from exams.models import ExamRequest

# Create your views here.
@staff_member_required
def manage_customers(request):
    customers = User.objects.filter(is_staff=False)

    complete_name = request.GET.get('name')
    email = request.GET.get('email')

    if email:
        customers = customers.filter(email__contains = email)
    if complete_name:
        customers = customers.annotate(full_name=Concat('first_name', Value(' '),'last_name')) \
                    .filter(full_name__contains=complete_name)
    return render(
        request, 
        'manage_customers.html',
        {
            'customers': customers
        }
    )

@staff_member_required
def customer(request, customer_id):
    customer = User.objects.get(id=customer_id)
    exams = ExamRequest.objects.filter(user=customer)
    return render(
        request, 
        'customer.html', 
        {
            'customer': customer,
            'exams': exams
        }
    )