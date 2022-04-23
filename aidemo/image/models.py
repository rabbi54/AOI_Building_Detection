from django.db import models

# Create your models here.


class SegmentModel(models.Model):
    inputFile = models.FileField(upload_to='input/', null=False)
    outputFile = models.FileField(upload_to='output/', null=True)