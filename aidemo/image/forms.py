from tkinter.tix import Form
from django import forms
from .models import SegmentModel

class SegmentForm(forms.ModelForm):
    class Meta:
        model = SegmentModel
        fields = ['inputFile','type']
