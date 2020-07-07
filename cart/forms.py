from django import forms
from .models import MyCity
from cities_light.models import City
from django.core.validators import RegexValidator
# from dal import autocomplete
# from dal_select2.widgets import ModelSelect2

PAYMENT_METHOD=(
    ('DE','پرداخت هنگام تحویل'),
    # ('CH','واریز به حساب'),
    # ('ZA', 'زرین پال'),
)

class CouponForm (forms.Form):
    code=forms.CharField(max_length=15,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'کد تخفیف'
    }))

class ProfileForm(forms.ModelForm):
    location = forms.ModelChoiceField(label='شهر',
    queryset=City.objects.all(),
    widget=(forms.Select(attrs={
        'class':'form-control'
    }))
    # widget=ModelSelect2(url='cart:country-autocomplete')
    )
    class Meta:
        model = MyCity
        fields = ('location',)

class CheckoutForm(forms.Form):
    first_name=forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    last_name=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    email=forms.EmailField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'test@test.com'
        # 'type':'email'
    }),error_messages={'invalid': 'آدرس ایمیل وارد شده نامعتبر است !'})
    phone = forms.CharField(required=False,max_length=11, validators=[RegexValidator('^(\+98|0)?9\d{9}$', 
        message = "شماره تلفن باید با فرمت : (۰۹۹۹۹۹۹۹۹۹۹) وارد شود .",code="invalid")],widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'مثال : **********۰۹',
    }))
    address=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    postal_code=forms.CharField(required=False,min_length=10,max_length=10,validators=[RegexValidator('^[0-9]*$',message='کد پستی فقط باید شامل اعداد باشد.')], widget=forms.TextInput(attrs={
        'class':'form-control'
    }),error_messages={'invalid':'کد پستی فقط باید شامل اعداد باشد .'},)
    set_default_info = forms.BooleanField(required=False)
    use_default_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_METHOD, initial='DE')
    agreed=forms.BooleanField(required=True,widget=forms.CheckboxInput(attrs={'class':"validate required"}))