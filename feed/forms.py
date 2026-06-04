from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escolha um usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Escolha uma senha'})
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Esse nome de usuário já está em uso.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data


class PostForm(forms.Form):
    texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'O que está acontecendo?',
            'rows': 3,
        })
    )
    imagem = forms.ImageField(required=False)
    video = forms.FileField(required=False)
