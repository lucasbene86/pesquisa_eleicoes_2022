from django import forms

class CadastroForms(forms.Form):
    cpf = forms.CharField(label='cpf', max_length=30)