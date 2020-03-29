from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from apporders import functions as OrderFunctions
from apporders.models import Order, OrderInCheck
from apptasks.models import Skill
from appcourses.models import Course
from appaccounts.forms import CourseEnrollForm
from allauth.account.views import ConfirmEmailView, EmailView, PasswordChangeView

from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, AllAuthAddEmailForm, AllAuthChangePasswordForm



class ProfileDetail(DetailView):
    model = Profile
    template_name = 'appaccounts/profile-detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        
        # lis of user's orders
        kwargs = {
            'filter_user': '==',
            'user': self.object.user,
            'add_skill_data': True,
            'add_fl_count': True,
        }
        context['orders'] = OrderFunctions.get_order_list(**kwargs)
        if self.request.user.is_authenticated:
            context['its_me'] = self.object == self.request.user.profile

        import json
        user_data = self.object.get_user_skills_data(user=self.object.user)
        context['user_skills_data'] = json.dumps(user_data['skills_data'])
        context['user_total_rate'] = user_data['total_rate_display']
        context['user_total_task_count'] = len(context['orders'])
        
        return context


class AllAuthEmailView(EmailView):

    template_name = "appaccounts/email.html"
    form_class = AllAuthAddEmailForm
    success_url = reverse_lazy('appaccounts:account_email')

    def get_context_data(self, **kwargs):
        
        context = super(AllAuthEmailView, self).get_context_data(**kwargs)

        context['profile'] = self.request.user.profile
        context['profile_chapter'] = 2
        context['post_url'] = reverse_lazy('appaccounts:account_email')
        context['form_file'] = False
        
        return context


class AllAuthPasswordChangeView(PasswordChangeView):

    template_name = "appaccounts/password_change.html"
    form_class = AllAuthChangePasswordForm
    success_url = reverse_lazy('appaccounts:password_change')

    def get_context_data(self, **kwargs):
        
        context = super(AllAuthPasswordChangeView, self).get_context_data(**kwargs)

        context['profile'] = self.request.user.profile
        context['profile_chapter'] = 3
        context['post_url'] = reverse_lazy('appaccounts:password_change')
        context['form_file'] = False
        
        return context


@login_required
def dashboard(request):
    return render(request, 'appaccounts/dashboard.html', {'section': 'dashboard'})


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'appaccounts/profile-edit.html'

    def get(self, request, *args, **kwargs):
        
        if request.user != self.get_object().user:
            raise Http404("Такой страницы не существует")
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        
        context['login'] = self.request.user.username
        context['first_name'] = self.request.user.first_name
        context['profile_chapter'] = 1
        context['post_url'] = reverse_lazy('appaccounts:profile_edit', kwargs={'pk': self.object.id})
        context['form_file'] = True
        
        if kwargs and 'profile_form' in kwargs:
            context['profile_form'] = kwargs['profile_form']
        else:
            context['profile_form'] = ProfileEditForm(instance=self.request.user.profile)
        
        return context
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(profile_form=form))

    def form_valid(self, form):
        
        first_name = self.request.POST.get('first_name', '')
        if first_name:
            self.request.user.first_name = first_name
            self.request.user.save()

        return super().form_valid(form)

    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            url = reverse_lazy('appaccounts:profile_edit', kwargs={'pk': self.object.id})
        return url


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    template_name = 'appaccounts/students/course/form.html'

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                     self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'appaccounts/students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'appaccounts/students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                                    id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context

