from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe

# Create your models here.
class ExamsTypes(models.Model):
    choices_type = (
        ('I', 'Image Test'),
        ('S', 'Blood Test')
    )
    name = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=1, choices=choices_type)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()

    def __str__(self):
        return self.name

class ExamRequest(models.Model):
    choice_status = (
        ('E', 'Under Analysis'),
        ('F', 'Finished')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(ExamsTypes, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    result = models.FileField(upload_to="results", null=True, blank=True)
    pass_required = models.BooleanField(default=False)
    password = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.user} | {self.exam.name}'

    def badge_template(self):
        if self.status == 'E':
            classes = 'bg-warning text-dark'
            text = 'In Analysis'
        elif self.status == 'F':
            classes = 'bg-success'
            text = 'Finished'
        return mark_safe(f'<span class="badge {classes}">{text}</span>')
        
class ExamsOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exams = models.ManyToManyField(ExamRequest)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} | {self.date}'

class AcessoMedico(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identification = models.CharField(max_length=50)
    access_time = models.IntegerField() # Em horas
    created_at = models.DateTimeField()
    date_start_exams = models.DateField()
    date_final_exams = models.DateField()
    token = models.CharField(max_length=20, null=True, black=True)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)