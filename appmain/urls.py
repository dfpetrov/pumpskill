from django.urls import path
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'appmain'

urlpatterns = [
    # url(r'^$', views.SkillList.as_view(), name='index'),
    url(r'^$', views.main_page, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^myorders$', login_required(views.MyOrderListView.as_view()), name='my_order_list'),
]