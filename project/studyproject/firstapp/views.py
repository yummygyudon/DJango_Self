from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer, Comment
from django.utils import  timezone
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


@login_required(login_url='account:login')
def question_modify(request, question_id) :
    """
    앱 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('firstapp:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now() #수정 일시 저장
            question.save()
            return redirect('firstapp:detail', question_id = question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'firstapp/question_form.html', context)


@login_required(login_url='account:login')
def question_delete(request, question_id) :
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한 없음')
        return redirect('firstapp:detail', question_id=question_id)
    question.delete()
    return redirect('firstapp:index')


@login_required(login_url='account:login')
def answer_modify(request, answer_id) :
    """
    앱 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('firstapp:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now() #수정 일시 저장
            answer.save()
            return redirect('firstapp:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer,'form': form}
    return render(request, 'firstapp/answer_form.html', context)

@login_required(login_url='account:login')
def answer_delete(request, answer_id) :
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한 없음')
    else :
        answer.delete()
    return redirect('firstapp:detail', question_id=answer.question.id)




@login_required(login_url='account:login')
def comment_create_question(request, question_id):
    """
    앱 질문(Question) 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.create_date=timezone.now()
            comment.question = question
            comment.save()
            return redirect('firstapp:detail', question_id=question.id)
    else :
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'firstapp/comment_form.html', context)

@login_required(login_url='account:login')
def comment_modify_question(request, comment_id) :
    """
    앱 질문(Question) 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('firstapp:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now() #수정 일시 저장
            comment.save()
            return redirect('firstapp:detail', question_id = comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'firstapp/comment_form.html', context)


@login_required(login_url='account:login')
def comment_delete_question(request, comment_id) :
    """
    앱 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한 없음')
        return redirect('firstapp:detail', question_id=comment.question_id)
    else :
        comment.delete()
    return redirect('firstapp:detail', question_id=comment.question_id)


@login_required(login_url='account:login')
def comment_create_answer(request, answer_id):
    """
    앱 답변(Answer) 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.create_date=timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('firstapp:detail', question_id=comment.answer.question.id)
            # comment 모델의 answer모델 내에도 question이 상속되어 있기 때문에
    else :
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'firstapp/comment_form.html', context)

@login_required(login_url='account:login')
def comment_modify_answer(request, comment_id) :
    """
    앱 답변(Answer) 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('firstapp:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now() #수정 일시 저장
            comment.save()
            return redirect('firstapp:detail', question_id = comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'firstapp/comment_form.html', context)


@login_required(login_url='account:login')
def comment_delete_answer(request, comment_id) :
    """
    앱 답변(Answer) 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한 없음')
        return redirect('firstapp:detail', question_id=comment.answer.question.id)
    else :
        comment.delete()
    return redirect('firstapp:detail', question_id=comment.answer.question.id)
# Create your views here.
