from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


