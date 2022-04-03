from .models import Marker
from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select, ClearableFileInput
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=14, widget=forms.TextInput(attrs={'class': 'authorization__form-input'}))
    password = forms.CharField(label='Пароль', max_length=128, widget=forms.PasswordInput(attrs={'class': 'authorization__form-input'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=14, widget=forms.TextInput(attrs={'class': 'authorization__form-input'}))
    password1 = forms.CharField(label='Пароль', max_length=128, widget=forms.PasswordInput(attrs={'class': 'authorization__form-input'}))
    password2 = forms.CharField(label='Повтор пароля', max_length=128, widget=forms.PasswordInput(attrs={'class': 'authorization__form-input'}))
    email = forms.EmailField(label='Email', max_length=320, widget=forms.EmailInput(attrs={'class': 'authorization__form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class MarkerForm(ModelForm):
    class Meta:
        model = Marker
        fields = ['search', 'animal', 'name', 'telephone', 'street', 'city', 'region', 'country', 'comment', 'photo']

        widgets = {
            'search': Select(attrs={
                'class': 'form-select',
                'id': 'search'
            }),
            'animal': Select(attrs={
                'class': 'form-select',
                'id': 'animal'
            }),
            'name': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Иван',
                'id': 'name'
            }),
            'telephone': TextInput(attrs={
                'class': 'form-input',
                'placeholder': '8 XXX XXX-XX-XX',
                'id': 'telephone'
            }),
            'street': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Улица, дом / Место',
                'id': 'street'
            }),
            'city': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Москва',
                'id': 'city'
            }),
            'region': Select(attrs={
                'class': 'form-select',
                'id': 'region'
            }),
            'country': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Россия',
                'id': 'country'
            }),
            'comment': Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Дополнительная информация',
                'id': 'comment'
            }),
            'photo': ClearableFileInput(attrs={
                'class': 'file_input',
                'accept': "image/png, image/jpeg",
                'id': 'photo'
            }),
        }

    def clean_city(self):
        city = self.cleaned_data['city']
        if re.match(r'\d', city):
            raise ValidationError('Ошибка в поле')
        elif not re.match(r'^(\w{2,})', city):
            raise ValidationError('Ошибка в поле')
        return city

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if not re.match(r'^((\+7|7|8)+([0-9]){10})$', telephone):
            raise ValidationError('Ошибка в поле')
        return telephone

    def clean_country(self):
        country = self.cleaned_data['country']
        if not re.match(r'^[а-яА-ЯёЁa-zA-Z]+$', country):
            raise ValidationError('Ошибка в поле')
        return country