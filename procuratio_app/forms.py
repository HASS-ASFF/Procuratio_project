from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import ModelForm

from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import *
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'image_profil']

        def clean_email(self):
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    'Please use another Email, that is already taken')
            return email

        def save(self, commit=True):
            user = super(UserForm, self).save(commit=False)

            if commit:
                user.save()
            return user

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3 username_personne'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-3 email_personne'}),
            'image_profil': forms.FileInput(attrs={'class': 'form-control mb-3 password_personne'})
        }


class ClientForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def save(self, commit=True):
        user = super(ClientForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3 username_personne', 'id': 'floatingText', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3 email_personne', 'id': 'floatingInput', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control password_personne', 'id': 'floatingPassword', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control password2_personne', 'id': 'floatingPassword', 'placeholder': 'Repeat Password'})
        self.fields['num_tel'].widget.attrs.update(
            {'class': 'form-control mb-3 num_tel_personne', 'id': 'floatingText', 'placeholder': 'numéro de téléphone'})
    class Meta:
        model = Client
        fields = ['username', 'password', 'email','num_tel']






class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Votre ancien mot passe"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "Votre nouveau mot passe"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Répétez votre nouveau mot de passe"})


class RendezVousForm(ModelForm):
    class Meta:
        model = RendezVous
        fields = '__all__'

class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class CForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['services_list']