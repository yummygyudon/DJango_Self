from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import  timezone
from .forms import QuestionForm

def index(request) :
    """
    firstapp 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}
    return render(request, 'firstapp/question_list.html', context)

def detail(request, question_id) :
    """
    firstapp 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'firstapp/question_detail.html', context)

def answer_create(request, question_id) :
    """
    firstapp 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    #방법1_Answer모델을 통해 데이터 저장
    '''
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    '''
    #방법2
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    #등록 후 등록한 값을 포함하여 되돌아가기 (표시하는 코드는 HTML파일에서)
    return redirect('firstapp:detail', question_id=question_id)

def question_create(request) :
    """
    firstapp 질문 등록
    """
    # 입력데이터 저장 코드
    if request.method == 'POST' :
        form = QuestionForm(request.POST)
        if form.is_valid() :
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return  redirect('firstapp:index')
    else :
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'firstapp/question_form.html', context)
# Create your views here.
