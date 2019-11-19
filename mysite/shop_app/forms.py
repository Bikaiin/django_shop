# .*. coding: utf-8 .*.
from django import  forms
from  django.utils import  timezone
from  django.contrib.auth.models import User


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'special', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'exampleDropdownFormPassword1', 'placeholder': 'Пароль'}))
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Данный логин не зарегистрирован')
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')





class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
            'password',
            'password_check'

        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = ''
        self.fields['password'].label = 'Пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['email'].label = 'Почта'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['first_name'].help_text = 'Как к вам обращаться?'
        self.fields['email'].help_text = 'Оставляйте действующую почту!'


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if password != password_check:
            raise forms.ValidationError('пароли не совпадают')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Данный логин занят')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная почта занята')


class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовывоз"),("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields['phone'].help_text = 'Пожалуйста укажите номер по которому мы можем с вами связвться'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Адресс доствки'
        self.fields['address'].help_text = 'Обязательно укажите свой город'
        self.fields['comments'].label = 'Коментарии'
        self.fields['date'].label = 'Дата достваки'
        self.fields['date'].help_text = 'Дата доставки не может быть раньше чем на следующий день после заказа'

