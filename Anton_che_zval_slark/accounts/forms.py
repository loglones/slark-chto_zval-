from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re


class Reg_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Введите пороль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Повторите пороль')
    confirm = forms.BooleanField(required=True, label='Согласие на обработку пресоональных данных')
    email = forms.EmailField(widget=forms.EmailInput(), label='Введите почту')

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'confirm_password', 'confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают.')
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[А-яёЁ\s-]+$', name):
            raise ValidationError('Имя должно состоять из кириллических букв, пробелов и дефисов.')
        return name




    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-z-]+$', username):
            raise ValidationError('Логин должен состоять из латинских букв и дефисов.')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким логином уже существует.')
        return username

