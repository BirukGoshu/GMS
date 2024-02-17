import random, math, requests, urllib.parse, ssl
from .models import *
from SMS.models import wallet,userwallet,all_campaigns,only_data_campaigns,all_campaign_whitelist,ordinarysurvey
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from GMS.settings import ozekihttpurl, ozekiusername, ozekipassword
from django.contrib.auth.models import auth
from .exceptions import ValidationErrors
import base64,mimetypes
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    #username = serializers.CharField()
    #email = serializers.CharField()
    def create(self, validated_data):
        pass
    def update(self, validated_data):
        pass

class logoutserializer(serializers.Serializer):
    def create(self, validated_data):
        pass
    def update(self, validated_data):
        pass

class GroupSerializer(serializers.ModelSerializer):
    permissions=serializers.SerializerMethodField()
    # create=serializers.BooleanField(write_only=True,required=False)
    # view=serializers.BooleanField(write_only=True,required=False)
    # update=serializers.BooleanField(write_only=True,required=False)
    # delete=serializers.BooleanField(write_only=True,required=False)

    def get_permissions(self,obj):
        return {
            'create':obj.create,
            'view':obj.view,
            'update':obj.update,
            'delete':obj.delete,
        }

    class Meta:
        model=group
        fields='__all__'

    def create(self,validated_data):
        if 'permissions' in self.context['request'].data and self.context['request'].data['permissions'] is not None:
            permission=self.context['request'].data['permissions']
            validated_data['create']=permission['create']
            validated_data['view']=permission['view']
            validated_data['update']=permission['update']
            validated_data['delete']=permission['delete']
        g=group.objects.create(**validated_data)
        return g

    def update(self,instance,validated_data):
        if 'permissions' in self.context['request'].data and self.context['request'].data['permissions'] is not None:
            permission=self.context['request'].data['permissions']
            validated_data['create']=permission['create']
            validated_data['view']=permission['view']
            validated_data['update']=permission['update']
            validated_data['delete']=permission['delete']
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class APISerializer(serializers.ModelSerializer):
    customer=serializers.CharField(read_only=True)

    class Meta:
        model=API
        fields='__all__'

    def create(self,validated_data):
        if self.context['request'].user.is_superuser:
            validated_data['customer']=customers.objects.get(id=self.context['request'].data['customer'])
        else:
            validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        api=API.objects.create(**validated_data)
        return api

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Location
        fields='__all__'

class CustomerFilesSerialzier(serializers.ModelSerializer):

    class Meta:
        model=customerfiles
        fields='__all__'

class CustomerPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model=customer_phones
        fields='__all__'

