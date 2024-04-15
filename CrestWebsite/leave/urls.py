from django.urls import path

from . import views

urlpatterns = [
    path("leave", views.leave, name="leave"),
    path("leave/apply", views.leave_apply, name="leave_apply"),
    path("leave/MyLeaves", views.myleaves, name="myleaves"),
    path("leave/MyLeaves/pending", views.myleaves_pending, name="myleaves_pending"),
    path("leave/MyLeaves/approved", views.myleaves_approved, name="myleaves_approved"),
    path("leave/MyLeaves/rejected", views.myleaves_rejected, name="myleaves_rejected"),
    path("leave/leavedetails/<int:id>", views.leavedetails, name="leavedetails"),
    path("leavedelete/<int:id>", views.leavedelete, name="leavedelete"),
    path("leave/EmployeeLeaves", views.emp_leaves, name="emp_leaves"),
    path("leave/EmployeeLeaves/pending", views.leaves_pending, name="leaves_pending"),
    path("leave/EmployeeLeaves/approved", views.leaves_approved, name="leaves_approved"),
    path("leave/EmployeeLeaves/rejected", views.leaves_rejected, name="leaves_rejected"),
    path("leave/leaveapprove/<int:id>", views.leaveapprove, name="leaveapprove"),
    path("leave/leavereject/<int:id>", views.leavereject, name="leavereject"),
    path("leave/leaveunapprove/<int:id>", views.leaveunapprove, name="leaveunapprove"),
]