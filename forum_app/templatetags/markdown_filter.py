from datetime import timedelta

from django import template
from django.utils import timezone
from markdown import markdown
from forum_app.models import Comment, CustomUser, Post

register = template.Library()


@register.filter
def safe_markdown(text: str):
    return markdown(text)


@register.filter
def check_comment_like(comment: Comment, user: CustomUser):
    # print(comment, user)
    # print(comment.likes.filter(pk=user.pk).exists())
    return comment.likes.filter(pk=user.pk).exists()


@register.filter
def check_post_like(post: Post, user: CustomUser):
    # print(comment, user)
    # print(comment.likes.filter(pk=user.pk).exists())
    return post.likes.filter(pk=user.pk).exists()


@register.filter
def time_dif(created_at):
    return timezone.now() - created_at < timedelta(days=1)
