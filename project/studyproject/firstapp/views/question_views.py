from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

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