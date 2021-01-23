from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
# from .api import EmployeeApi
from django.conf.urls import url, include

app_name = 'vms'

urlpatterns = [

    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/dj_rest_auth/', include('dj_rest_auth.urls')),
    path('', views.registerpage, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('home/', views.home, name='home'),
    path('visitor/', views.visitors, name='visitor'),
    path('employee_detail/', views.employee_detail, name='employee_detail'),
    path('employee/<int:e_id>/', views.employee, name='employee'),
    path('employee_profile/', views.employeeProfilePage, name='emp-profile-page'),
    path('settings/', views.employeeSettings, name='settings'),

    path('new_visitor/', views.AddVisitor, name='add_visitor'),
    path('update_visitor/<int:pk>/', views.UpdateVisitor, name='update_visitor'),
    path('delete_visitor/<int:pk>/', views.DeleteVisitor, name='delete_visitor'),
    #  path('create_visit/<int:pk>', views.createVisit, name='create_visit'),
    path('new_visit/', views.createVisit, name='new_visit'),
    path('update_visit/<int:pk>/', views.updateVisit, name='update_visit'),
    path('delete_visit/<int:pk>/', views.deleteVisit, name='delete_visit'),
    path('new_employee/', views.AddEmployee, name='add_employee'),
    path('update_employee/<int:e_id>/',
         views.updateEmployee, name='update_employee'),
    path('delete_employee/<int:pk>/',
         views.deleteEmployee, name='delete_employee'),

    path('new_employee/check_username_exist',
         views.check_username_exist, name="check_username_exist"),
    path('new_employee/check_email_exist',
         views.check_email_exist, name="check_email_exist"),
    path('check_username_exist',
         views.check_username_exist, name="check_username_exist"),
    path('check_email_exist',
         views.check_email_exist, name="check_email_exist"),

    path('api/', views.EmpList.as_view()),
    path('api/<int:pk>/', views.EmpDetail.as_view()),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
