from django import forms
from firstapp.models import Question

class QuestionForm(forms.ModelForm) :
    class Meta :
        model = Question
        feilds = ['subject', 'content']