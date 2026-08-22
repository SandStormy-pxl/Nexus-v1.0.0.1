from django import forms


TAMANHO_MAXIMO = 5 * 1024 * 1024  # 5MB


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
