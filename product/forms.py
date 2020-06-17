from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, PasswordField
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod
from django import forms
from django.utils.translation import gettext

class CustomLoginForm(LoginForm):
    password = PasswordField(label=("رمز عبور"))
    error_messages = {
        'account_inactive':
        ("این حساب در حال حاضر غیرفعال است ."),

        'email_password_mismatch':
        ("The e-mail address and/or password you specified are not correct."),

        'username_password_mismatch':
        ("نام کابری یا رمز عبور اشتباه است ."),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        login_widget = forms.TextInput(attrs={'placeholder':
                                              ('نام کاربری'),
                                              'autofocus': 'autofocus'})
        username = forms.CharField(
            label=("نام کاربری"),
            widget=login_widget,
            max_length=100)

        self.fields["login"] = username

class CustomSignupForm(SignupForm):
    username = forms.CharField(label=("نام کاربری"),
                            #    min_length=app_settings.USERNAME_MIN_LENGTH,
                               widget=forms.TextInput(
                                   attrs={'placeholder':
                                          ('نام کاربری'),
                                          'autofocus': 'autofocus'}))
    field_order= [
                    'username',
                    'email',
                    'email2',  # ignored when not present
                    'password1',
                    'password2'  # ignored when not present
                ]

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label=("رمز عبور"))
        self.fields['password2'] = PasswordField(label=("تکرار رمز عبور"))
        self.fields['email'].label = gettext("ایمیل")

class CustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(
        label=("پست الکترونیک"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "email",
                   "size": "30",
                   "placeholder": ('آدرس پست الکترونیک')}))