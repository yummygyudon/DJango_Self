from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question

def index(request) :
    """
    firstapp 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page','1') #페이지
    kw = request.GET.get('kw', '') #검색창
    sort = request.GET.get('sort', 'recent')

    #정렬
    if sort == 'recommend' :
        question_list = Question.objects.annotate(
            num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    elif sort == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else : #recent (최근순_초기값)
        question_list = Question.objects.order_by('-create_date')

    #조회
    #question_list = Question.objects.order_by('-create_date') [정렬]의 기준 중 하나로 변환
    if kw :
        question_list = question_list.filter(
            Q(subject__icontains=kw)|
            Q(content__icontains=kw)|
            Q(author__username__icontains=kw)|
            Q(answer__author__username__icontains=kw)
        ).distinct()

    #페이지 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보기 설정
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj, #paginator를 통해 페이지 번호와 보기 개수까지 받기
               'page' : page, 'kw' : kw,
               'sort' : sort}
    return render(request, 'firstapp/question_list.html', context)

def detail(request, question_id) :
    """
    firstapp 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'firstapp/question_detail.html', context)

