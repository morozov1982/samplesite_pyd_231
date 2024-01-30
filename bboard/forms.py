# from django.forms import ModelForm, modelform_factory, DecimalField
from django import forms
from django.contrib.auth.models import User

# from django.forms.widgets import Select

from .models import Bb, Rubric


#  Фабрика классов
# BbForm = modelform_factory(
#     Bb,
#     fields=('title', 'content', 'price', 'rubric'),
#     labels={'title': 'Название товара'},
#     help_texts={'rubric': 'Не забудь выбрать рубрику!'},
#     field_classes={'price': DecimalField},
#     widgets={'rubric': Select(attrs={'size': 8})},
# )


#  Быстрое объявление
# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'},
#         help_texts = {'rubric': 'Не забудь выбрать рубрику!'},
#         field_classes = {'price': DecimalField},
#         widgets = {'rubric': Select(attrs={'size': 8})},


#  Полное объявление
# class BbForm(forms.ModelForm):
#     title = forms.CharField(label='Название товара')
#     content = forms.CharField(label='Описание',
#                               widget=forms.widgets.Textarea())
#     price = forms.DecimalField(label='Цена', decimal_places=2)
#     rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
#                                     label='Рубрика', help_text='Не забудь выбрать рубрику!',
#                                     widget=forms.widgets.Select(attrs={'size': 8}))
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


class BbForm(forms.ModelForm):
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика', help_text='Не забудь выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))
    # published = forms.DateField(
    #     widget=forms.widgets.SelectDateWidget(
    #         empty_label=('Выберите год', 'Выберите месяц', 'Выберите число')
    #     )
    # )

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль',
                                widget=forms.widgets.PasswordInput())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.widgets.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2',
                  'first_name', 'last_name')
