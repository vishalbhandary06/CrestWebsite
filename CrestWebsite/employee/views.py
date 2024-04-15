from django.contrib import auth, messages
from django.shortcuts import redirect, render
from .models import Employee, Relationship, Emergency
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.core.paginator import Paginator


def login_user(request):
    context = {}

    if request.method == 'POST':
        form = EmployeeAuthentiationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
    
    else:
        form = EmployeeAuthentiationForm()

    context = {'form' : form}
    return render(request, 'employee/login.html', context)
    

def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    logout(request)
    return redirect('login_user')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags = 'alert alert-danger alert-dismissible show')
            
    form = PasswordChangeForm(request.user)
    context = {}
    context['form'] = form
    return render(request, "dashboard/change_password.html", context)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    return render(request, "dashboard/dashboard.html")
    

def profile_personal(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        form = EmployeePersonalUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile successfully updated !!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('profile_personal')
    else:
        form = EmployeePersonalUpdateForm(
            initial={
                'email' : request.user.email,
                'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'gender' : request.user.gender,
                'birthday' : request.user.birthday,
                'c_address': request.user.c_address,
                'p_address': request.user.p_address,
                'phone': request.user.phone,
                'per_email': request.user.per_email,
                'marital': request.user.marital,
                'blood': request.user.blood,
            }
        )

    profile = request.user
    context = {'profile' : profile, 'form' : form}
    return render(request, "employee/profile_personal.html", context)

def employee_personal(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        user = Employee.objects.get(pk=id)
        form = EmployeePersonalUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile successfully updated !!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('employee_personal', id=id)
    else:
        user = Employee.objects.get(pk=id)
        form = EmployeePersonalUpdateForm(
            initial={
                'email' : user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'gender' : user.gender,
                'birthday' : user.birthday,
                'c_address': user.c_address,
                'p_address': user.p_address,
                'phone': user.phone,
                'per_email': user.per_email,
                'marital': user.marital,
                'blood': user.blood,
            }
        )
    profile = user
    context = {'profile' : profile, 'form' : form}
    return render(request, "employee/employee_personal.html", context)

def profile_work(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        form = EmployeeWorkUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile successfully updated !!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('profile_work')
    else:
        form = EmployeeWorkUpdateForm(
            initial={
                'emp_id' : request.user.emp_id,
                'emp_status' : request.user.emp_status,
                'department' : request.user.department,
                'manager' : request.user.manager,
                'role' : request.user.role,
                'title': request.user.title,
                'position': request.user.position,
                'experience': request.user.experience,
                'is_active': request.user.is_active,
            }
        )
    profile = request.user
    context = {'profile' : profile, 'form' : form}
    return render(request, "employee/profile_work.html", context)

def employee_work(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        user = Employee.objects.get(pk=id)
        form = EmployeeWorkUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile successfully updated !!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('employee_work', id=id)
    else:
        user = Employee.objects.get(pk=id)
        form = EmployeeWorkUpdateForm(
            initial={
                'emp_id' : user.emp_id,
                'emp_status' : user.emp_status,
                'department' : user.department,
                'manager' : user.manager,
                'role' : user.role,
                'title': user.title,
                'position': user.position,
                'experience': user.experience,
                'is_active': user.is_active,
            }
        )
    profile = user
    context = {'profile' : profile, 'form' : form}
    return render(request, "employee/employee_work.html", context)

def profile_relationship(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if 'new_rel' in request.POST:
        form = RelationshipForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('profile_relationship')

    if 'new_emer' in request.POST:
        form = EmergencyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('profile_relationship')

    new_rel_form = RelationshipForm()
    new_emer_form = EmergencyForm()

    rel = Relationship.objects.all()
    emg = Emergency.objects.all()
    context = {'relation' : rel, 'emergency' : emg, 'new_rel_form' : new_rel_form}
    context['new_emer_form'] = new_emer_form
    return render(request, "employee/profile_relationship.html", context)

def employee_family(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = Employee.objects.get(pk=id)

    if 'new_rel' in request.POST:
        form = RelationshipForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = user
            instance.save()
            return redirect('employee_family', id=id)

    if 'new_emer' in request.POST:
        form = EmergencyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = user
            instance.save()
            return redirect('employee_family', id=id)

    new_rel_form = RelationshipForm()
    new_emer_form = EmergencyForm()

    rel = Relationship.objects.all()
    emg = Emergency.objects.all()
    context = {'relation' : rel, 'emergency' : emg, 'new_rel_form' : new_rel_form, 'profile' : user}
    context['new_emer_form'] = new_emer_form
    print(user)
    return render(request, "employee/employee_family.html", context)

def profile_relationship_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        relation = Relationship.objects.get(pk=id)
        form = RelationshipForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            return redirect('profile_relationship')
        else:
            print('error')
            return redirect('profile_relationship')

    relation = Relationship.objects.get(pk=id)
    form = RelationshipForm(
        initial= {
            "fullname" : relation.fullname,
            "phone" : relation.phone,
            "relationship" : relation.relationship,
        }
    )
    context = {'form' : form}
    return render(request, "employee/profile_relationship_update.html", context)

def employee_relation_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        relation = Relationship.objects.get(pk=id)
        id = relation.employee.id
        form = RelationshipForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            return redirect('employee_family', id=id)
        
    relation = Relationship.objects.get(pk=id)
    id = relation.employee.id
    form = RelationshipForm(
        initial= {
            "fullname" : relation.fullname,
            "phone" : relation.phone,
            "relationship" : relation.relationship,
        }
    )
    context = {'form' : form, 'id' : id}
    return render(request, "employee/employee_relationship_update.html", context)


def profile_emergency_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        relation = Emergency.objects.get(pk=id)
        form = EmergencyForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            return redirect('profile_relationship')
        else:
            print('error')
            return redirect('profile_relationship')

    relation = Emergency.objects.get(pk=id)
    form = EmergencyForm(
        initial= {
            "fullname" : relation.fullname,
            "phone" : relation.phone,
            "relationship" : relation.relationship,
        }
    )
    context = {'form' : form}
    return render(request, "employee/profile_emergency_update.html", context)

def employee_emergency_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        relation = Emergency.objects.get(pk=id)
        id = relation.employee.id
        form = EmergencyForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            return redirect('employee_family', id=id)

    relation = Emergency.objects.get(pk=id)
    id = relation.employee.id
    form = EmergencyForm(
        initial= {
            "fullname" : relation.fullname,
            "phone" : relation.phone,
            "relationship" : relation.relationship,
        }
    )
    context = {'form' : form, 'id' : id}
    return render(request, "employee/employee_emergency_update.html", context)


def profile_relationship_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    relation = Relationship.objects.get(pk=id)
    relation.delete()
    return redirect('profile_relationship')

def employee_relation_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    relation = Relationship.objects.get(pk=id)
    id = relation.employee.id
    relation.delete()
    return redirect('employee_family', id=id)    

def employee_emergency_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    relation = Emergency.objects.get(pk=id)
    id = relation.employee.id
    relation.delete()
    return redirect('employee_family', id=id)    

def profile_emergency_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    emergency = Emergency.objects.get(pk=id)
    emergency.delete()
    return redirect('profile_relationship')

def profile_education(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('profile_education')
        
    educ = Education.objects.all()
    form = EducationForm()
    context = {}
    context['education'] = educ
    context['form'] = form
    return render(request, "employee/profile_education.html", context)

def employee_education(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    profile = Employee.objects.get(pk=id)

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = profile
            instance.save()
            return redirect('employee_education', id=id)
        
    
    educ = Education.objects.all()
    form = EducationForm()
    context = {}
    context['profile'] = profile
    context['education'] = educ
    context['form'] = form
    return render(request, "employee/employee_education.html", context)


def profile_education_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        education = Education.objects.get(pk=id)
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            return redirect('profile_education')
        else:
            print('Error')
            return redirect('profile_education')

    education = Education.objects.get(pk=id)
    form = EducationForm(
        initial= {
            'qualification' : education.qualification,
            'course_name' : education.course_name,
            'course_type' : education.course_type,
            'stream' : education.stream,
            'start' : education.start,
            'end' : education.end,
            'college_name' : education.college_name,
            'university_name' : education.university_name,
        }
    )
    context = {'form' : form}
    return render(request, "employee/profile_education_update.html", context)

def employee_education_update(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        education = Education.objects.get(pk=id)
        id = education.employee.id
        user = Employee.objects.get(pk=id)
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = user
            instance.save()
            return redirect('employee_education', id=id)

    education = Education.objects.get(pk=id)
    id = education.employee.id
    form = EducationForm(
        initial= {
            'qualification' : education.qualification,
            'course_name' : education.course_name,
            'course_type' : education.course_type,
            'stream' : education.stream,
            'start' : education.start,
            'end' : education.end,
            'college_name' : education.college_name,
            'university_name' : education.university_name,
        }
    )
    context = {'form' : form, 'id' : id}
    return render(request, "employee/employee_education_update.html", context)

def profile_education_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    education = Education.objects.get(pk=id)
    education.delete()
    return redirect('profile_education')

def employee_education_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    education = Education.objects.get(pk=id)
    id = education.employee.id
    education.delete()
    return redirect('employee_education', id=id)


def team_view(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    profile = Employee.objects.get(pk=id)
    context = {'profile' : profile}
    return render(request, "employee/team_view.html", context)


def addemp(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    context = {}
    if request.method == 'POST':
        form =  AddEmployeeForm(request.POST)
        role_id = request.POST['role']
        role = Role.objects.get(pk=role_id)
        print(role, role.priority, request.user.role.priority)
        if request.user.role.priority <= role.priority:
            if form.is_valid():
                form.save()
                return render(request, 'employee/addemp.html', {'text' : 'Employee successfully registered!!!'})
            else:
                context = {'form' : form}
        else:
            messages.error(request, 'Sorry, you do not have sufficient permission to add the role you have provided')
            return redirect('addemp')
    else:
        form =  AddEmployeeForm()
        context = {'form' : form}
    return render(request, "employee/addemp.html", context)

def team(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        form =  AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team')

    emp_form = AddEmployeeForm()
    employees = Employee.objects.all().order_by('first_name')
    count = Employee.objects.count
    p = Paginator(employees, 10)
    page = request.GET.get('page')
    employees = p.get_page(page)
    context = {'emps' : employees, 'count' : count}
    context['emp_form'] = emp_form
    return render(request, "employee/team.html", context)

def create(request, id=0):
    if not request.user.is_authenticated:
        return redirect('login_user')

    context = {}
    if 'add_department' in request.POST:
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create')

    if 'add_title' in request.POST:
        form = TitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create')

    if 'add_position' in request.POST:
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create')

    if 'add_role' in request.POST:
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create')

    department = Department.objects.all()
    depart_form = DepartmentForm()
    title = Title.objects.all()
    title_form = TitleForm()
    position = Position.objects.all()
    position_form = PositionForm()
    role = Role.objects.all().order_by('priority')
    role_form = RoleForm()
    context['department'] = department
    context['depart_form'] = depart_form
    context['titles'] = title
    context['title_form'] = title_form
    context['positions'] = position
    context['position_form'] = position_form
    context['roles'] = role
    context['role_form'] = role_form
    
    return render(request, "employee/create.html", context)

def department_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    depart = Department.objects.get(pk=id)
    depart.delete()
    return redirect('create')

def title_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    title = Title.objects.get(pk=id)
    title.delete()
    return redirect('create')

def position_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    position = Position.objects.get(pk=id)
    position.delete()
    return redirect('create')

def role_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    role = Role.objects.get(pk=id)
    role.delete()
    return redirect('create')

def search(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    if 'q' in request.GET:
        q = request.GET['q']
        q = q.capitalize()
        employees = Employee.objects.filter(first_name__contains=q).order_by('first_name')
        if q == '':
            return redirect('team')
    count = Employee.objects.count
    context = {'emps' : employees, 'count' : count}
    return render(request, "employee/team.html", context)

def delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')


    user = Employee.objects.get(pk=id)
    user.delete()

    return redirect('team')

def emp_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')


    if request.method == 'POST':
        emp = Employee.objects.get(pk=id)
        form = EmployeeTeamUpdateForm(request.POST, instance=emp)
    
        if form.is_valid():
            form.save()
            return render(request, "employee/update.html", {'text' : 'Profile successfully updated!!!'})
    else:
        user = Employee.objects.get(pk=id)
        form = EmployeePersonalUpdateForm(
            initial={
                'email' : user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'gender' : user.gender,
                'birthday' : user.birthday,
                'c_address': user.c_address,
                'p_address': user.p_address,
                'phone': user.phone,
                'per_email': user.per_email,
                'marital': user.marital,
                'blood': user.blood,
            }
        )

    
    context = {'form' : form}
    return render(request, "employee/update.html", context)
