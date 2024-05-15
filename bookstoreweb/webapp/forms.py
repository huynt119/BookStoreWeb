from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    password_repeat = forms.CharField(label="password_repeat", max_length=100, widget= forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_num', 'password']
          
    def save(self, commit=True):
    # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get("password_repeat")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("* Passwords don't match")
        return cleaned_data

class PaymentForm(forms.Form):
    card_number = forms.CharField(label="Card Number", max_length=16)
    card_holder = forms.CharField(label="Card Holder", max_length=100)
    expiration_date = forms.DateField(label="Expiration Date")
    cvv = forms.CharField(label="CVV", max_length=3)
