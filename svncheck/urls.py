"""svncheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_user import views as app_user_views
from app_svn import views as app_svn_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_user_views.login),
    path('svn/', app_user_views.index),
    path('mainblank/', app_user_views.mainblank),
    path('chg_pwd/', app_user_views.chg_pwd),
    path('chgpwd_action/', app_user_views.chgpwd_action),

    path('upload/', app_svn_views.upload),
    path('upload_page/', app_svn_views.upload_page),
    path('check_action/', app_svn_views.check_action),
    path('check_page/', app_svn_views.check_page),
    path('check_page/result_page/', app_svn_views.check_result_page),
    path('check_page/result_action/', app_svn_views.check_result_action),
    path('settag/', app_svn_views.settag),
    path('check_count/', app_svn_views.check_count_page),
    path('check_count_action/', app_svn_views.check_count_action),

]
