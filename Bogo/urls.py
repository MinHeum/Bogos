"""Bogo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
import parsed_data.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', parsed_data.views.home, name="home"),
    path('parsed_data/login/',parsed_data.views.login, name="login"),
    path('accounts/',include('allauth.urls')),
    path('parsed_data/home/', parsed_data.views.home, name="home"),
    path('parsed_data/gs25/', parsed_data.views.gs25, name="gs25"),
    path('parsed_data/seven/', parsed_data.views.seven, name="seven"),
    path('parsed_data/emart/', parsed_data.views.emart, name="emart"),
    path('parsed_data/cu/', parsed_data.views.cu, name="cu"),
    path('parsed_data/ministop/', parsed_data.views.ministop, name="ministop"),

    path('parsed_data/post/',parsed_data.views.post, name = 'post'),
    path('parsed_data/post/<int:post_id>', parsed_data.views.detail, name='post_detail'),
    path('parsed_data/post/<int:post_id>/delete', parsed_data.views.delete, name='post_delete'),
    path('parsed_data/post/<int:post_id>/edit', parsed_data.views.edit, name='post_update'),
    path('parsed_data/post/new',parsed_data.views.new, name = 'post_new'),
    path('parsed_data/post/create',parsed_data.views.create, name='post_create'),
]
