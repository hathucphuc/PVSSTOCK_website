import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from .utils import ActivationMailFormMixin
from .models import Provider
from search_device.models import ManageDevice


logger = logging.getLogger(__name__)

class ResendActivationEmailForm(
        ActivationMailFormMixin, forms.Form):

    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                email=self.cleaned_data['email'])
        except:
            logger.warning(
                'Resend Activation: No user with '
                'email: {} .'.format(
                    self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user


class ProviderSignUpForm(ActivationMailFormMixin,UserCreationForm):
    name = forms.CharField(label="Company Name",max_length=10)
    full_name = forms.CharField(label='Full Company Name',max_length=100)
    phone = forms.CharField(label='Hotline',max_length=15)
    url = forms.URLField(label='URL Website',max_length=200)

    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("name","full_name","email","phone","url")


    def clean_name(self):
        name = self.cleaned_data["name"]
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if name in disallowed:
            raise ValidationError("A user with that name already exists.")
        return name

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"]
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if full_name in disallowed:
            raise ValidationError("A user with that full name already exists.")
        return full_name

    @transaction.atomic
    def save(self,**kwargs):
        user = super().save(commit=False)
        user.is_provider = True
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        Provider.objects.update_or_create(user=user,defaults={'name': self.cleaned_data['name'] ,"slug": slugify(self.cleaned_data["name"]),"full_name":self.cleaned_data["full_name"],'phone': self.cleaned_data['phone'],'url': self.cleaned_data['url']},)
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user

class ProviderChangeForm(forms.Form):
    name = forms.CharField(required=False)
    full_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    url = forms.URLField(required=False)
    skype_name = forms.CharField(required=False)
    zalo_link = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ProviderChangeForm, self).__init__(*args, **kwargs)

    class Meta():
        fields = ("name","full_name","email","phone","url","skype_name","zalo_link")

    

    def clean_name(self):
        name = self.cleaned_data["name"]
        
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if name in disallowed:
            raise ValidationError("A user with that name already exists.")
        try:
            Provider.objects.get(name=name)
            raise ValidationError("A user with that name already exists.")
        except (FieldError, ValueError, Provider.DoesNotExist):
            print("name")           
            return name
        

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"]
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if full_name in disallowed:
            raise ValidationError("A user with that full name already exists.")

        try:
            Provider.objects.get(full_name=full_name)
            raise ValidationError("A full name with that name already exists.")
        except(FieldError, ValueError, ObjectDoesNotExist):
            print("full_name")            
            return full_name
        

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        try:
            User.objects.get(email=email)
            raise ValidationError("A email with that name already exists.")
        except(FieldError, ValueError, ObjectDoesNotExist):
            print("email")             
            return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        try:
            Provider.objects.get(phone=phone)
            raise ValidationError("A phone with that name already exists.")
        except(FieldError, ValueError, ObjectDoesNotExist):
            print("phone")              
            return phone

    def clean_url(self):
        url = self.cleaned_data["url"]
        try:
            Provider.objects.get(url=url)
            raise ValidationError("A url with that name already exists.")
        except(FieldError, ValueError, ObjectDoesNotExist):
            print("url")               
            return url

    def clean_skype_name(self):
        skype_name = self.cleaned_data["skype_name"]
        if skype_name!="":

            try:
                print("skpye_f")
                Provider.objects.get(skype_name=skype_name)
                print("skype_a")
                raise ValidationError("A name skype with that name already exists.")
            except(FieldError, ValueError, ObjectDoesNotExist):
                print("skype_name")             
                return skype_name
        else:
            return skype_name

    def clean_zalo_link(self):
        zalo_link = self.cleaned_data["zalo_link"]
        print("zalo")
        if zalo_link!="":
            try:
                print("zalo_a")
                Provider.objects.get(zalo_link=zalo_link)
                print("zalo_a")
                raise ValidationError("A link zalo with that link already exists.")
            except(FieldError, ValueError, ObjectDoesNotExist):
                print("zalo_link")               
                return zalo_link
        else:
            return zalo_link
    
    def clean(self):
        if not self.cleaned_data.get("name") and not self.cleaned_data.get("full_name") and not self.cleaned_data.get("email") and not self.cleaned_data.get("phone") and not self.cleaned_data.get("skype_name") and not self.cleaned_data.get("zalo_link") and not self.cleaned_data.get("url"):
            print("worng")
            raise ValidationError("All fields are blank!!!")
        print("clean")
        return self.cleaned_data


    def save(self):
        user = self.user
        provider = Provider.objects.get(user=user)
        if self.cleaned_data["name"]:
            provider.name = self.cleaned_data['name']
            ManageDevice.objects.filter(user=user).update(provider=self.cleaned_data['name'])
        if self.cleaned_data["full_name"]:
            provider.full_name = self.cleaned_data['full_name']
        if self.cleaned_data["phone"]:
            provider.phone = self.cleaned_data['phone']
            ManageDevice.objects.filter(user=user).update(phone=self.cleaned_data['phone'])
        if self.cleaned_data["url"]:
            provider.url = self.cleaned_data['url']
        if self.cleaned_data["skype_name"]:
            print("123")
            provider.skype_name = self.cleaned_data["skype_name"]
        if self.cleaned_data["zalo_link"]:
            provider.zalo_link = self.cleaned_data["zalo_link"]
        provider.save()

        if self.cleaned_data["email"]:
            user.email = self.cleaned_data['email']
        user.save()

        return provider





