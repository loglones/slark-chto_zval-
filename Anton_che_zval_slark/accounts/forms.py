from enum import unique

from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from .models import Aplication

class Reg_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Введите пороль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Повторите пороль')
    confirm = forms.BooleanField(required=True, label='Согласие на обработку пресоональных данных')
    email = forms.EmailField(widget=forms.EmailInput(), label='Введите почту')

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'confirm_password', 'confirm', 'gender']

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

STATUS_CHOISE = [
    ('new', 'Новая'),
    ('haired', 'Принято в работу'),
    ('done', 'Выполнено'),
    ('all', 'Все заявки')
]
# class AddAplForm(forms.ModelForm):
#     class Meta:
#         model = Aplication
#         fields = ('name', 'description', 'Category', 'photo_file')
#         enctype = "multipart/form-data"

class AddAplForm(forms.ModelForm):
    class Meta:
        model = Aplication
        fields = ['name', 'description', 'Category', 'photo_file', 'photo_file2', 'photo_file3']
        enctype = "multipart/form-data"




class CategoryList(forms.ModelForm):
    name = forms.CharField(max_length=250, label='Новая категория',  required=True)

    class Meta:
        model = Category
        fields = ['name']

class AppListFormFilter(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOISE, label='Отсортировать по статусу ', initial='All')

class AppListHandleForm(forms.ModelForm):
    name = forms.CharField(disabled=True, label='Имя заявки')
    description = forms.CharField(disabled=True, label='Описание')
    photo_file = forms.ImageField(disabled=True, label='Фото заявки')
    status = forms.ChoiceField(choices=[('done', 'Выполнено'), ('haired', 'Принято в работу')],
                               label='Изменить статус на ')
    Category = forms.ModelChoiceField(queryset=Category.objects.all(), disabled=True, label='Категория')
    comment = forms.CharField(disabled=False, label='Комментарий', required=False)
    photo_fileReady = forms.ImageField(disabled=False, label='Фото готовой заявки', required=False)
    photo_fileReady2 = forms.ImageField(disabled=False, label='Фото готовой заявки2', required=False)
    photo_fileReady3 = forms.ImageField(disabled=False, label='Фото готовой заявки3', required=False)


    def clean(self):
        status = self.cleaned_data.get('status')
        comment = self.cleaned_data.get('comment')
        photo_fileReady = self.cleaned_data.get('photo_fileReady')
        if self.instance.status != 'new':
            raise forms.ValidationError({'status': 'Статус можно сменить только у новой заявки'})
        if status == 'new' and comment:
            raise forms.ValidationError({'comment': 'К новой заявке нельзя добавить комментарий'})

        if status == 'haired' and not comment:
                self.add_error('comment', 'Нужно указать комментарий для заявки, принятой в работу')
        elif status == 'done' and not photo_fileReady:
                self.add_error('photo_fileReady', 'Нужно добавить фотографию для выполненной заявки')

    class Meta:
        model = Aplication
        fields = ['name', 'description', 'photo_file', 'status', 'Category', 'photo_fileReady','photo_fileReady2','photo_fileReady3', 'comment']
        enctype = "multipart/form-data"
