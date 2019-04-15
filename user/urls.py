from django.conf.urls import include, url
from django.urls import reverse_lazy
from django.views.generic import (RedirectView, TemplateView)
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .views import ActivateAccount, ProviderSignUpView, ResendActivationEmail, profile


app_name = "user"

password_urls = [
    url(r'^$',
        RedirectView.as_view(
            pattern_name='user:pw_reset_start',
            permanent=False)),

    url(r'^change/$',
        auth_views.PasswordChangeView.as_view(
        template_name=
            'user/password_change_form.html',
         success_url= reverse_lazy(
            'user:pw_change_done')),
        name='pw_change'),
    url(r'^change/done/$',
        auth_views.PasswordChangeDoneView.as_view(
        template_name=
            'user/password_change_done.html'),
        name='pw_change_done'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
        template_name=
            'user/password_reset_form.html',
         email_template_name=
            'user/password_reset_email.txt',
         subject_template_name=
            'user/password_reset_subject.txt',
         success_url= reverse_lazy(
            'user:pw_reset_sent')),
        name='pw_reset_start'),
    url(r'^reset/sent/$',
        auth_views.PasswordResetDoneView.as_view(
        template_name=
            'user/password_reset_sent.html'),
        name='pw_reset_sent'),
    url(r'^reset/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
        template_name=
            'user/password_reset_confirm.html',
        success_url= reverse_lazy(
            'user:pw_reset_complete')),
        name='pw_reset_confirm'),
    url(r'reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(
        template_name=
            'user/password_reset_complete.html',
        extra_context=
             {'form': AuthenticationForm}),
        name='pw_reset_complete'),
]


urlpatterns = [

		url(r'^$',
        RedirectView.as_view(
            pattern_name='user:login',
            permanent=False)),
		
		url(r'^create-provider/$',
        ProviderSignUpView.as_view(),
        name='create_provider'),

        url(r'^create-provider/done/$',
        TemplateView.as_view(
        template_name=(
        'user/user_create_done.html')),
        name='create_done'),

		url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        ActivateAccount.as_view(),
        name='activate'),

		url(r'^activate/resend/$',
        ResendActivationEmail.as_view(),
        name='resend_activation'),

		url(r'^login/$',
        LoginView.as_view(
        template_name= 'user/login.html'),
        name='login'),

		url(r'^logout/$',
        auth_views.LogoutView.as_view(
        template_name= 'user/logged_out.html',
        extra_context=
             {'form': AuthenticationForm}),
        name='logout'),

        url(r'^password/', include(password_urls)),

        url(r"^profile/$",profile,name="profile"),


]
