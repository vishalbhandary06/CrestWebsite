from cProfile import label
from django.contrib import admin

# Register your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField

# Create your models here.

class EmployeeManager(BaseUserManager):
    def create_user(self, email, first_name, emp_id, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have an Name")
        if not emp_id:
            raise ValueError("Users must have an Employee ID")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            emp_id = emp_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, emp_id, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            emp_id = emp_id,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Department(models.Model):
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name='Created',auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated',auto_now=True)


    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name','created']
    
    def __str__(self):
        return self.name

class Role(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    priority = models.CharField(max_length=125,null=True,blank=True)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name='Created',auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated',auto_now=True)


    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name','created']


    def __str__(self):
        return self.name

class Title(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name='Created',auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated',auto_now=True)


    class Meta:
        verbose_name = 'Job Title'
        verbose_name_plural = 'Job Titles'
        ordering = ['name','created']


    def __str__(self):
        return self.name

class Position(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name='Created',auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated',auto_now=True)


    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['name','created']


    def __str__(self):
        return self.name



GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

ROLE = [
    ('Admin', 'Admin'),
    ('H.R', 'H.R'),
    ('Manager', 'Manager'),
    ('Employee', 'Employee'),
]

BLOOD_TYPE = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

STATUS = [
    ('Probationary', 'Probationary'),
    ('Contract', 'Contract'),
    ('Permanent', 'Permanent'),
    ('Resigned', 'Resigned'),
]

MARITAL_STATUS=[
    ('Single', 'Single'),
    ('Married', 'Married'),
]

class Employee(AbstractBaseUser):
    # Personal Info
    email           = models.EmailField(max_length=254, verbose_name='Official Email', unique=True)
    first_name      = models.CharField(max_length=50, verbose_name="First Name")
    last_name       = models.CharField(max_length=50, verbose_name="Last Name",blank=True)
    gender          = models.CharField(max_length=10, verbose_name="Gender", choices=GENDER,blank=True)
    birthday        = models.DateField(verbose_name="Date of Birth",null=True, blank=True, help_text="MM/DD/YYYY")
    phone           = models.CharField(max_length=15, verbose_name="Phone Number", blank=True)
    blood           = models.CharField(verbose_name="Blood Type", choices=BLOOD_TYPE,blank=True, max_length=10)
    marital         = models.CharField(verbose_name="Marital Status", choices=MARITAL_STATUS,blank=True, max_length=10)
    per_email       = models.EmailField(max_length=254, verbose_name='Personal Email', unique=True, blank=True, null=True)
    c_address       = models.CharField(max_length=1000, verbose_name="Current Address", null=True, blank=True)
    p_address       = models.CharField(max_length=1000, verbose_name="Permanent Address", null=True, blank=True)
    # Work Info
    emp_id          = models.CharField(max_length=15, verbose_name="Employee ID", unique=True)
    date_joined     = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    emp_status      = models.CharField(verbose_name="Employee Status", choices=STATUS,blank=False, max_length=20)
    department      = models.ForeignKey(Department,verbose_name ='Department',on_delete=models.SET_NULL,null=True,default=None)
    manager         = models.ForeignKey(to="self",verbose_name ='Reporting Manager',on_delete=models.SET_NULL,null=True,default=None, blank=True)
    role            = models.ForeignKey(Role,verbose_name ='Role',on_delete=models.SET_NULL,null=True,default=None)
    title           = models.ForeignKey(Title,verbose_name ='Job Title',on_delete=models.SET_NULL,null=True,default=None)
    position        = models.ForeignKey(Position,verbose_name ='Position',on_delete=models.SET_NULL,null=True,default=None)
    experience      = models.CharField(max_length=10, verbose_name="Work Experience", null=True, blank=True)
    is_active       = models.BooleanField(verbose_name="Active",default=True)
    # Misc Info
    last_login      = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin        = models.BooleanField(verbose_name="Admin",default=False)
    is_staff        = models.BooleanField(verbose_name="Staff",default=False)
    is_superuser    = models.BooleanField(verbose_name="Superuser",default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'emp_id',]

    objects = EmployeeManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Employee._meta.fields]

    def relation(self):
        return Employee.objects.select_related('relationship').all()

class Emergency(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    EMERGENCY_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )


    # access table: employee.emergency_set.
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    fullname = models.CharField(('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    phone    = models.CharField(max_length=15, verbose_name="Phone Number", blank=False)
    relationship = models.CharField(('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default=FATHER,choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)


    created = models.DateTimeField(verbose_name=('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']


    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name + " - " + self.relationship

class Relationship(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    EMERGENCY_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )


    # access table: employee.emergency_set.
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    fullname = models.CharField(('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    phone    = models.CharField(max_length=15, verbose_name="Phone Number", blank=False)
    relationship = models.CharField(('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default=FATHER,choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)


    created = models.DateTimeField(verbose_name=('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationship'
        ordering = ['-created']


    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name + " - " + self.relationship


class Education(models.Model):
    GRADUATION = 'Graduation'
    POST_GRADUATION = 'Post Graduation'
    DOCTORATE = 'Doctorate'
    DIPLOMA = 'Diploma'
    PRE_UNIVERSITY = 'Pre University'
    OTHER_EDUCATION = 'Other Education'
    CERTIFICATION = 'Certification'

    QUAL_TYPE = (
        (GRADUATION, 'Graduation'),
        (POST_GRADUATION, 'Post Graduation'),
        (DOCTORATE, 'Doctorate'),
        (DIPLOMA,'Diploma'),
        (PRE_UNIVERSITY,'Pre University'),
        (OTHER_EDUCATION,'Other Education'),
        (CERTIFICATION,'Certification'),
    )

    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'
    CERTIFICATION = 'Certification'
    CORRESPONDENCE = 'Correspondence'

    COURSE_TYPE = (
        (FULL_TIME,'Full Time'),
        (PART_TIME,'Part Time'),
        (CORRESPONDENCE, 'Correspondence'),
        (CERTIFICATION,'Certification'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    qualification = models.CharField(verbose_name="Qualificayion Type", choices=QUAL_TYPE,blank=True, max_length=20)
    course_name = models.CharField(verbose_name="Course Name", max_length=50)
    course_type = models.CharField(verbose_name="Course Type", choices=COURSE_TYPE,blank=True, max_length=20)
    stream = models.CharField(verbose_name="Stream", max_length=50)
    start = models.DateField(verbose_name="Course Start Date", help_text="MM/DD/YYYY")
    end = models.DateField(verbose_name="Course Start End", help_text="MM/DD/YYYY")
    college_name = models.CharField(verbose_name="College Name", max_length=50)
    university_name = models.CharField(verbose_name="University Name", max_length=50)

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name + " - " + self.course_name