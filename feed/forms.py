from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Usuário', 'autocomplete': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'autocomplete': 'current-password'})
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escolha um usuário', 'autocomplete': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Escolha uma senha', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha', 'autocomplete': 'new-password'})
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
            'rows': 4,
        })
    )
    imagem = forms.ImageField(required=False)
    video = forms.FileField(required=False)


class ComentarioForm(forms.Form):
    texto = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escreva um comentário...', 'autocomplete': 'off'})
    )


class MensagemForm(forms.Form):
    texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Mensagem...', 'autocomplete': 'off'})
    )
