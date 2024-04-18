import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, Permission

def user_upload_path(instance, username):
    return f'Employee/{instance.username}/Documents/{username}'

def user_image_upload_path(instance, username):
    return f'Employee/{instance.username}/{username}'

def lead_and_customer_companylogo(instance, org_name):
    return f'Leads and Customer/{instance.org_name}/{org_name}'

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='roles_created')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='roles_updated')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=True)
    employee_mobile_number = models.IntegerField(unique=True, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, blank=True, null=True)
    document = models.FileField(upload_to=user_upload_path, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, blank=True, null=True)
    parent_number = models.IntegerField(null=True, blank=True)
    employee_photo = models.ImageField(upload_to=user_image_upload_path, null=True, blank=True)
    qualification = models.CharField(default='', max_length=10, null=True, blank=True)
    company_email =  models.EmailField(max_length=254, blank=True)
    date_of_join = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_trainee = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_teamlead = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    address = models.TextField(null=True, blank=True)


    # Custom relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,  # Make the fields optional if needed
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,  # Make the fields optional if needed
    )

    def __str__(self):
        return self.username

class EmployeeStatus(models.Model):
    STATUS_CHOICES = (
        ('Working Day', 'Working Day'),
        ('Work From Home', 'Work From Home'),
        ('Leave', 'Leave'),
    )
    employee_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_status_created')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_status_updated')
    updated_date = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return  f"{self.employee_id}-{self.status}"

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_created')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_updated')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class Position(models.Model):
    Position_Name = models.CharField(max_length=10)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='positions_created')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='positions_updated')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Position_Name



class ClientType(models.Model):
    type_name = models.CharField(max_length=50, null=False, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='client_types_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='client_types_updated')

    def __str__(self):
        return self.type_name


class ProjectStatus(models.Model):
    status_name = models.CharField(max_length=50)
    status_level = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='project_statuses_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='project_statuses_updated')
        
    def __str__(self):
        return self.status_name

class Ticket(models.Model):
    STATUS_CHOICES = (('Open', 'Open'), ('In Progress', 'In Progress'), ('On Hold', 'On Hold'), ('Closed', 'Closed'))
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')  
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True) 
    client_details = models.ForeignKey(ClientType, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    issue_title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    resolution = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.issue_title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments')
    text = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='ticket_files/', verbose_name='Upload Files')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='uploaded_attachments')
    date_uploaded = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user_id = models.IntegerField(default=-1)  # -1 for admin notification
    notification_text = models.TextField()
    notification_sent = models.BooleanField(default=False)

class OrgType(models.Model):
    org_type = models.CharField(max_length=30)

    def __str__(self):
        return self.org_type

class Location(models.Model):
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.location

class City(models.Model):
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city
    
class OrgName(models.Model):
    Org_Name = models.CharField(max_length=25)

    def __str__(self):
        return self.Org_Name
    
class ProductTable(models.Model):
    Product_Name = models.CharField(max_length=25)

    def __str__(self):
        return self.Product_Name

@receiver(post_save, sender=ProductTable)
def create_default_products(sender, instance, created, **kwargs):
    if created:
        default_products = ['Branding', 'Design', 'SMM', 'Website', 'CRM', 'Google Adds', 'Meta Adds', 'Video Editing', 'Marketing']
        for product_name in default_products:
            ProductTable.objects.get_or_create(Product_Name=product_name)

class LeadTable(models.Model):
    Lead_Name =  models.CharField(max_length=25)

    def __str__(self):
        return self.Lead_Name
    
