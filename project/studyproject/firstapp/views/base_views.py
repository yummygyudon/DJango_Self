from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question

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