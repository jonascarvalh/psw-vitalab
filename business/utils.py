import string, os
from random import choice, shuffle
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO

def generate_random_password(size):
    special_chars = string.punctuation
    chars = string.ascii_letters
    numbers_list = string.digits

    rest = 0
    qty = size // 3
    if not size % 3 == 0:
        rest = size - (qty*3)
    
    letters = ''
    for i in range(0, qty+rest):
        letters += choice(chars)

    numbers = ''
    for i in range(0, qty):
        numbers += choice(numbers_list)

    specials = ''
    for i in range(0, rest):
        letters += choice(special_chars)
    
    password = list(letters + numbers + specials)
    shuffle(password)

    return ''.join(password)

def generate_exam_pdf(exam, patient, password):
    path_template = os.path.join(
        settings.BASE_DIR,'templates','partials','password_exam.html'
    )

    template_render = render_to_string(
        path_template,
        {
            'exam': exam,
            'patient': patient,
            'password': password
        }
    )

    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)

    return path_output