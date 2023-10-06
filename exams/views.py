from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ExamsTypes, ExamsOrders, ExamRequest
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
@login_required
def request_exams(request):
    exams_types = ExamsTypes.objects.all()
    if request.method == "GET":
        return render(
            request, 
            'request_exams.html',
            context = {'exams_types': exams_types}
        )
    elif request.method == "POST":
        exams_id = request.POST.getlist('exams')
        request_exams_objects = ExamsTypes.objects.filter(
            id__in=exams_id
        )

        # TODO: verificar preço dos dados disponíveis
        price_total = 0
        for i in request_exams_objects:
            if i.available:
                price_total += i.price
        
        return render(
            request, 
            'request_exams.html',
            {
                'exams_types': exams_types,
                'request_exams_objects': request_exams_objects,
                'price_total': price_total,
                'date_now': datetime.now()
            }, 
        )

@login_required
def close_order(request):
    exams_id = request.POST.getlist('exams')
    exam_request = ExamsTypes.objects.filter(id__in=exams_id)


    order_exam = ExamsOrders(
        user = request.user,
        date = datetime.now()
    )

    order_exam.save()

    for exam in exam_request:
        request_exams_temp = ExamRequest(
            user=request.user,
            exam=exam,
            status="E",
        )
        request_exams_temp.save()
        order_exam.exams.add(request_exams_temp)

    order_exam.save()
    messages.add_message(request_exams_temp, constants.SUCCESS, 'Exams Order sucessfully done!')
    return redirect('/exams/show_orders/')

@login_required
def manage_orders(request):
    orders_exams = ExamsOrders.objects.filter(
        user=request.user
    )
    return render(
        request, 
        'manage_orders.html',
        {
            'orders_exams': orders_exams,
        },
    )

@login_required
def cancel_order(request, order_id):
    order = ExamsOrders.objects.get(id=order_id)
    if not order.user == request.user:
        messages.add_message(
            request,
            constants.ERROR,
            'This order is not your.'
        )
        return redirect('/exams/manage_orders/')
    
    order.scheduled = False
    order.save()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Order cancelled sucessfully.'
    )
    return redirect('/exams/manage_orders/')

@login_required
def manage_exams(request):
    exams = ExamRequest.objects.filter(user=request.user)
    return render(
        request, 
        'manage_exams.html',
        {
            'exams': exams,
        },
    )

@login_required
def allow_open_exam(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)

    if not exam.pass_required:
        if exam_have_result(exam):
            return redirect(exam.result.url)
        else:
            messages.add_message(
                request,
                constants.ERROR,
                "This result doesn't exists."
            )
            return redirect('/exams/manage_exams/')
        
    return redirect(f'/exams/request_password_exam/{exam_id}')

@login_required
def request_password_exam(request, exam_id):
    exam = ExamRequest.objects.get(id=exam_id)

    if request.method == "GET":
        return render(
            request, 
            "request_password_exam.html",
            {
                'exam': exam
            }
        )
    elif request.method == "POST":
        password = request.POST.get('password')

        if password == exam.password:
            if exam_have_result(exam):
                return redirect(exam.result.url)
            else:
                messages.add_message(
                request,
                constants.ERROR,
                "This result doesn't exists."
            )
            return redirect(f'/exams/request_password_exam/{exam.id}')
        else:
            messages.add_message(
                request,
                constants.ERROR,
                'Invalid Password!'
            )
            return redirect(f'/exams/request_password_exam/{exam.id}')

def exam_have_result(exam):
    try:
        redirect(exam.result.url)
        return True
    except:
        return False