from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

Gender= (
    ('M', 'Male'),
    ('F', 'Female'),
)

phonetype = (
    ('smart', 'Smart Phone'),
    ('non-smart', 'non-smart Phone'),
)

class SubCategories(models.Model):
    name=models.CharField(max_length=50)

    # def __str__(self):
    #     return self.name

class Category(models.Model):
    name=models.CharField(max_length=20)
    subcategory=models.ManyToManyField(SubCategories,blank=True)

    # def __str__(self):
    #     return self.name

class CustomCategory(models.Model):
    name=models.CharField(max_length=50)

    # def __str__(self):
    #     return self.name

class package_subscriptions(models.Model):
    package_name = models.CharField(max_length=30)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,blank=True,null=True)
    options=models.ManyToManyField(SubCategories,blank=True)
    customcategory=models.ForeignKey(CustomCategory,on_delete=models.PROTECT,blank=True,null=True)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'package_subscriptions'

    # def __str__(self):
    #     return self.package_name


class bussiness_types(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'bussiness_types'

    # def __str__(self):
    #     return self.name


class industries(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'industries'

    # def __str__(self):
    #     return self.id

class users(AbstractUser):
    email = models.EmailField(unique=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    otp=models.IntegerField(blank=True,null=True)
    disabled=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table='users'

    # def __str__(self):
    #     return self.username

class customerfiles(models.Model):
    customer=models.ForeignKey(users,on_delete=models.CASCADE)
    file=models.FileField(upload_to='customer/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table='customer_files'

class group(models.Model):
    name=models.CharField(max_length=50)
    # permissions=models.JSONField(blank=True,null=True)
    create=models.BooleanField(default=False)
    view=models.BooleanField(default=False)
    update=models.BooleanField(default=False)
    delete=models.BooleanField(default=False)
    # premium=models.BooleanField(default=False)
    # staff=models.BooleanField(default=False)
    finance=models.BooleanField(default=False)
    content_editor=models.BooleanField(default=False)


class customers(users):
    company_name = models.CharField(max_length=30,null=True)
    # email = models.EmailField()
    # password = models.CharField(max_length=30)
    company_phone = PhoneNumberField(region='ET',null=True)
    contact_person_first_name = models.CharField(max_length=20,null=True)
    contact_person_phone = PhoneNumberField(region='ET', null=True)
    contact_person_email = models.EmailField(null=True)
    employee_number = models.IntegerField(null=True)
    industry = models.ForeignKey(industries, on_delete=models.PROTECT,null=True, blank=True)
    business_type = models.ForeignKey(bussiness_types, on_delete=models.PROTECT, null=True, blank=True)
    # industry = models.CharField(max_length=191, blank=True, null=True)
    # business_type = models.CharField(max_length=191, blank=True, null=True)
    # files=models.ManyToManyField(customerfiles,on_delete=models.PROTECT)
    # files = models.CharField(max_length=30, null=True)
    usertype = models.CharField(max_length=30, null=True, blank=True)
    email_verified_at = models.DateTimeField(blank=True,null=True)
    # remember_token = models.CharField(max_length=50)
    # created_at = models.DateTimeField(auto_now=True)
    # updated_at = models.DateTimeField(null=True)
    # otp = models.IntegerField(null=True)

    class Meta:
        db_table = 'customers'

class API(models.Model):
    customer=models.ForeignKey(customers,on_delete=models.CASCADE)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table='api'

class Location(models.Model):
    customer=models.ForeignKey(customers,on_delete=models.CASCADE,related_name='customerlocation')
    city=models.CharField(max_length=50,blank=True,null=True)
    subcity=models.CharField(max_length=50,blank=True,null=True)
    woreda=models.CharField(max_length=50,blank=True,null=True)
    zone=models.CharField(max_length=50,blank=True,null=True)
    region=models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table='location'

class staff(users):
    group = models.ForeignKey(group, on_delete=models.SET_NULL, blank=True, null=True)
    salary = models.FloatField(blank=True, null=True)
    department = models.CharField(max_length=191, blank=True, null=True)
    #add fields heres

    class Meta:
        db_table = 'staff'

class subscribers(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    gender = models.CharField(choices=Gender, max_length=15)
    age = models.IntegerField()
    industry = models.ForeignKey(industries, on_delete=models.PROTECT)
    phone = PhoneNumberField(region='ET',)
    phonetype = models.CharField(choices=phonetype, max_length=15, default='smart')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return '{} {}'.format(first_name,last_name)

    class Meta:
        db_table = 'subscribers'

class customer_phones(models.Model):
    customer = models.ForeignKey(users, on_delete=models.PROTECT,related_name='customer_phonebook')
    # name = models.CharField(max_length=30)
    phone = PhoneNumberField(region='ET')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'customer_phones'

    def __str__(self):
        return self.customer.username


class personal_access_tokens(models.Model):
    tokenable_type = models.CharField(max_length=30)
    tokenable_id = models.IntegerField()
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=50)
    abilities = models.CharField(max_length=30)
    last_used_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'personal_access_tokens'

class password_resets(models.Model):
    email = models.ForeignKey(users, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'password_resets'

class services(models.Model):
    image=models.ImageField(upload_to='services',blank=True,null=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    meta=models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name


# class bussiness_types(models.Model):
#     name = models.CharField(max_length=20)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_created=True)
#     updated_at = models.DateTimeField(null=True)

#     class Meta:
#         db_table = 'bussiness_types'

# class industries(models.Model):
#     name = models.CharField(max_length=20)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_created=True)
#     updated_at = models.DateTimeField(null=True)

#     class Meta:
#         db_table = 'industries'

class customer_subscription_data(models.Model):
    customer_id = models.ForeignKey(users,on_delete=models.CASCADE)
    package_id = models.ForeignKey(package_subscriptions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'customer_subscription_data'

class customer_contents(models.Model):
    customer_id = models.ForeignKey(users, on_delete=models.PROTECT)
    service_id = models.ForeignKey(services, on_delete=models.PROTECT)
    campaign_name = models.CharField(max_length=20)
    message = models.TextField()
    ref_number = models.CharField(max_length=20)
    sender = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'customer_contents'

    def __str__(self):
        return self.campaign_name
