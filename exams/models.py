from django.db import models
from django.contrib.auth.models import User

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

class ExamsOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exams = models.ManyToManyField(ExamRequest)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} | {self.date}'