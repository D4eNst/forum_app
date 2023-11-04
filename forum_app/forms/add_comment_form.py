from django import forms
from tinymce.widgets import TinyMCE

from forum_app.models import Comment


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={
        'cols': 50,
        'rows': 30,
    }, mce_attrs={
        "menubar": '',
        "plugins": '',
        'toolbar': '',
        'width': '70%',
        'height': '300px',
    }))

    class Meta:
        model = Comment
        fields = ['text']
