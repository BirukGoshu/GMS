from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from UserManagment.models import users, customers, services,Gender,phonetype, industries, bussiness_types, Location

# Create your models here.
# class CustomerPhone(models.Model):
#     customer_id = models.ForeignKey()
class SMS(models.Model):
    Recipient = PhoneNumberField(region='ET', blank=True)
    Message = models.TextField(max_length=250)
    # creator = models.ForeignKey(users, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'SMS'

# class SMStype(models.Model):
#     name=models.CharField(max_length=20)
#     description=models.TextField(null=True,blank=True)

class all_campaigns(models.Model):
    date_tobe_sent = models.DateTimeField()
    # link = models.CharField(max_length=50)
    sender = models.CharField(max_length=50)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    phones = models.FileField(upload_to='content/Phones',blank=True, null = True)
    customer = models.ForeignKey(customers, on_delete=models.PROTECT, null=True,blank=True)
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    message = models.TextField()
    totalphones=models.IntegerField(blank=True,null=True)
    # other = models.CharField(max_length=20)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return 'sender-{} message-{}'.format(self.sender, self.message)


    class Meta:
        db_table = 'all_campaigns'

class template(models.Model):
    name=models.CharField(max_length=20)
    text=models.TextField(null=True)
    description=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table='templates'

class only_data_campaigns(models.Model):
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    customer=models.ForeignKey(customers,models.PROTECT)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    minage = models.IntegerField(blank=True, null=True)
    maxage = models.IntegerField(blank=True, null=True)
    # minsmsexpected=models.IntegerField(blank=True, null=True)
    # maxsmsexpected=models.IntegerField(blank=True, null=True)
    message=models.TextField(blank=True,null=True)
    # expected_delivery = models.CharField(max_length=191, null=True)
    gender = models.CharField(choices=Gender, max_length=15, blank=True, null=True)
    phone_type = models.CharField(choices=phonetype, max_length=15, blank=True, null=True)
    date_tobe_sent = models.DateTimeField(null=True)
    # location = models.CharField(max_length=191, null=True)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,blank=True,null=True)
    totalphones=models.IntegerField(blank=True,null=True)
    #occupation = models.CharField(max_length=191, null=True)
    industry = models.ForeignKey(industries,on_delete=models.SET_NULL,blank=True,null=True)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'only_data_campaigns'

    def __str__(self):
        return self.campaign_name

class all_campaign_whitelist(models.Model):
    date_tobe_sent = models.DateTimeField()
    sender = models.CharField(max_length=50)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    # phones = models.FileField(upload_to='all_campaign_whitelist/Phones/', blank=True, null = True)
    customer = models.ForeignKey(customers, on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    message = models.TextField()
    totalphones=models.IntegerField(blank=True,null=True)
    # minage = models.IntegerField(blank=True, null=True)
    # maxage = models.IntegerField(blank=True, null=True)
    # minsmsexpected=models.IntegerField(blank=True, null=True)
    # maxsmsexpected=models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=Gender, max_length=15, blank=True, null=True)
    phone_type = models.CharField(choices=phonetype, max_length=15, blank=True, null=True)
    # date_tobe_sent = models.DateTimeField(null=True)
    # location = models.CharField(max_length=191, blank=True, null=True)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,blank=True,null=True)
    #occupation = models.CharField(max_length=191, blank=True, null=True)
    industry = models.ForeignKey(industries,on_delete=models.SET_NULL,blank=True,null=True)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return 'sender-{} message-{}'.format(self.sender, self.message)

    class Meta:
        db_table='whitelist_all_campaign'

class ordinarysurvey(models.Model):
    sender = models.CharField(max_length=50)
    phones = models.FileField(upload_to='survey/Phones/', blank=True, null = True)
    customer = models.ForeignKey(customers, on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    message = models.TextField()
    totalphones=models.IntegerField(blank=True,null=True)
    # minage = models.IntegerField(blank=True, null=True)
    # maxage = models.IntegerField(blank=True, null=True)
    # minsmsexpected=models.IntegerField(blank=True, null=True)
    # maxsmsexpected=models.IntegerField(blank=True, null=True)
    # gender = models.CharField(choices=Gender, max_length=15, blank=True, null=True)
    # phone_type = models.CharField(choices=phonetype, max_length=15, blank=True, null=True)
    date_tobe_sent = models.DateTimeField(blank=True,null=True)
    # location = models.CharField(max_length=191, blank=True, null=True)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,blank=True,null=True)
    industry = models.ForeignKey(industries,on_delete=models.SET_NULL,blank=True,null=True)
    # occupation = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)

    class Meta:
        db_table='ordinarysurvey'

class demographicsurvey(models.Model):
    sender = models.CharField(max_length=50)
    # phones = models.FileField(upload_to='survey/Phones/', blank=True, null = True)
    customer = models.ForeignKey(customers, on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    message = models.TextField()
    totalphones=models.IntegerField(blank=True,null=True)
    # minage = models.IntegerField(blank=True, null=True)
    # maxage = models.IntegerField(blank=True, null=True)
    # minsmsexpected=models.IntegerField(blank=True, null=True)
    # maxsmsexpected=models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=Gender, max_length=15, blank=True, null=True)
    phone_type = models.CharField(choices=phonetype, max_length=15, blank=True, null=True)
    date_tobe_sent = models.DateTimeField(blank=True,null=True)
    # location = models.CharField(max_length=191, blank=True, null=True)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,blank=True,null=True)
    #occupation = models.CharField(max_length=191, blank=True, null=True)
    industry = models.ForeignKey(industries,on_delete=models.SET_NULL,blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)

    class Meta:
        db_table='demographicsurvey'

class internalsurvey(models.Model):
    sender = models.CharField(max_length=50)
    # phones = models.FileField(upload_to='survey/Phones/', blank=True, null = True)
    customer = models.ForeignKey(customers, on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(services, on_delete=models.PROTECT, null=True)
    campaign_name = models.CharField(max_length=191, null=True)
    ref_number = models.CharField(max_length=191, null=True)
    # type=models.ForeignKey(SMStype,on_delete=models.SET_NULL,blank=True,null=True)
    message = models.TextField()
    totalphones=models.IntegerField(blank=True,null=True)
    # minage = models.IntegerField(blank=True, null=True)
    # maxage = models.IntegerField(blank=True, null=True)
    # minsmsexpected=models.IntegerField(blank=True, null=True)
    # maxsmsexpected=models.IntegerField(blank=True, null=True)
    # gender = models.CharField(choices=Gender, max_length=15, blank=True, null=True)
    # phone_type = models.CharField(choices=phonetype, max_length=15, blank=True, null=True)
    # date_tobe_sent = models.DateTimeField(null=True)
    # location = models.CharField(max_length=191, blank=True, null=True)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,blank=True,null=True)
    industry = models.ForeignKey(industries,on_delete=models.SET_NULL,blank=True,null=True)
    # occupation = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    approved = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status=models.CharField(default='created',max_length=20)

    class Meta:
        db_table='internalsurvey'

class BulkSMS(models.Model):
    phones = models.FileField(upload_to='UserManagment/uploads/Phones')
    message = models.TextField()
    # creator = models.ForeignKey(users, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'BulkSMS'

class wallet(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    checkoutdata=models.JSONField(blank=True,null=True)
    paymentdata=models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'wallet'

    def __str__(self):
        return self.user.username

class userwallet(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)







