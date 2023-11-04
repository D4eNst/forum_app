from django import forms
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from forum_app.models import Category


# class AddCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'slug', ]
#
#     def clean_slug(self):
#         # Получите значение 'title' из cleaned_data
#         name = self.cleaned_data.get('name')
#         slug = self.cleaned_data.get('slug')
#
#         # Если title существует, создайте slug из него
#         if name and not slug:
#             # Используйте функцию slugify для генерации slug
#             slug = slugify(name)
#
#             # Убедитесь, что slug уникален, добавляя уникальный суффикс
#             queryset = Category.objects.filter(slug__startswith=slug)
#             count = 1
#             while queryset.exists():
#                 slug = f"{slug}-{count}"
#                 queryset = Category.objects.filter(slug__startswith=slug)
#                 count += 1
#
#             return slug
#
#         # Если name не существует, верните slug
#         return slug
