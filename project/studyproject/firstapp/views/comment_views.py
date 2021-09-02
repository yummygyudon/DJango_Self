from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment


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