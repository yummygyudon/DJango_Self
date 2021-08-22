from django import forms
from firstapp.models import Question, Answer

class QuestionForm(forms.ModelForm) :
    class Meta :
        model = Question
        fields = ['subject', 'content']
        #widget 삭제
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }

class AnswerForm(forms.ModelForm) :
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content':'답변내용',
        }
