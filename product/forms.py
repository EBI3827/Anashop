from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, PasswordField
from allauth.account import app_settings
from django import forms
from django.utils.translation import gettext
from django.forms import ModelForm
from .models import Contact, ProductComment
# need django-simple-captcha module
from captcha.fields import CaptchaField

class CustomLoginForm(LoginForm):
    password = PasswordField(label=("رمز عبور"))
    error_messages = {
        'account_inactive':
        ("این حساب در حال حاضر غیرفعال است ."),

        'email_password_mismatch':
        ("آدرس ایمیل یا رمز عبور وارد شده اشتباه است ."),

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

class ContactForm(forms.ModelForm):
    name=forms.CharField(label="نام شما ", widget=forms.TextInput(attrs={ 
        'class': "form-control",
        }))
    email=forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={ 
        'class': "form-control",
        }))
    message=forms.CharField(label="پیام شما" , widget=forms.Textarea(attrs={ 
        'class': "form-control",
        }))

    class Meta:
        model = Contact
        fields = "__all__" 

class ProductCommentForm(forms.ModelForm):
    # username=forms.CharField(label="نام شما ", widget=forms.TextInput(attrs={ 
    #     'class': "form-control",
    #     }))
    # message=forms.CharField(label="پیام شما" , widget=forms.Textarea(attrs={ 
    #     'class': "form-control",
    #     }))
    # # captcha = CaptchaField(label="کد امنیتی ")
    # product=forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = ProductComment
        fields='__all__'
        exclude = ('approved','parent')
        widgets = {
            'product': forms.HiddenInput(),
            'username':forms.TextInput(attrs={ 
            'class': "form-control",
        }),
            'message': forms.Textarea(attrs={ 
            'class': "form-control",
        }),
        }

        labels = {
            'username': 'نام شما',
            'message': 'نظر شما',
        }
