from django.db import models
from django.db.models.fields.related import ForeignKey
from .manager import LeaveManager
from employee.models import Employee
import datetime
from django.utils import timezone

class Remaining_Leaves(models.Model):
    user            = ForeignKey(Employee,on_delete=models.CASCADE,default=1)
    casual_leave    = models.IntegerField(default=20)
    sick_leave      = models.IntegerField(default=5)

    def __str__(self):
        return str(self.user)

    def deduct_casual(self):
        self.casual_leave -= 1
        self.save()

    def deduct_sick(self):
        self.sick_leave -= 1
        self.save()

    def add_casual(self):
        self.casual_leave += 1
        self.save()

    def add_sick(self):
        self.sick_leave += 1
        self.save()

    def reset_casual(self):
        self.casual_leave = 20
        self.save()

    def reset_sick(self):
        self.sick_leave = 5
        self.save()


LEAVE_TYPE = (
('SICK','Sick Leave'),
('CASUAL','Casual Leave'),
('OPTIONAL','Optional Leave'),
)

class Leave(models.Model):
    user = ForeignKey(Employee,on_delete=models.CASCADE,default=1)
    startdate = models.DateField(verbose_name='Start Date',help_text='leave start date is on ..',null=True,blank=False)
    enddate = models.DateField(verbose_name='End Date',help_text='coming back on ...',null=True,blank=False)
    leavetype = models.CharField(choices=LEAVE_TYPE,max_length=25,default=LEAVE_TYPE[0],null=True,blank=False)
    reason = models.CharField(verbose_name='Reason for Leave',max_length=255,help_text='add additional information for leave',null=True,blank=True)
    casual_leave    = 20
    optional_leave  = 6
    sick_leave      = 5
    status = models.CharField(max_length=12,default='Pending')
    is_approved = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LeaveManager()

    class Meta:
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'

    def __str__(self):
        return ('{0} - {1}'.format(self.leavetype,self.user))

    @property
    def leave_days(self):
        count = 0
        startdate = self.startdate
        enddate = self.enddate
        start_date = datetime.date(startdate.year, startdate.month, startdate.day)
        end_date = datetime.date(enddate.year, enddate.month, enddate.day)
        delta = datetime.timedelta(days=1)

        while start_date <= end_date:
            day = start_date.weekday()
            start_date += delta
            if (day == 5 or day == 6):
                continue
            else:
                count += 1
            
        return count


    @property
    def leave_approved(self):
        return self.is_approved == True

    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'Approved'
            self.save()

    @property
    def reject_leave(self):
        if self.leave_approved or not self.leave_approved:
            self.is_approved = False
            self.status = "Rejected"
            self.save()

    @property
    def unapprove_leave(self):
        if self.leave_approved:
            self.is_approved = False
            self.status = "Pending"
            self.save()

    def c_leave(self):
        self.casual_leave -= 1

    def o_leave(self):
        self.optional_leave -= 1

    def s_leave(self):
        self.sick_leave -= 1
        
        
NOTIFICATION_TYPE = (
(1,'Leave Approved'),
(2,'Leave Rejected'),
(3,'Leave Unapproved'),
)
class Notification(models.Model):
    notification_type = models.CharField(choices=NOTIFICATION_TYPE,max_length=25,default=NOTIFICATION_TYPE[0],null=True,blank=False)
    to_user = models.ForeignKey(Employee, related_name='notification_to',on_delete=models.CASCADE)
    from_user = models.ForeignKey(Employee, related_name='notification_from',on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone)
    user_has_seen = models.BooleanField(default=False)