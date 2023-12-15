from django import forms

from forum_app.forms import CustomUserChangeForm
from forum_app.models import CustomUser


class SettingsForm(CustomUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Электронная почта"
        self.fields["username"].label = "Логин"

    password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label="Подтвердите пароль",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': None}),
        }

    def clean_password(self):
        # Игнорировать изменения в поле пароля
        return self.initial.get('password')
