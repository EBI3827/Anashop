from django import forms
from .models import UserProfile
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
import datetime
class FirstLastNameForm(forms.Form):
    first_name=forms.CharField(max_length=200,label='نام',widget=forms.TextInput(attrs={
        'class':'form-control',
    }))
    last_name=forms.CharField(max_length=200,label='نام خانوادگی',widget=forms.TextInput(attrs={
        'class':'form-control',
    }))

class EmailForm(forms.Form):
    email=forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={
        'class':'form-control',
    }))

class PhoneForm(forms.Form):
    phone_number=forms.CharField(max_length=11, label='شماره موبایل',widget=forms.TextInput(attrs={
        'class':'form-control',
    }))

this_year=datetime.date.today().year
YEARS=[i for i in range(this_year,this_year-90,-1)]
class BirthDateForm(forms.Form):
    birth_date=forms.DateField(label='تاریخ تولد',help_text='زبان خود را به انگلیسی تغییر دهید', widget=forms.SelectDateWidget(attrs={
        # 'placeholder':'2006-10-25',
        'class':'form-control',
    },years=YEARS))

class ImageForm(forms.Form):
    image=forms.ImageField(label='تصویر کابر')

