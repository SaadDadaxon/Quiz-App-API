from django import forms
from .models import Account
from django.urls import reverse_lazy
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class AccountCreateForms(forms.ModelForm):
    password = forms.CharField(max_length=88, min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=88, min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', )

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2:
            if password != password2:
                raise forms.ValidationError('Parol mos emas! Try again')
            return password2
        return forms.ValidationError('Iltimos parolni kiriting')

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password'])
        if commit:
            account.save()
        return account


class AccountChangeForms(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = Account
        fields = ('email', 'full_name', 'image', 'is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AccountChangeForms, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = "<a href='%s'>change password</a>" % reverse_lazy(
            "admin:auth_user_password_change", args=[self.instance.id]
        )

    def clean_password(self):
        return self.initial['password']
