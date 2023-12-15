from typing import Any

from forum_app.models import UserActivity, ActivityName, Post, Category


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


def filter_category(user) -> Any:
    is_admin = user.is_staff

    if is_admin:
        return Category.objects.all()

    not_empty_cat = Category.objects.filter(post__isnull=False, post__is_active=True)
    if not user.is_authenticated:
        return not_empty_cat.distinct()
    users_empty_cat = Category.objects.filter(post__isnull=True, user=user)
    users_draft_cat = Category.objects.filter(post__is_active=False, user=user)

    category_queryset = (not_empty_cat | users_empty_cat | users_draft_cat).distinct()
    return category_queryset


def filter_category_form(form, user) -> Any:

    form.fields['category'].queryset = filter_category(user)

    return form