class CustomersSerializer(serializers.ModelSerializer):
    customerphonebook=CustomerPhoneSerializer(read_only=True,many=True,source='customer_phonebook')
    customerfiles=CustomerFilesSerialzier(many=True,read_only=True,source='customerfiles_set')
    api=APISerializer(read_only=True,many=True,source='api_set')
    # location=LocationSerializer(read_only=True,source='customerlocation')

    def get_business_type(self,obj):
        type=obj.business_type
        if type:
            return {
                'id':type.id,
                'name':type.name,
                'description':type.description,
            }
        return None
    def get_location(self,obj):
        location=Location.objects.get(customer=obj)
        if location:
            return{
                'id':location.id,
                'region':location.region,
                'city':location.city,
                'subcity':location.subcity,
                'woreda':location.woreda,
                'zone':location.zone
            }
        return None

    def get_service(self,service):
        if service:
            return {
                'id':service.id,
                'image': 'https://gmsmessaging.pythonanywhere.com' + service.image.url if service.image else None,
                'name':service.name,
                'description':service.description,
                'meta':service.meta,
                'created_at':service.created_at,
                'updated_at':service.updated_at,
            }
        return None

    def get_industry(self,obj):
        type=obj.industry
        if type:
            return {
                'id':type.id,
                'name':type.name,
                'description':type.description,
            }
        return None

    def get_all_content(self,obj):
        campaigns=all_campaigns.objects.filter(customer=obj)
        content=[]
        for campaign in campaigns:
            data={
                'id':campaign.id,
                'date_tobe_sent':campaign.date_tobe_sent,
                'sender':campaign.sender,
                'campaign_name':campaign.campaign_name,
                'ref_number':campaign.ref_number,
                'phones':'https://gmsmessaging/pythonanyehere.com' + campaign.phones.url if campaign.phones else None,
                'customer':campaign.customer.id,
                # 'service':campaign.service.id if campaign.service else None,
                'service':self.get_service(campaign.service),
                'message':campaign.message,
                'approved':campaign.approved,
                'sent':campaign.sent,
                'status':campaign.status,
                'created_at':campaign.created_at,
                'updated_at':campaign.updated_at,
            }
            content.append(data)
        return content

    def get_only_data_campaign(self,obj):
        campaigns=only_data_campaigns.objects.filter(customer=obj)
        content=[]
        for campaign in campaigns:
            data={
                'id':campaign.id,
                # 'service':campaign.service.id if campaign.service else None,
                'service':self.get_service(campaign.service),
                'customer':campaign.customer.id,
                'campaign_name':campaign.campaign_name,
                'ref_number':campaign.ref_number,
                'message':campaign.message,
                'gender':campaign.gender,
                'phone_type':campaign.phone_type,
                'date_tobe_sent':campaign.date_tobe_sent,
                # 'location':campaign.location,
                'industry':campaign.industry.id if campaign.industry else None,
                'industrydetail':self.get_industry(campaign),
                'approved':campaign.approved,
                'sent':campaign.sent,
                'status':campaign.status,
                'created_at':campaign.created_at,
                'updated_at':campaign.id,
            }
            content.append(data)
        return content

    def get_all_data_whitelist(self,obj):
        campaigns=all_campaign_whitelist.objects.filter(customer=obj)
        content=[]
        for campaign in campaigns:
            data={
                'id':campaign.id,
                'date_tobe_sent':campaign.date_tobe_sent,
                'sender':campaign.sender,
                'campaign_name':campaign.campaign_name,
                'ref_number':campaign.ref_number,
                'customer':campaign.customer.id,
                # 'service':campaign.service.id if campaign.service else None,
                'service':self.get_service(campaign.service),
                'message':campaign.message,
                'gender':campaign.gender,
                'phone_type':campaign.phone_type,
                # 'location':campaign.location,
                'industry':campaign.industry.id if campaign.industry else None,
                'industrydetail':self.get_industry(campaign),
                'approved':campaign.approved,
                'sent':campaign.sent,
                'status':campaign.status,
                'created_at':campaign.created_at,
                'updated_at':campaign.updated_at,
            }
            content.append(data)
        return content

    def get_survey(self,obj):
        campaigns=ordinarysurvey.objects.filter(customer=obj)
        content=[]
        for campaign in campaigns:
            data={
                'id':campaign.id,
                'sender':campaign.sender,
                'phones':'https://gmsmessaging.pythonanywhere.com' + campaign.phones.url if campaign.phones else None,
                'customer':campaign.customer.id,
                # 'service':campaign.service.id if campaign.service else None,
                'service':self.get_service(campaign.service),
                'campaign_name':campaign.campaign_name,
                'ref_number':campaign.ref_number,
                'message':campaign.message,
                # 'gender':campaign.gender,
                # 'phone_type':campaign.phone_type,
                'date_tobe_sent':campaign.date_tobe_sent,
                # 'location':campaign.location,
                # 'industry':campaign.industry,
                'created_at':campaign.created_at,
                'updated_at':campaign.updated_at,
                'approved':campaign.approved,
                'sent':campaign.sent,
                'status':campaign.status,
            }
            content.append(data)
        return content

    def get_wallet(self,obj):
        wallets=wallet.objects.filter(user=obj)
        wal=[]
        for w in wallets:
            data= {
                'id':w.id,
                'user':w.user.id,
                'balance':w.balance
            }
            wal.append(data)
        return wal

    def get_total_balance(self,obj):
        # w = userwallet.objects.filter(user=obj)
        if userwallet.objects.filter(user=obj).exists():
            w=userwallet.objects.get(user=obj)
            return {
                'id':w.id,
                'user':w.user.id,
                'balance':w.balance
            }
        return None

    wallet=serializers.SerializerMethodField()
    total_balance=serializers.SerializerMethodField()
    businesstypedetail=serializers.SerializerMethodField(method_name='get_business_type')
    location=serializers.SerializerMethodField(method_name='get_location')
    industrydetail=serializers.SerializerMethodField(method_name='get_industry')
    contents=serializers.SerializerMethodField(method_name='get_all_content')
    onlydatacampaign=serializers.SerializerMethodField(method_name='get_only_data_campaign')
    alldatacampaign=serializers.SerializerMethodField(method_name='get_all_data_whitelist')
    survey=serializers.SerializerMethodField(method_name='get_survey')

    class Meta:
        model=customers
        fields='__all__'
        # fields=['id','email', 'username', 'company_name', 'company_phone', 'contact_person_email', 'contact_person_first_name', 'contact_person_phone', 'employee_number', 'industry', 'business_type',  'usertype','customerphonebook','customerfiles']

    def update(self,instance,validated_data):
        if 'groups' in validated_data:
            validated_data.pop('groups')
        if 'user_permissions' in validated_data:
            validated_data.pop('user_permissions')
        if 'password' in validated_data and validated_data['password'] != instance.password:
            instance.set_password(validated_data['password'])
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class StaffSerializer(serializers.ModelSerializer):
    customerphonebook=CustomerPhoneSerializer(read_only=True,many=True,source='customer_phonebook')
    customerfiles=CustomerFilesSerialzier(many=True,read_only=True,source='customerfiles_set')

    class Meta:
        model=staff
        fields='__all__'

    def update(self,instance,validated_data):
        if 'groups' in validated_data:
            validated_data.pop('groups')
        if 'user_permissions' in validated_data:
            validated_data.pop('user_permissions')
        if 'password' in validated_data and validated_data['password'] != instance.password:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class UsersSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    customerphonebook=CustomerPhoneSerializer(read_only=True,many=True,source='customer_phonebook')
    customerfiles=CustomerFilesSerialzier(many=True,read_only=True,source='customerfiles_set')

    class Meta:
        model = users
        # fields = ('url', 'username', 'company_name', 'company_phone', 'contact_person_email', 'contact_person_first_name', 'contact_person_phone', 'employee_number', 'industry', 'business_type', 'files', 'usertype')
        fields='__all__'
        # extra_kwargs = {'url': {'view_name': 'UserManagment:user-detail'}}

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    code = serializers.IntegerField(write_only=True,required=False, allow_null=True)

    class Meta:
        model = users
        fields = ('email','password','code')

    # def create(self,validated_data):
    #     # us = users.objects.get(username=username)
    #     username=validated_data['username']
    #     if 'password' in validated_data and validated_data['password'] !='':
    #         password=validated_data['password']
    #         user = auth.authenticate(username=username, password=password)
    #         if user:
    #             auth.login(request, user)
    #         else:
    #             raise ValidationErrors('invalid credentials supplied')
    #     elif 'code' in validated_data and validated_data['code'] !='' and validated_data['code'] is not None:
    #         code=validated_data['code']
    #         user=users.objects.get(username=username)
    #         if us and us.otp==code:
    #             auth.login(request, us)
    #         else:
    #             raise ValidationErrors('invalid username or OTP code supplied')
    #     else:
    #         raise validationErrors('please Enter password or OTP code')
        # return user

        # if request.POST['email'] and request.POST['Code']:
        #     verify = client.verify.services(TWILIO_VERIFY_SERVICE_SID)
        #     result = verify.verification_checks.create(to=str(Users.objects.get(email=email).Phone), code=request.POST['Code'])
        #     return response.Response([u['email'],u['idToken'],result.status])
        # return response.Response('{} successfully logged in'.format(user.username))
        # elif request.POST['username'] and request.POST['Code']:
        #     username = request.POST['username']
        #     code = request.POST['Code']
        #     us = users.objects.get(username=username)
        #     #u=authe.sign_in_with_email_and_password(email,us.password)

        #         return response.Response('success')
        #     else:
        #         return response.Response('Please Check your username or OTP')
        # else:
        #     return response.Response('Valid credentials not supplied')


class RegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=users.objects.all())])
    password = serializers.CharField(write_only=True,required=True)
    password_confirmation = serializers.CharField(write_only=True,required=True)
    files=serializers.ListField(child=serializers.CharField(allow_blank=True,allow_null=True),allow_empty=True,allow_null=True)

    def to_internal_value(self,attrs):
        empty=[]
        attrs['username']=attrs['email']
        for field in attrs:
            if attrs[field] =='':
                print(f'{field} empty')
                empty.append(field)
        for var in empty:
            attrs.pop(var)
        return super().to_internal_value(attrs)

    class Meta:
        model = customers
        # fields = ('email', 'company_name', 'company_phone', 'contact_person_email', 'contact_person_first_name', 'contact_person_phone', 'employee_number', 'industry', 'business_type', 'files', 'usertype', 'remember_token', 'password', 'Confirm_password','customerfiles')
        fields='__all__'
        # extra_kwargs = {'email':{'required':True},'last_name':{'required':True},'Phone':{'required':True}}
        # exclude = ['created_at', 'email_verified_at', 'updated_at']

    def validate(self,attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationErrors({'password':'password fields don\'t match.'})
        return attrs

    def create(self,validated_data):
        validated_data.pop('password_confirmation')
        # validated_data['username']=validated_data['email']
        # authe.send_email_verification(u['idToken'])
        # verify = client.verify.services(TWILIO_VERIFY_SERVICE_SID)
        digits = [i for i in range(0,10)]
        # otp='your GMS OTP is '
        code = ''
        for i in range(6):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        # print(otp)

        # message = Message(to_connection='OTP@localhost',to_address=validated_data['Phone'],text=otp,)
        # api = MessageApi(configuration)
        # api.send([message],)
        message = 'Your GMS OTP code is {}'.format(code)
        phone = validated_data['company_phone']
        messagetype = "SMS:TEXT:GSM7BIT:CLASS0"
        recipient = urllib.parse.quote(phone)
        # originator = urllib.parse.quote('GMS') 'originator='+ originator +
        messagedata = urllib.parse.quote(message)
        # username = ozekiUsername
        # password = ozekiPassword
        # sendString = (ozekihttpurl + "api?action=sendmessage" + "&username=" + ozekiusername + "&password=" + ozekipassword + "&recipient=" + recipient + "&messagetype=" + messagetype + "&messagedata=" + messagedata + "&responseformat=json")
        # requests.packages.urllib3.disable_warnings()
        # resp = requests.get(sendString, verify=False)
        # u = authe.create_user_with_email_and_password(validated_data['email'], validated_data['password'])
        # if resp.status_code == 200:
        validated_data['otp']=code
        password=validated_data.pop('password')
        files=validated_data.pop('files')
        user = customers.objects.create(**validated_data)
        for file in files:
            try:
                content_type, image_data = file.split(';base64,')
                decoded_image = base64.b64decode(image_data)
                # Create an InMemoryUploadedFile
                image_file = InMemoryUploadedFile(
                    file=BytesIO(decoded_image),
                    field_name=None,
                    name='uploaded_image{}'.format(mimetypes.guess_extension(content_type, strict=False)),  # Customize the filename
                    content_type=content_type,  # Customize the content type based on your image format
                    size=len(decoded_image),
                    charset=None,
                )
                customerfiles.objects.create(customer=user,file=image_file)
                user.file=image_file
            except Exception as e:
                print(f'error in registration with {e}')
                raise ValidationErrors(f'{e}')
        # user = users.objects.create(
        #     username = validated_data['username'],
        #     company_name = validated_data['company_name'],
        #     # email = validated_data['email'],
        #     company_phone = validated_data['company_phone'],
        #     contact_person_first_name = validated_data['contact_person_first_name'],
        #     contact_person_phone = validated_data['contact_person_phone'],
        #     contact_person_email = validated_data['contact_person_email'],
        #     employee_number = validated_data['employee_number'],
        #     industries = validated_data['industries'],
        #     bussiness_types = validated_data['bussiness_types'],
        #     files = validated_data['files'],
        #     usertype = validated_data['usertype'],
        #     remember_token = validated_data['remember_token'],
        #     otp = code,
        #     # is_active = 'False',
        # )
        userwallet.objects.create(user=user,balance=0.0)
        user.set_password(password)
        user.save()
        return user