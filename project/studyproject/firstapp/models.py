from django.db import models

class Question(models.Model) :
    #질문의 제목
    subject = models.CharField(max_length=200)
    #질문의 내용
    content = models.TextField()
    #작성 일시
    create_date = models.DateTimeField()
    def __str__(self):
        return self.subject

class Answer(models.Model) :
    #특정 질문의 답변
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #답변의 내용
    content = models.TextField()
    #작성 일시
    create_date = models.DateTimeField()

# Create your models here.
