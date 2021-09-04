from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


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
            return redirect('{}#answer_{}'.format(
                resolve_url('firstapp:detail', question_id=question.id),answer.id))
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
            return redirect('{}#answer_{}'.format(
                resolve_url('firstapp:detail', question_id=answer.question.id), answer.id))
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