class Lead(models.Model):
    FRESH = 'Fresh'
    CALL_BACK = 'Call Back'
    DO_NOT_DISTURB = 'Do Not Disturb'
    FOLLOW_UP = 'Follow up'
    PROPOSED = 'Proposed'
    HOLD = 'Hold'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (FRESH, 'Fresh'),
        (CALL_BACK, 'Call Back'),
        (DO_NOT_DISTURB, 'Do Not Disturb'),
        (FOLLOW_UP, 'Follow up'),
        (PROPOSED, 'Proposed'),
        (HOLD, 'Hold'),
        (CLOSED, 'Closed'),
    ]

    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    ONE_TIME = 'One Time'
    RECURRING = 'Recurring'
    BUSINESS_TYPE_CHOICES = [
        (ONE_TIME, 'One Time'),
        (RECURRING, 'Recurring'),
    ]

    client_name = models.CharField(max_length=20)
    client_number = models.IntegerField()
    org_name = models.CharField(max_length=30)
    org_img = models.ImageField(upload_to='lead_and_customer_companylogo', null=True, blank=True)  # Corrected the upload_to argument
    org_type = models.ForeignKey(OrgType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    lead_name = models.ForeignKey(LeadTable, on_delete=models.CASCADE)
    business_type = models.CharField(choices=BUSINESS_TYPE_CHOICES, max_length=20)
    products = models.ManyToManyField(ProductTable)
    amount = models.FloatField()
    end_of_date = models.DateField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    mail_id = models.EmailField(max_length=50, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    comment = models.TextField(max_length=100)
    remarks = models.TextField(max_length=100)
    follow_up = models.DateField()
    is_customer = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='leads_created', null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='leads_updated_by', null=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.org_name


def generate_customer_id():
    last_customer = customertable.objects.order_by('-id').first()
    if last_customer:
        last_id = int(last_customer.customer_id[7:]) 
        new_id = last_id + 1
    else:
        new_id = 1
    return f'RDSCUS{new_id:04d}'

class customertable(models.Model):
    FRESH = 'Fresh'
    CALL_BACK = 'Call Back'
    DO_NOT_DISTURB = 'Do Not Disturb'
    FOLLOW_UP = 'Follow up'
    PROPOSED = 'Proposed'
    HOLD = 'Hold'
    CLOSED = 'Closed'
    STATUS_CHOICES = [
        (FRESH, 'Fresh'),
        (CALL_BACK, 'Call Back'),
        (DO_NOT_DISTURB, 'Do Not Disturb'),
        (FOLLOW_UP, 'Follow up'),
        (PROPOSED, 'Proposed'),
        (HOLD, 'Hold'),
        (CLOSED, 'Closed'),
    ]

    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    ONE_TIME = 'One Time'
    RECURRING = 'Recurring'
    BUSINESS_TYPE_CHOICES = [
        (ONE_TIME, 'One Time'),
        (RECURRING, 'Recurring'),
    ]
    customer_id = models.CharField(max_length=10, default=generate_customer_id, unique=True)
    client_name = models.CharField(max_length=20)
    client_number = models.IntegerField()
    org_name = models.CharField(max_length=30)
    org_img = models.ImageField(upload_to= lead_and_customer_companylogo, null=True, blank=True)
    org_type = models.ForeignKey(OrgType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    lead_name = models.ForeignKey(LeadTable, on_delete=models.CASCADE)
    business_type = models.CharField(choices=BUSINESS_TYPE_CHOICES, max_length=20)
    products = models.ManyToManyField(ProductTable, blank=True)
    amount = models.FloatField()
    end_of_date = models.DateField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    mail_id = models.EmailField(max_length=50, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    comment = models.TextField(max_length=100)
    remarks = models.TextField(max_length=100)
    follow_up = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='custoner_created', null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='customer_updated_by', null=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.org_name
    
class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    team_icon = models.ImageField(upload_to='Team Icon', null=True, blank=True)
    members = models.ManyToManyField(CustomUser, related_name='teams')
    deportment = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='teams_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='teams_updated')

    def __str__(self):
        return self.team_name
    
class Client(models.Model):
    client_id =  models.CharField(max_length=20)
    client_detrails = models.ForeignKey(Lead, on_delete=models.CASCADE)
    client_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Customer : {self.client_id} -- {self.client_detrails.org_name}" 


class TasksheetTable(models.Model):
    ASSIGNED = 'Assigned'
    ON_PROCESS = 'On Process'
    HOLD = 'Hold'
    DROPPED = 'Dropped'
    COMPLETED = 'Completed'
    REJECTED = 'Rejected'
    TASK_STATUS_CHOICES = [
        (ASSIGNED, 'Assigned'),
        (ON_PROCESS, 'On Process'),
        (HOLD, 'Hold'),
        (DROPPED, 'Dropped'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
    ]
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    date = models.DateField(null=False, blank=False)
    client = models.CharField(max_length=100)
    types = models.CharField(max_length=50)
    task = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_assigned_to')
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_assigned_by')
    status = models.CharField(choices=TASK_STATUS_CHOICES, max_length=20, default=ASSIGNED)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default=MEDIUM)
    expected_time =  models.IntegerField(default=60)
    start_time = models.TimeField(null=True, blank=True)
    endtime_time = models.TimeField(null=True, blank=True)
    time_taken = models.IntegerField(default=0)
    remarks = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assigned_by} - {self.assigned_to}"


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    timestamp = models.DateTimeField(auto_now_add=True)
    lable = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
