from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


from ..models import Question, Answer

@login_required(login_url='account:login')
def vote_question(request, question_id) :
    """
    앱 질문 추천 기능
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author :
        messages.error(request, '본인의 질문은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('firstapp:detail', question_id=question.id)

@login_required(login_url='account:login')
def vote_answer(request, answer_id) :
    """
    앱 답변 추천 기능
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author :
        messages.error(request, '본인의 답변은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('firstapp:detail', question_id=answer.question.id)