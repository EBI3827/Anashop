from django import forms
from .models import BlogComment


class BlogCommentForm(forms.ModelForm):
    # username=forms.CharField(label="نام شما ", widget=forms.TextInput(attrs={
    #     'class': "form-control",
    #     }))
    # message=forms.CharField(label="پیام شما" , widget=forms.Textarea(attrs={
    #     'class': "form-control",
    #     }))
    # # captcha = CaptchaField(label="کد امنیتی ")
    # product=forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = BlogComment
        fields = '__all__'
        exclude = ('approved', 'parent')
        widgets = {
            'blog': forms.HiddenInput(),
            'username': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control",
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'test@test.com',
            })
        }

        error_messages = {
            'email': {
                'invalid': ('آدرس ایمیل وارد شده نامعتبر است !'),
            },
        }

        labels = {
            'username': 'نام شما',
            'email': 'ایمیل شما',
            'message': 'متن پیام',
        }
