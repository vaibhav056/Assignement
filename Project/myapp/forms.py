# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    phonenumber=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['phonenumber'].widget.attrs['class'] ='input'
        self.fields['phonenumber'].widget.attrs['placeholder'] ='Phonenumber'
        self.fields['password'].widget.attrs['class'] ='input'
        self.fields['password'].widget.attrs['placeholder']='Password'
        self.fields['password'].widget.attrs['id']='password'
    
    def clean_phonenumber(self):
        phone=self.cleaned_data.get('phonenumber',False)
        if(phone and len(str(phone))==10 and phone.isnumeric()):
            try:
                User.objects.get(phonenumber=phone)
            except:
                raise forms.ValidationError("Mobile Number Not Registered.!")
        else:
            raise forms.ValidationError("Please Enter Valid Mobile Number .!")
        return phone
    
    def clean_password(self):
        password=self.cleaned_data.get('password',False)
        if(password and len(password)>1):
            pass
        else:
            raise forms.ValidationError("Please Enter Password Correctly .!")
        return password

    def clean(self):
        cleaned_data=super().clean()
        phonenumber_=cleaned_data.get('phonenumber',None)
        password_=cleaned_data.get('password',None)
        if phonenumber_ and password_:
            pass
        else:
            raise forms.ValidationError("Please Enter Valid Details .!")




    

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber')
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['full_name'].widget.attrs['id'] = 'full_name'
        self.fields['phonenumber'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phonenumber'].widget.attrs['id'] = 'phonenumber'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['id'] = 'email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['id'] = 'password2'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken .!")
        return email
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if(len(str(phonenumber)) != 10):
            raise forms.ValidationError("Enter Valid Phonenumber .!") 
        qs = User.objects.filter(phonenumber=phonenumber)
        if qs.exists():
            raise forms.ValidationError("Phonenumber is Already taken .!")
        return phonenumber

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1 or len(str(password1))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if not password2 or len(str(password2))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password2
    
    
    def clean(self):
        cleaned_data=super().clean()
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        if(password1 and password2):
            if(password1!=password2):
                raise forms.ValidationError("Password Not Matched .!")
        else:
            raise forms.ValidationError("Enter Passwrods .!")


class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber','admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active=True
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]