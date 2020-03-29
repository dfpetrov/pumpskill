from django.shortcuts import render, get_object_or_404, resolve_url
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings

from apporders.models import Order
from apptasks.models import Task, Skill, TaskFavourites
from apptasks import functions as TaskFunctions
from apporders import functions as OrderFunctions


@login_required
def dashboard(request):

    request_user = request.user

    context = {
        'order_href_title_prefix': settings.ORDER_HREF_TITLE_PREFIX,
        'task_href_title_prefix': settings.TASK_HREF_TITLE_PREFIX,
        'skill_href_title_prefix': settings.SKILL_HREF_TITLE_PREFIX,
    }

    # list of new task:
    kwargs = {
        'filter_author': '!=',
        'author': request_user,
        'filter_order': '-',
        'add_author_data': True,
        'add_skill_data': True,
        'add_fl_count': True,
        'count': 5,
    }
    context['new_tasks'] = TaskFunctions.get_task_list(**kwargs)

    # list of user's tasks:
    kwargs['filter_author'] = '=='
    kwargs['filter_order'] = None
    context['my_tasks'] = TaskFunctions.get_task_list(**kwargs)
    
    # lis of user's orders
    kwargs = {
        'filter_user': '==',
        'user': request_user,
        'add_skill_data': True,
        'count': 5,
    }
    context['user_orders'] = OrderFunctions.get_order_list(**kwargs)

    # list of favourite tasks
    context['task_favourites'] = TaskFunctions.get_favourites_task_list(user=request_user, count=5)
    
    # list of favourite orders
    context['order_favourites'] = OrderFunctions.get_favourites_order_list(user=request_user, count=5)

    return render(request, 'appmain/dashboard.html', context)


def main_page(request):

    context = {
        # 'css_path': 'css/app2.css',
        'js_path': 'js/app2.js',
        'skill_list': Skill.objects.all(),
    }

    return render(request, 'appmain/index.html', context)


class SkillList(generic.ListView):
    model = Skill
    template_name = 'appmain/skill_list.html'
    paginate_by = 50
    
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skills = []
        skill_list = Skill.objects.all()
        for skill in skill_list:
            data = {
                'title': skill.title, 
                'description': skill.description,
                'description_min': skill.description_min, 
                'url': skill.get_absolute_url
            }
            if skill.avatar:
                data['avatar'] = skill.avatar.url
            else:
                data['avatar'] = ''
            skills.append(data)

        # пагинация
        page_size = self.get_paginate_by(skills)
        if page_size:
            paginator, page, skills, is_paginated = self.paginate_queryset(
                skills, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': skills
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': skills
            }

        context['skills'] = skills

        return context

class MyOrderListView(generic.ListView):
    model = Order
    template_name = 'appmain/myorder_list.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(MyOrderListView, self).dispatch(request, *args, **kwargs)
        
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by
        
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # lis of user's orders
        kwargs = {
            'filter_user': '==',
            'user': self.request.user,
            'add_task_data': True,
            'add_skill_data': True,
        }
        order_list = OrderFunctions.get_order_list(**kwargs)

        # пагинация
        page_size = self.get_paginate_by(order_list)
        if page_size:
            paginator, page, order_list, is_paginated = self.paginate_queryset(
                order_list, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': order_list
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': order_list
            }

        context['order_count'] = len(order_list)
        context['orders'] = order_list

        return context
