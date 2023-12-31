from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from exams.models import ExamRequest
from .utils import generate_exam_pdf, generate_random_password
from django.contrib import messages
from django.contrib.messages import constants

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
            'customers': customers,
            'authenticated': request.user,
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
            'exams': exams,
            'authenticated': request.user,
        }
    )

@staff_member_required
def exam_customer(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)
    return render(
        request, 
        'exam_customer.html', 
        {
            'exam': exam,
            'authenticated': request.user,
        }
    )

def proxy_pdf(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)
    response = exam.result.open()

    return HttpResponse(response)

def gen_password(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)

    if exam.password:
        return FileResponse(generate_exam_pdf(
            exam.exam.name, 
            exam.user.first_name,
            exam.password
            ),
            filename="token.pdf"
        )
    
    exam.password = generate_random_password(9)
    exam.save()
    return FileResponse(generate_exam_pdf(
            exam.exam.name, 
            exam.user.first_name,
            exam.password
            ),
            filename="token.pdf"
        )

def change_exam_data(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)

    pdf           = request.FILES.get('result')
    status        = request.POST.get('status')
    pass_required = request.POST.get('pass_required')

    if pass_required and (not exam.password):
        messages.add_message(
            request,
            constants.ERROR,
            'To require the password, first create one!'
        )
        return redirect(f'/business/exam_customer/{exam_id}')
    exam.pass_required = True if pass_required else False
    if pdf:
        exam.result = pdf

    exam.status = status
    exam.save()

    messages.add_message(
            request,
            constants.SUCCESS,
            'Successfully data modified!'
        )
    return redirect(f'/business/exam_customer/{exam_id}')