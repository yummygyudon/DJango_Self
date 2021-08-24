from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import  timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request) :
    """
    firstapp 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page','1') #페이지

    #조회
    question_list = Question.objects.order_by('-create_date')

    #페이지 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보기 설정
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj} #paginator를 통해 페이지 번호와 보기 개수까지 받기
    return render(request, 'firstapp/question_list.html', context)

def detail(request, question_id) :
    """
    firstapp 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'firstapp/question_detail.html', context)

@login_required(login_url='account:login')
def answer_create(request, question_id) :
    """
    firstapp 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST" :
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('firstapp:detail', question_id=question_id)
    else :
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'firstapp/question_detail.html', context)

    #방법1_Answer모델을 통해 데이터 저장
    '''
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    '''
    # #방법2
    # question.answer_set.create(content=request.POST.get('content'),
    #                            create_date=timezone.now())
    # #등록 후 등록한 값을 포함하여 되돌아가기 (표시하는 코드는 HTML파일에서)
    # return redirect('firstapp:detail', question_id=question_id)

@login_required(login_url='account:login')
def question_create(request) :
    """
    firstapp 질문 등록
    """
    # 입력데이터 저장 코드
    if request.method == 'POST' :
        form = QuestionForm(request.POST)
        if form.is_valid() :
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return  redirect('firstapp:index')
    else :
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'firstapp/question_form.html', context)
# Create your views here.
