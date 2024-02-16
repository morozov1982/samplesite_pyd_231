# from django.forms import ModelForm, modelform_factory, DecimalField
from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    title = forms.CharField(
        label='Название товара',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слошком короткое название товара!'}
    )

    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика', help_text='Не забудь выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный текст'},
    )

    def clean_title(self):
        # val = self.cleaned_data['title']
        val = self.cleaned_data.get('title')
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается!')
        return val

    def clean(self):
        super().clean()
        errors = {}

        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Укажите описание продаваемого товара')

        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')

        if errors:
            raise ValidationError(errors)

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


class RubricBaseFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) or ('Мебель' not in names):
            raise ValidationError(
                  'Добавьте рубрики недвижимости, транспорта и мебели')


class SearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=20,
        label='Искомое слово',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
    )
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')

    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный текст'},
        # generator='captcha.helpers.random_char_challenge',
        # generator='captcha.helpers.math_challenge',
        # generator='captcha.helpers.word_challenge',
    )

    error_css_class = 'form-control is-invalid'
    required_css_class = 'required'
