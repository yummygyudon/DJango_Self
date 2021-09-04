import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


#페이지 작업 활용
@register.filter
def sub(value, arg) :
    return value - arg

@register.filter
def mark(value) : #value는 사용자의 웹페이지 입력값
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
