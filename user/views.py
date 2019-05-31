from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import (
    get_user, get_user_model, logout)
from django.contrib.auth.decorators import \
    login_required
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.messages import error, success
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.template.response import \
    TemplateResponse
from django.utils.decorators import \
    method_decorator
from django.utils.encoding import force_text
from django.utils.http import \
    urlsafe_base64_decode
from django.views.decorators.cache import \
    never_cache
from django.views.decorators.csrf import \
    csrf_protect
from django.views.decorators.debug import \
    sensitive_post_parameters
from django.views.generic import View

from .utils import MailContextViewMixin
from .forms import (
    ResendActivationEmailForm, ProviderSignUpForm, ProviderChangeForm)
from .models import Provider, User
from search_device.forms import AddDeviceForm, AddStoreForm
from search_device.models import ManageDevice, RequestQuota


# Create your views here.



class ActivateAccount(View):
    success_url = reverse_lazy('user:login')
    template_name = 'user/user_activate_failed.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            # urlsafe_base64_decode()
            #     -> bytestring in Py3
            uid = force_text(
                urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError,
                OverflowError, User.DoesNotExist):
            user = None
        if (user is not None
                and token_generator
                .check_token(user, token)):
            user.is_active = True
            user.save()
            success(
                request,
                'User Activated! '
                'You may now login.')
            return redirect(self.success_url)
        else:
            return TemplateResponse(
                request,
                self.template_name)

class ProviderSignUpView(MailContextViewMixin, View):
    form_class = ProviderSignUpForm
    success_url = reverse_lazy(
        'user:create_done')
    template_name = 'user/user_create_provider.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters(
        'password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            # not catching returned user
            bound_form.save(
                **self.get_save_kwargs(request))
            if bound_form.mail_sent:  # mail sent?
                return redirect(self.success_url)
            else:
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                # TODO: redirect to email resend
                return redirect("user:resend_activation")
        return TemplateResponse(
            request,
            self.template_name,
            {'form': bound_form})

class ResendActivationEmail(
        MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(
                **self.get_save_kwargs(request))
            if (user is not None
                    and not bound_form.mail_sent):
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop(
                        '__all__')
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url)

def profile(request):
    user = request.user
    tickets = RequestQuota.objects.all()
    # view for PVS staffs
    if user.is_staff:
        if user.is_superuser:
            roles = "Admin"
        else:
            roles = "PVS staff"
        list_device = ManageDevice.objects.filter(public=True)
        if request.method=="POST":
            form = ProviderChangeForm(request.POST,user=request.user)
            if form.is_valid():
                form.save()
                return redirect("user:profile")
        else:
            form = ProviderChangeForm()
            vendors = User.objects.filter(is_provider=True)
        return render(request,"user/profile_pvs.html",{"form":form,"roles":roles,"list_device":list_device,"vendors":vendors,"tickets":tickets})

    # view for vendor
    elif user.is_provider:
        roles = "Provider"
        list_device = ManageDevice.objects.filter(user=user)
        if request.method == "POST":
            form = ProviderChangeForm(request.POST,user=request.user)
            form_add = AddDeviceForm(request.POST,user=request.user)
            form_add_store = AddStoreForm()
            if form_add.is_valid():
                print("form_add")
                form_add.save()
                return redirect("user:profile")
            
            elif form.is_valid():
                form.save()
                print("456")
                return redirect("user:profile")

        else:
            form = ProviderChangeForm()
            form_add = AddDeviceForm(user=user)
            form_add_store = AddStoreForm()           
        return render(request,"user/profile.html",{"form":form,"form_add":form_add,"form_add_store":form_add_store,"user":user,"roles":roles,"list_device":list_device})
















