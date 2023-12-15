from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from forum_app.forms import AddCommentForm
from forum_app.models import Comment


class UpdateComment(UpdateView, UserPassesTestMixin):
    model = Comment
    form_class = AddCommentForm
    template_name = 'forum_app/update_comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return f"{reverse('post_detail', args=[self.object.post.slug])}#com-{self.object.id}"

    def test_func(self):
        user = self.request.user
        comment = self.get_object()

        return user == comment.user or user.is_superuser


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_superuser or comment.user == request.user:
        comment.delete()

    return redirect('post_detail', slug=comment.post.slug)

