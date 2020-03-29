from django.urls import path, re_path, reverse_lazy
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
    PasswordResetView as DjangoPasswordResetView
)
from allauth.account.views import (
    LoginView, 
    SignupView, 
    ConfirmEmailView,
    PasswordResetView as AllAuthPasswordResetView,
    PasswordResetDoneView as AllAuthPasswordResetDoneView,
    PasswordResetFromKeyView as AllAuthPasswordResetFromKeyView,
    PasswordResetFromKeyDoneView as AllAuthPasswordResetFromKeyDoneView
)

from .forms import (
    UserPasswordResetForm, 
    UserSetPasswordForm, 
    AllAuthLoginForm, 
    AllAuthSignupForm, 
    AllAuthAddEmailForm, 
    AllAuthResetPasswordForm, 
    AllAuthResetPasswordKeyForm
)
from . import views

app_name = 'appaccounts'

urlpatterns = [
    
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileDetail.as_view(), name='profile'),
    url(r'^profile/(?P<pk>\d+)/edit/$', login_required(views.ProfileUpdate.as_view()), name='profile_edit'),
    
    ###################
    # Auth urls by Django
    ###################

    # register urls
    # url(r'^register/$', views.register, name='register'),
     
    # password reset
    # url(r'^password-reset/$', DjangoPasswordResetView.as_view(form_class=UserPasswordResetForm, success_url=reverse_lazy('appaccounts:password_reset_done')), name='password_reset'),
    # url(r'^password-reset/done/$', DjangoPasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    # url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', DjangoPasswordResetConfirmView.as_view(form_class=UserSetPasswordForm, success_url=reverse_lazy('appaccounts:password_reset_complete')), name='password_reset_confirm'),
    # url(r'^password-reset/complete/$', DjangoPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    ###################
    # Auth urls by AllAuth
    ###################

    # register urls
    url(r'^register/$', SignupView.as_view(form_class=AllAuthSignupForm, template_name='appaccounts/register.html'), name='register'),
    
    # password reset
    url(r'^password/reset/$', AllAuthPasswordResetView.as_view(form_class=AllAuthResetPasswordForm), name="password_reset"), 
    url(r'^password/reset/done/$', AllAuthPasswordResetDoneView.as_view(), name="account_reset_password_done"),
    # url(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', AllAuthPasswordResetFromKeyView.as_view(form_class=AllAuthResetPasswordKeyForm), name="account_reset_password_from_key"),
    url(r'^password/reset/key/done/$', AllAuthPasswordResetFromKeyDoneView, name="account_reset_password_from_key_done"),

    # Login
    url(r'^login/$', LoginView.as_view(form_class=AllAuthLoginForm, template_name='registration/login.html'), name='login'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),

    # E-mail
    url(r'^email/$', login_required(views.AllAuthEmailView.as_view()), name="account_email"),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name="confirm_email"),
    
    # change password
    url(r'^password-change/$', login_required(views.AllAuthPasswordChangeView.as_view()), name="password_change"),

    ## students urls
    # path('enroll-course/',
    #     views.StudentEnrollCourseView.as_view(),
    #     name='student_enroll_course'),
    # path('courses/',
    #     views.StudentCourseListView.as_view(),
    #     name='student_course_list'),
    # path('course/<pk>/',
    #     cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
    #     name='student_course_detail'),
    # path('course/<pk>/<module_id>/',
    #     cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
    #     name='student_course_detail_module'),

]
