from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import get_user_model

user = get_user_model()

from .models import Comment, CustomUser, Rating


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Введите логин'})))
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Введите имя'})))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "auth-input", 'placeholder': 'Введите email'}))
    #image = forms.ImageField(label="Аватар", widget=forms.FileInput(attrs=({"class": "auth-input", 'placeholder': 'Выберите фотографию'})))
    password1 = forms.CharField(label="Пароль",widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Введите пароль'})))
    password2=forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Подтвердите пароль'})))

    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ('username', 'name', 'gender', 'email',)

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Введите логин'})))
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Введите имя'})))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "auth-input", 'placeholder': 'Введите email'}))
    #image = forms.ImageField(label="Аватар", widget=forms.FileInput(attrs=({"class": "auth-input", 'placeholder': 'Выберите фотографию'})))
    #password1 = forms.CharField(label="Пароль",widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Введите пароль'})))
    #password2=forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Подтвердите пароль'})))

    class Meta:
        model = CustomUser
        #fields = '__all__'
        fields = ('username', 'name', 'surname', 'gender', 'phone', 'email', 'region', 'city', 'address',)


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=20, widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Enter Your userName'})))
    password = forms.CharField(label="Пароль", max_length=20,  widget=forms.PasswordInput(attrs=({"class": "auth-input"})))

    def clean(self, *args, **kwargs):

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('User does not exist')
            
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Введите имя'})))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "auth-input", 'placeholder': 'Введите email'}))
    password1 = forms.CharField(label="Пароль",widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Введите пароль'})))
    password2=forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs=({"class": "auth-input", 'placeholder': 'Подтвердите пароль'})))
    
    class Meta:
        model = CustomUser
        fields = ('username',  'email', 'password1', 'password2', )

    def clean(self, *args, **kwargs):
        email=self.cleaned_data.get('email')
        email_qs = user.objects.filter(email=email)

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if email_qs.exists():
            raise forms.ValidationError('email is already in use')
        
        if password1 != password2:
            raise forms.ValidationError("password and confirm_password does not match")
        
        return super(RegisterForm, self).clean(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['text'].widget = Textarea(attrs={'row':3})  
    

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']