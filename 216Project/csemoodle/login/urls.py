from django.conf.urls import url
#from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from login import views
from django.urls import path, include
from . import views
from django.conf.urls.static import static

app_name = 'login'

urlpatterns = [
    path('home/homepage/',views.index, name = 'homepage'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('istiakbro/courses123/', views.list_sessions, name='course_list'),
    path('peoples/', views.list_people, name='people_list'),
    path('student/', views.studentlogin, name='student_login'),
    path('teacher/', views.teacherlogin, name='teacher_login'),
   # path('upload_image/', views.upload_image, name='upload_image')
    #url(r'^$', views.index, name="home")
] + static(settings.MEDIA_URL, document_root =  settings.MEDIA_ROOT)