from django import forms
from django.contrib.auth import authenticate, get_user_model

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Enter Your userName'})))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs=({"class": "auth-input"})))

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


user = get_user_model()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs=({"class": "auth-input", 'placeholder': 'Enter Your userName'})))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={"class": "auth-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs=({"class": "auth-input"})))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs=({"class": "auth-input"})))
    

    class Meta:
        model=user
        fields=[
            'username',
            'email',
            'password',
            'confirm_password',
        ]

    

    def clean(self, *args, **kwargs):
        email=self.cleaned_data.get('email')
        email_qs = user.objects.filter(email=email)

        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if email_qs.exists():
            raise forms.ValidationError('email is already in use')
        
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        
        return super(UserRegisterForm, self).clean(*args, **kwargs)