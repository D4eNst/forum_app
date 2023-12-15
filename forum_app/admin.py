from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Category, Post, Comment, UserActivity, ActivityName


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('category', 'is_active', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityName)
class UserActivityAdmin(admin.ModelAdmin):
    pass

