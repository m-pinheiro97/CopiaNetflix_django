from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


class CriarContaForm(UserCreationForm):
    email = forms.EmailField()  # padrão obrigatório, (required=False) para alterar

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)

    email.widget.attrs['class'] = 'form-control'

    # outras soluções para adiconar as classes bootstrap ao formulario

    # 1
    # email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # 2
    # def __init__(self, *args, **kwargs):
    #     super(FormHomepage, self).__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['class'] = 'form-control'
