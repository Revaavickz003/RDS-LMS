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




class CustomUser(AbstractUser):
    Employee_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=True)
    employee_mobile_number = models.IntegerField(unique=True, null=True, blank=True)
    document = models.FileField(upload_to=user_upload_path, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
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
    company_name = models.CharField(max_length=30)
    company_img = models.ImageField(upload_to='lead_and_customer_companylogo', null=True, blank=True)  # Corrected the upload_to argument
    company_type = models.ForeignKey(OrgType, on_delete=models.CASCADE)
    country = models.ForeignKey(Location, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    reffral_name = models.ForeignKey(LeadTable, on_delete=models.CASCADE)
    business_type = models.CharField(choices=BUSINESS_TYPE_CHOICES, max_length=20)
    products = models.ManyToManyField(ProductTable)
    proposal_amount = models.FloatField()
    finally_budjet = models.FloatField()
    end_of_date = models.DateField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    mail_id = models.EmailField(max_length=50, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    additional_remarks = models.TextField(max_length=100)
    call_back_comments = models.TextField(max_length=100)
    call_back = models.DateField()
    is_customer = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='leads_created', null=True)
    created_date = models.DateField()
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='leads_updated_by', null=True)
    updated_date = models.DateField()

    def __str__(self):
        return self.company_name


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
    


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    timestamp = models.DateTimeField(datetime.datetime.now())
    lable = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
