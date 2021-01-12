from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, DateInput
from django import forms
from django.contrib.auth.models import User
# this is for the authentication system that we've worked with before
from django.contrib.auth.forms import UserCreationForm
from prompt_toolkit.layout import Layout
from django.core import validators
from home.models import Customer, DeliveryInfo
from django.forms import SelectDateWidget
import datetime

class RegistrationForm(UserCreationForm):
    # parantez içindeki inheritance özelliğini aktarmak içindir, inherite ettiği class yani
    email = forms.EmailField(widget=forms.EmailInput, validators=[validators.EmailValidator()])
    first_name = forms.CharField()
    last_name = forms.CharField()

    # email field orijinalde django user authentication sisteminde dahil değil sanırım
    # meta classta onu da ekledik ama username ve password1 password2 kendileri var zaten, password 1 ve 2 ikisinin eşleşip eşleşmediğini kontrol etmek için
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CustomerForm(ModelForm):
    years_to_display = range(datetime.datetime.now().year - 100,
                             datetime.datetime.now().year)
    date = forms.DateField(widget=SelectDateWidget(years = years_to_display))
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class AddressForm(ModelForm):

    class Meta:
        model = DeliveryInfo
        fields = '__all__'
        exclude = ['belongs_to']