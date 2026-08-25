from django import forms
from django.contrib.auth.models import User

TAMANHO_MAXIMO = 5 * 1024 * 1024  # 5MB


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'autocomplete': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'autocomplete': 'current-password'})
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escolha um nome de usuário', 'autocomplete': 'username'})
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
            'rows': 3,
        })
    )
    imagem = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if imagem and imagem.size > TAMANHO_MAXIMO:
            raise forms.ValidationError('A imagem não pode ultrapassar 5MB.')
        return imagem

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and video.size > TAMANHO_MAXIMO:
            raise forms.ValidationError('O vídeo não pode ultrapassar 5MB.')
        return video

    def clean(self):
        cleaned_data = super().clean()
        texto = cleaned_data.get('texto')
        imagem = cleaned_data.get('imagem')
        video = cleaned_data.get('video')
        if not texto and not imagem and not video:
            raise forms.ValidationError('O post precisa ter pelo menos texto, imagem ou vídeo.')
        return cleaned_data


class StoryForm(forms.Form):
    imagem = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if imagem and imagem.size > TAMANHO_MAXIMO:
            raise forms.ValidationError('A imagem não pode ultrapassar 5MB.')
        return imagem

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and video.size > TAMANHO_MAXIMO:
            raise forms.ValidationError('O vídeo não pode ultrapassar 5MB.')
        return video

    def clean(self):
        cleaned_data = super().clean()
        imagem = cleaned_data.get('imagem')
        video = cleaned_data.get('video')
        if not imagem and not video:
            raise forms.ValidationError('Escolha uma imagem ou um vídeo para o seu story.')
        if imagem and video:
            raise forms.ValidationError('Escolha apenas uma imagem OU um vídeo, não os dois.')
        return cleaned_data


class ComentarioForm(forms.Form):
    texto = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Postar sua resposta...', 'autocomplete': 'off'})
    )


class MensagemForm(forms.Form):
    texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enviar uma mensagem direta...', 'autocomplete': 'off'})
    )

