"""teebag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from teebagapi.views import register_user, login_user, GolferView, CourseView, NoteView, RoundView, HoleView, ClubView, MyClubView, MyBagView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'golfers', GolferView, 'golfer')
router.register(r'courses', CourseView, 'course')
router.register(r'notes', NoteView, 'note')
router.register(r'rounds', RoundView, 'round')
router.register(r'holes', HoleView, 'hole')
router.register(r'clubs', ClubView, 'club')
router.register(r'myclubs', MyClubView, 'myclub')
router.register(r'mybags', MyBagView, 'mybag')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]