from typing import Any

from forum_app.models import UserActivity, CustomUser, ActivityName, Post, Category


def create_activity(user, post: Post, action_type: str, action_name: str) -> None:
    activity = ActivityName.objects.filter(name=action_name)
    if not activity:
        activity = ActivityName.objects.create(name=action_name)
    else:
        activity = activity.first()
    UserActivity.objects.create(
        user=user,
        action_type=action_type,
        action_name=activity,
        post=post
    )


def filter_category(form, user) -> Any:
    is_admin = user.is_staff

    if not is_admin:
        not_empty_cat = Category.objects.filter(post__isnull=False, post__is_active=True)
        users_empty_cat = Category.objects.filter(post__isnull=True, user=user)
        users_draft_cat = Category.objects.filter(post__is_active=False, user=user)

        category_queryset = (not_empty_cat | users_empty_cat | users_draft_cat).distinct()
        form.fields['category'].queryset = category_queryset
    else:
        form.fields['category'].queryset = Category.objects.all()

    return form
