import json
import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic import DetailView

from forum_app.forms import AddCommentForm
from forum_app.models import Post, Comment, UserActivity
from forum_app.views.main_views.utils import create_activity


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum_app/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        context['form'] = AddCommentForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_active and not self.request.user.is_superuser and self.request.user != obj.user:
            raise Http404

        if obj.is_active:
            obj.views_cnt += 1

        user = self.request.user
        if user.is_authenticated:
            if not obj.views.filter(pk=user.pk).exists():
                obj.views.add(user)

        obj.save()
        return obj

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.is_active and not self.request.user.is_superuser and self.request.user != obj.user:
            raise Http404

        if request.POST.get('confirm_post', 'false') == 'true':
            current_post = obj
            current_post.is_active = True
            current_post.save()

            create_activity(user=self.request.user,
                            post=current_post,
                            action_type="Пользователь написал новый пост",
                            action_name="new_post")

            # UserActivity.objects.create(
            #     user=current_post.user,
            #     action_type="Пользователь написал новый пост",
            #     action_name=ActivityName.objects.get(name="new_post"),
            #     post=current_post
            # )
            return self.get(request, *args, **kwargs)

        comment_dict = {
            'user': request.user,
            'post': Post.objects.get(slug=kwargs.get('slug')),
            'text': request.POST.get('text')
        }

        if self.request.POST.get('text'):
            comment = Comment(**comment_dict)
            comment.save()

            create_activity(user=self.request.user,
                            post=comment_dict.get('post'),
                            action_type="Пользователь прокомментировал пост",
                            action_name="comments")

            # UserActivity.objects.create(
            #     user=self.request.user,
            #     action_type="Пользователь прокомментировал пост",
            #     action_name=ActivityName.objects.get(name="comments"),
            #     post=comment_dict.get('post')
            # )
            current_url = request.get_full_path()
            current_url += f'#com-{comment.id}'

            response = HttpResponseRedirect(current_url)
            return response
        else:
            pass

        return self.get(request, *args, **kwargs)


def toggle_like(request, obj_type, obj_id):
    if request.method == 'POST':
        model = None

        if obj_type == 'comment':
            model = Comment
        elif obj_type == 'post':
            model = Post

        if model:
            try:
                obj = model.objects.get(id=obj_id)
                body = request.body.decode('utf-8')
                data = json.loads(body)
                liked = data.get('liked') == 'true'
                likes_count = int(re.sub(r"\D", "", data.get('likes_count')))

                if liked:
                    getattr(obj, 'likes').remove(request.user)
                    liked = False
                    likes_count -= 1
                    if model is Post:
                        old_act = UserActivity.objects.filter(
                            user=request.user,
                            action_name__name="likes",
                            post=Post.objects.get(id=obj_id)
                        )
                        if old_act:
                            old_act.first().delete()
                else:
                    getattr(obj, 'likes').add(request.user)
                    liked = True
                    likes_count += 1
                    if model is Post:
                        create_activity(user=request.user,
                                        post=Post.objects.get(id=obj_id),
                                        action_type="Пользователь поставил лайк на пост",
                                        action_name="likes")
                obj.save()

                response_data = {
                    'liked': liked,
                    'likes_count': likes_count,
                }

                return JsonResponse(response_data)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Object not found'}, status=404)

    # В случае GET-запроса верните HTTP 405 Method Not Allowed
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def toggle_comment_like(request, comment_id):
    return toggle_like(request, 'comment', comment_id)


def toggle_post_like(request, post_id):
    return toggle_like(request, 'post', post_id)
