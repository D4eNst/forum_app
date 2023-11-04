from django import forms
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from forum_app.models import Post, Category


class AddPostForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=TinyMCE(attrs={

    }, mce_attrs={

    }))

    class Meta:

        model = Post
        fields = ['title', 'slug', 'category', 'is_active', 'text']
        widgets = {'category': forms.Select(attrs={'class': 'selectpicker category-select',
                                                   'data-live-search': 'true',
                                                   'data-width': '200px',
                                                   })}

    # def __init__(self, *args, **kwargs):
    #     super(AddPostForm, self).__init__(*args, **kwargs)
    #     sorted_categories = Category.objects.order_by('name')
    #     category_choices = [(category.id, category.name) for category in sorted_categories]
    #     self.fields['category'].widget.choices = category_choices

    def clean_slug(self):
        # Получите значение 'title' из cleaned_data
        title = self.cleaned_data.get('title')
        slug = self.cleaned_data.get('slug')

        # Если title существует, создайте slug из него
        if title and not slug:
            # Используйте функцию slugify для генерации slug
            slug = slugify(title)

            # Убедитесь, что slug уникален, добавляя уникальный суффикс
            queryset = Post.objects.filter(slug__startswith=slug)
            count = 1
            while queryset.exists():
                slug = f"{slug}-{count}"
                queryset = Post.objects.filter(slug__startswith=slug)
                count += 1

            return slug

        # Если title не существует, верните slug
        return slug
