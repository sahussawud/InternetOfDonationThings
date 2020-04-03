from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import user
from django.db import models

class regForm(UserCreationForm):
    username = forms.CharField(widget=
        forms.TextInput(attrs={'class':'form-control'}),
    )
    password1 = forms.CharField(widget=
        forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
        label="Password"
    )
    password2 = forms.CharField(widget=
        forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
        label="Password Confirm"
    )
    # first_name = forms.CharField(widget=
    #     forms.TextInput(attrs={'class':'form-control'}),
    # )
    # last_name = forms.CharField(widget=
    #     forms.TextInput(attrs={'class':'form-control'}),
    # )
    phone = forms.CharField(widget=
        forms.TextInput(attrs={'class':'form-control'}),
    )
    # address = forms.CharField(widget=
    #     forms.Textarea(attrs={'class':'form-control', 'style':'height:100px'}),
    # )
    is_accept = forms.BooleanField()
    email = forms.EmailField(widget=
        forms.TextInput(attrs={'class':'form-control'}),
    )
    profile_pic = forms.ImageField(required=True)

    class Meta:
        model = user
        fields = (
            'username',
            'password1',
            'password2',
            # 'first_name',
            # 'last_name',
            # 'address',
            'email',
            'phone',
            'is_accept',
            'profile_pic',
        )

    def save(self, commit=True):
        user = super(regForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.address = self.cleaned_data['address']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.is_accept = self.cleaned_data['is_accept']
        user.profile_pic = self.cleaned_data['profile_pic']

        if commit:
            user.save()
        return user
