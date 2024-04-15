from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Leave, Remaining_Leaves
from .forms import LeaveCreationForm
import datetime

def leave(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leaves = Remaining_Leaves.objects.get(user=request.user)
    return render(request, "leave/leave.html", {'leaves' : leaves})

def leave_apply(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    if request.method == 'POST':
        count = 0
        startdate = request.POST['startdate']
        startdate = startdate.split("/")
        enddate = request.POST['enddate']
        enddate = enddate.split("/")
        start_date = datetime.date(int(startdate[2]), int(startdate[0]), int(startdate[1]))
        end_date = datetime.date(int(enddate[2]), int(enddate[0]), int(enddate[1]))
        delta = datetime.timedelta(days=1)

        while start_date <= end_date:
            day = start_date.weekday()
            start_date += delta
            if (day == 5 or day == 6):
                continue
            else:
                count += 1

        id = request.user.id
        rem_leaves = Remaining_Leaves.objects.get(user=request.user)
        if request.POST['leavetype'] == 'CASUAL':
            if count > rem_leaves.casual_leave:
                messages.success(request,'Remaining casual leave(s) = {0}, but applied number of leave(s) = {1}'.format(rem_leaves.casual_leave, count),extra_tags = 'alert alert-danger alert-dismissible show')
                return redirect('leave_apply')
        elif request.POST['leavetype'] == 'SICK':
            if count > rem_leaves.sick_leave:
                messages.success(request,'Remaining sick leave(s) = {0}, but applied number of leave(s) = {1}'.format(rem_leaves.sick_leave, count),extra_tags = 'alert alert-danger alert-dismissible show')
                return redirect('leave_apply')

        form = LeaveCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.user
            instance.user = user
            instance.save()
            messages.success(request,'Leave Request Sent, wait for Manager\'s response',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('leave_apply')
            
        messages.error(request,'Failed to Request a Leave, please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
        return redirect('leave_apply')

    form = LeaveCreationForm()
    context = {'form' : form}
    return render(request, "leave/leave_creation.html", context)

def myleaves(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = request.user
    leaves = Leave.objects.filter(user=user)
    dataset = dict()
    dataset['leave_list'] = leaves
    dataset['all'] = True
    return render(request,'leave/myleaves.html',dataset)

def myleaves_pending(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = request.user
    leaves = Leave.objects.filter(user=user, status='Pending')
    dataset = dict()
    dataset['leave_list'] = leaves
    dataset['pending'] = True
    return render(request,'leave/myleaves.html',dataset)

def myleaves_approved(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = request.user
    leaves = Leave.objects.filter(user=user, status='Approved')
    dataset = dict()
    dataset['leave_list'] = leaves
    dataset['approved'] = True
    return render(request,'leave/myleaves.html',dataset)

def myleaves_rejected(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = request.user
    leaves = Leave.objects.filter(user=user, status='Rejected')
    dataset = dict()
    dataset['leave_list'] = leaves
    dataset['rejected'] = True
    return render(request,'leave/myleaves.html',dataset)

def leavedetails(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    leave = Leave.objects.get(pk=id)
    context = {'leave' : leave}

    return render(request,'leave/leavedetails.html', context)

def leavedelete(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leave = Leave.objects.get(pk=id)
    # leave = get_object_or_404(Leave, id = id)
    leave.delete()

    return redirect('leave')


def emp_leaves(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leaves = Leave.objects.all()
    context = {'leaves' : leaves, 'all' : True}

    return render(request, "leave/emp_leaves.html", context)

def leaves_pending(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leaves = Leave.objects.filter(status='Pending')
    context = {'leaves' : leaves, 'pending' : True}

    return render(request, "leave/emp_leaves.html", context)

def leaves_approved(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leaves = Leave.objects.filter(status='Approved')
    context = {'leaves' : leaves, 'approved' : True}

    return render(request, "leave/emp_leaves.html", context)

def leaves_rejected(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    leaves = Leave.objects.filter(status='Rejected')
    context = {'leaves' : leaves, 'rejected' : True}

    return render(request, "leave/emp_leaves.html", context)

def leaveapprove(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    leave = Leave.objects.get(pk=id)
    u_id = leave.user.id
    rem_leaves = Remaining_Leaves.objects.get(pk=u_id)
    count = leave.leave_days
    if leave.leavetype == 'CASUAL':
        if count > rem_leaves.casual_leave:
            messages.success(request,'Remaining casual leave(s) = {0}, but applied number of leave(s) = {1}'.format(rem_leaves.casual_leave, count),extra_tags = 'alert alert-danger alert-dismissible show')
            return redirect('leavedetails', id)
    elif leave.leavetype == 'SICK':
        if count > rem_leaves.sick_leave:
            messages.success(request,'Remaining sick leave(s) = {0}, but applied number of leave(s) = {1}'.format(rem_leaves.sick_leave, count),extra_tags = 'alert alert-danger alert-dismissible show')
            return redirect('leavedetails', id)
    leave.approve_leave

    while count:
        count -= 1
        if leave.leavetype == 'CASUAL':
            rem_leaves.deduct_casual()
        elif leave.leavetype == 'SICK':
            rem_leaves.deduct_sick()

    messages.success(request,'Leave successfully approved for {0}'.format(leave.user),extra_tags = 'alert alert-success alert-dismissible show')

    return redirect('leavedetails', id)

def leavereject(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    leave = Leave.objects.get(pk=id)
    leave.reject_leave

    messages.success(request,'Leave successfully rejected for {0}'.format(leave.user),extra_tags = 'alert alert-success alert-dismissible show')

    return redirect('leavedetails', id)

def leaveunapprove(request, id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    leave = Leave.objects.get(pk=id)
    leave.unapprove_leave
    u_id = leave.user.id
    rem_leaves = Remaining_Leaves.objects.get(pk=u_id)
    count = leave.leave_days

    while count:
        count -= 1
        if rem_leaves.casual_leave > 20:
            continue
        if rem_leaves.sick_leave > 5:
            continue

        if leave.leavetype == 'CASUAL':
            rem_leaves.add_casual()
        elif leave.leavetype == 'SICK':
            rem_leaves.add_sick()
        

    messages.success(request,'Leave successfully unapproved for {0}'.format(leave.user),extra_tags = 'alert alert-success alert-dismissible show')

    return redirect('leavedetails', id)