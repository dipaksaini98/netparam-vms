from rest_framework.permissions import IsAuthenticated
import random as r
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import Group

from .models import Employee, Visit, Visitor, Event
from .forms import EmployeeCreationForm, EmployeeChangeForm, VisitForm, AddVisitorForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .serializers import EmployeeSerializer
from .filters import VisitFilter

from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

# Create your views here.


@unauthenticated_user
def registerpage(request):

    fm = EmployeeCreationForm()
    if request.method == 'POST':
        fm = EmployeeCreationForm(request.POST or None)
        if fm.is_valid():

            name = fm.cleaned_data.get('name')
            username = fm.cleaned_data.get('username')
            email = fm.cleaned_data.get('email')


#############################Email Send##############################################################
            ctx = {
                'username': username,
                'name': name,
                'form': fm
            }
            message = get_template('vms/email_template.html').render(ctx)
            mail = EmailMessage("test-mail", message,
                                settings.EMAIL_HOST_USER, [email],)
            mail.content_subtype = "html"
            mail.send(fail_silently=False)
            print("mail sent successfully!!")

            # group = Group.objects.get(name='User')
            # request.user.groups.add(group)
            # Employee.objects.create(user=user)
            fm.save()
            messages.success(request, 'Account was created for '+username)
            return redirect('/login/')
    return render(request, 'vms/register.html', {'form': fm})


@unauthenticated_user
def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, 'Username or Password is incorrect!!')
    return render(request, 'vms/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def home(request):
    visits = Visit.objects.all()
    employees = Employee.objects.all()

    total_employees = employees.count()

    total_visits = visits.count()
    done = visits.filter(status='Done').count()
    pending = visits.filter(status='Pending').count()

    context = {'visits': visits, 'employees': employees, 'total_employees': total_employees,
               'total_visits': total_visits, 'done': done, 'pending': pending}
    return render(request, 'vms/dashboard.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def visitors(request):
    visitors = Visitor.objects.all()
    visits = Visit.objects.all()
    return render(request, 'vms/visitors.html', {'visitors': visitors, 'visits': visits})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def AddVisitor(request):
    fm = AddVisitorForm()

    if request.method == 'POST':
        fm = AddVisitorForm(request.POST, request.FILES)

        if fm.is_valid():
            name = fm.cleaned_data.get('name')
            email = fm.cleaned_data.get('email')
            otp = otpgen()
            ctx = {
                'name': name,
                'form': fm,
                'otp': otp
            }
            message = get_template('vms/visit_confirm_mail.html').render(ctx)
            mail = EmailMessage("test-mail", message,
                                settings.EMAIL_HOST_USER, [email],)
            mail.content_subtype = "html"
            mail.send(fail_silently=False)
            print("mail sent successfully!!")

            fm.save()
            return redirect('/visitor/')
    return render(request, 'vms/addvisitor.html', {'form': fm})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def UpdateVisitor(request, pk):
    visitor = Visitor.objects.get(id=pk)
    fm = AddVisitorForm(instance=visitor)
    if request.method == 'POST':
        fm = AddVisitorForm(request.POST, request.FILES, instance=visitor)
        if fm.is_valid():
            fm.save()
        return redirect('/visitor/')
    return render(request, 'vms/addvisitor.html', {'form': fm})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def DeleteVisitor(request, pk):
    visitor = Visitor.objects.get(id=pk)
    if request.method == 'POST':
        visitor.delete()
        return redirect('/visitor/')
    return render(request, 'vms/delete_visitor.html', {'visitor': visitor})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def employee_detail(request):
    employees = Employee.objects.all()
    return render(request, 'vms/employee_detail.html', {'employees': employees})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def employee(request, e_id):
    employee = Employee.objects.get(id=e_id)
    visits = employee.visit_set.all()
    visits_count = visits.count()

    emp_filter = VisitFilter(request.GET, queryset=visits)
    visits = emp_filter.qs

    context = {'employee': employee, 'visits': visits,
               'visits_count': visits_count, 'emp_filter': emp_filter}
    return render(request, 'vms/employee.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['User'])
def employeeProfilePage(request):
    visits = request.user.visit_set.all()
    total_visits = visits.count()
    done = visits.filter(status='Done').count()
    pending = visits.filter(status='Pending').count()

    context = {'visits': visits, 'total_visits': total_visits,
               'done': done, 'pending': pending}
    return render(request, 'vms/emp_profile.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['User'])
def employeeSettings(request):
    employee = request.user
    form = EmployeeChangeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeChangeForm(
            request.POST, request.FILES, instance=employee)
        if form.is_valid:
            form.save()
    context = {'form': form, 'employee': employee}
    return render(request, 'vms/employee_settings.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def AddEmployee(request):
    fm = EmployeeCreationForm()
    if request.method == 'POST':
        fm = EmployeeCreationForm(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data.get('name')
            username = fm.cleaned_data.get('username')
            email = fm.cleaned_data.get('email')
            ctx = {
                'username': username,
                'name': name,
                'form': fm
            }
            message = get_template('vms/email_template.html').render(ctx)
            mail = EmailMessage("test-mail", message,
                                settings.EMAIL_HOST_USER, [email],)
            mail.content_subtype = "html"
            mail.send(fail_silently=False)
            print("mail sent successfully!!")
            g = Group.objects.get(name='User')
            g.user_set.add(request.user)
            request.user.save()
            fm.save()
            return redirect('/employee_detail')
    return render(request, 'vms/add_emp.html', {'form': fm})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def updateEmployee(request, e_id):
    employee = Employee.objects.get(id=e_id)
    form = EmployeeChangeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeChangeForm(request.POST, instance=employee)
        if form.is_valid:
            form.save()

        return redirect(reverse('vms:employee', args=(e_id,)))
    context = {'form': form, 'employee': employee}
    return render(request, 'vms/update_employee.html', context)


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def deleteEmployee(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('/home/')

    return render(request, 'vms/delete_employee.html', {'employee': employee})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def createVisit(request):
    fm = VisitForm()
    print(fm)
    if request.method == 'POST':
        fm = VisitForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('/')

    return render(request, 'vms/visit_form.html', {'form': fm})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def updateVisit(request, pk):
    visit = Visit.objects.get(id=pk)
    form = VisitForm(instance=visit)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('/home/')
    return render(request, 'vms/visit_form.html', {'form': form})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['Admin'])
def deleteVisit(request, pk):
    visit = Visit.objects.get(id=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('/home/')

    return render(request, 'vms/delete_visit.html', {'visit': visit})


###########################Serialization#####################################################


class EmpList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmpDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


################Check Existing User name and Email################################################


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    data = {'is_taken': Employee.objects.filter(
        username__iexact=username).exists()}
    print(data)
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse(data)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    data = {'is_taken': Employee.objects.filter(email__iexact=email).exists()}
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse(data)


######################################################################################################

# function for otp generation


def otpgen():
    otp = ""
    for i in range(6):
        otp += str(r.randint(1, 9))
    return otp
