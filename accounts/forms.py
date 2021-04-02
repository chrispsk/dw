from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator
USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class UserForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control', 'type':'email', 'placeholder':"Required"}))
    city=forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':"Optional"}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta():
        model = User
        fields = ('username','email', 'city')


    # def clean_username(self): # handled by default (database)
    #    username = self.cleaned_data.get('username')
    #    if User.objects.filter(username=username).exists():
    #        raise forms.ValidationError("Username exists")
    #    return username

    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
           raise forms.ValidationError("Email exists")
       return email


    def clean_password2(self): # must have !!!!!!!!!!!!!!!
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True): # must have !!!!!!!!!!!!!!!
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            raise forms.ValidationError("Invalid Credentials!! [USERNAME]")
        if not user_obj.check_password(password):
                # log auth tries
            raise forms.ValidationError("Invalid Credentials!! [PASSWORD]")
        if not user_obj.is_active:
            raise forms.ValidationError("User is Inactive. Please contact the administrator!")

        return super(UserLoginForm, self).clean(*args, **kwargs)