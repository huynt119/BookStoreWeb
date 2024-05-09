from django import forms


class SignInForm(forms.Form):
    uname = forms.CharField(label="uname", max_length=100)
    psw = forms.CharField(label="psw", max_length=100)

class SignUpForm(forms.Form):
    first_name = forms.CharField(label="first-name", max_length=100)
    last_name = forms.CharField(label="last-name", max_length=100)
    email = forms.CharField(label="email", max_length=100)
    psw = forms.CharField(label="psw", max_length=100)
    psw_repeat = forms.CharField(label="psw-repeat", max_length=100)