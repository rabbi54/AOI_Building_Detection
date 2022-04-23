from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.


class SegmentModel(models.Model):
    TYPE_UNET = 4
    TYPE_RESNET = 9

    TYPE_CHOICES = (
        (TYPE_UNET, 'Unet'),
        (TYPE_RESNET, 'Resnet'),
    )


    inputFile = models.FileField(upload_to='input/', null=False, validators=[FileExtensionValidator(['tif', 'tiff'])])
    outputFile = models.FileField(upload_to='output/', null=True)
    maskedFile = models.FileField(upload_to='masked/', null=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=TYPE_UNET)