from django.db import models

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