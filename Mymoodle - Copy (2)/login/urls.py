from django.conf.urls import url
from login import views

app_name = 'login'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/', views.user_login, name='user_login'),
    url(r'^courses/$', views.list_sessions, name='course_list'),
    url(r'^peoples/$', views.list_people, name='people_list'),
    url(r'^student/$', views.studentlogin, name='student_login'),
    url(r'^teacher/$', views.teacherlogin, name='teacher_login'),
    url(r'^$', views.index, name="home")

]
