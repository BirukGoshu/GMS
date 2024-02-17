from rest_framework import serializers
from .models import *
from GMS.settings import chapakey
from UserManagment.exceptions import ValidationErrors
from UserManagment.models import *
from UserManagment.serializers import UsersSerializer,CustomersSerializer,LocationSerializer
import base64,mimetypes,math,random
from chapa import Chapa
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class BussinessTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = bussiness_types
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):

    class Meta:
        model = industries
        fields = '__all__'
class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model=template
        fields='__all__'

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=SubCategories
        fields='__all__'

class CategorySerialzier(serializers.ModelSerializer):
    subcategorydetail=SubCategorySerializer(read_only=True,many=True,source='subcategory')

    class Meta:
        model=Category
        fields='__all__'

class CustomCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomCategory
        fields='__all__'

class PackageSubscriptionSerializer(serializers.ModelSerializer):
    categorydetail=CategorySerialzier(read_only=True,source='category')
    customcategorydetail=CustomCategorySerializer(read_only=True,source='customcategory')

    class Meta:
        model = package_subscriptions
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    # image=CharField(max_length=400,allow_blank=True,allow_null=True)

    def to_internal_value(self,attrs):
        if 'image' in attrs:
            try:
                content_type, image_data = image.split(';base64,')
                decoded_image = base64.b64decode(image_data)
                content_type=content_type.split(':')[1]
                # Create an InMemoryUploadedFile
                image_file = InMemoryUploadedFile(
                    file=BytesIO(decoded_image),
                    field_name=None,
                    name='uploaded_image{}'.format(mimetypes.guess_extension(content_type,strict=False)),  # Customize the filename
                    content_type=content_type,  # Customize the content type based on your image format
                    size=len(decoded_image),
                    charset=None,
                )
                attrs['image']=image_file
            except Exception as e:
                print(f'error in registration with {e}')
                return response.Response({'error': 'Invalid image data'}, status=400)
        return super().to_internal_value(attrs)

    class Meta:
        model = services
        fields = '__all__'

class SMSSerializer(serializers.ModelSerializer):
    # creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # creator = serializers.CharField(read_only=True, source='creator.username')
    Sender=serializers.CharField(write_only=True,required=False)

    class Meta:
        model=SMS
        fields = '__all__'

class BulkSMSSerializer(serializers.ModelSerializer):
    # creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #creator = serializers.CharField(read_only=True, source='creator.username')

    class Meta:
        model = BulkSMS
        fields = '__all__'

class AllCampaingSerializer(serializers.ModelSerializer):
    # customer_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    phones = serializers.FileField(read_only=True)
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)

    class Meta:
        model = all_campaigns
        fields = '__all__'

    def create(self,validated_data):
        # if 'messagetype' in self.context['request'].data:
        #     type=self.context['request'].data['messagetype']
        #     if 'flash' in type.name:
        #         messagetype='SMS:TEXT:GSM7BIT:CLASS0'
        #     elif 'promotion' in type.name:
        #         messagetype='SMS:TEXT:GSM7BIT:CLASS1'
        #     else:
        #         messagetype='SMS:TEXT'
        if 'files' in self.context['request'].data:
            phone=self.context['request'].data.get('files')

            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            # if customers.objects.filter(email=self.context['request'].user.email).exists():
            #     validated_data['customer']=customers.objects.get(email=self.context['request'].user.email)

            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
                content_type=content_type.split(':')[1]
            except Exception as e:
                print(f'error {e}')
                raise serializers.ValidationError({'error': 'Invalid file phones'})
            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='content_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        code=''
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='content-{}'.format(code)
        ac=all_campaigns.objects.create(**validated_data)
        return ac

    def update(self,instance,validated_data):
        if 'phones' in self.context['request'].data and self.context['request'].data.get('phones') != instance.phones:
            phone=self.context['request'].data.get('phones')
            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            # validated_data['customer']=self.context['request'].user
            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
                content_type=content_type.split(':')[1]
            except Exception as e:
                raise serializers.ValidationError({'error': 'Invalid file phones'})

            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='content_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class OnlyDataCampaignSerializer(serializers.ModelSerializer):
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)
    occupation=serializers.PrimaryKeyRelatedField(queryset=industries.objects.all(),write_only=True,required=False)
    industrydetail=IndustrySerializer(read_only=True,source='industry')
    locationdetail=LocationSerializer(read_only=True,source='location')

    class Meta:
        model = only_data_campaigns
        fields='__all__'

    def create(self,validated_data):
        # if self.context['request'].user.is_superuser:
        #     validated_data['customer']=self.context['request'].data.get('customer')
        # else:
        # if customers.objects.filter(email=self.context['request'].user.email).exists():
        #     validated_data['customer']=customers.objects.get(email=self.context['request'].user.email)
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        code=''
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='only-data-campaign-{}'.format(code)
        validated_data['industry']=validated_data['occupation']
        validated_data.pop('occupation')
        od=only_data_campaigns.objects.create(**validated_data)
        return od

class AllCampaignWhitelistSerialzier(serializers.ModelSerializer):
    phones = serializers.FileField(read_only=True)
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)
    occupation=serializers.PrimaryKeyRelatedField(queryset=industries.objects.all(),write_only=True,required=False)
    industrydetail=IndustrySerializer(read_only=True,source='industry')
    locationdetail=LocationSerializer(read_only=True,source='location')

    class Meta:
        model=all_campaign_whitelist
        fields='__all__'

    def create(self,validated_data):
        if 'phone' in self.context['request'].data:
            phone=self.context['request'].data.get('phones')
            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            # if customers.objects.filter(email=self.context['request'].user.email).exists():
            # validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
                content_type=content_type.split(':')[1]
            except Exception as e:
                raise serializers.ValidationError({'error': 'Invalid file phones'})
            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='all_campaign_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        code=''
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='all-campaign-whitelist-{}'.format(code)
        validated_data['industry']=validated_data['occupation']
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        validated_data.pop('occupation')
        ac=all_campaign_whitelist.objects.create(**validated_data)
        return ac

    def update(self,instance,validated_data):
        if 'phones' in self.context['request'].data and self.context['request'].data.get('phones') != instance.phones:
            phone=self.context['request'].data.get('phones')
            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            #     validated_data['customer']=self.context['request'].user
            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
            except Exception as e:
                raise serializers.ValidationError({'error': 'Invalid file phones'})
            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='all_campaign_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class SurveySerializer(serializers.ModelSerializer):
    phones = serializers.FileField(read_only=True)
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)
    industrydetail=IndustrySerializer(read_only=True,source='industry')
    locationdetail=LocationSerializer(read_only=True,source='location')
    occupation=serializers.PrimaryKeyRelatedField(queryset=industries.objects.all(),write_only=True,required=False)

    class Meta:
        model=ordinarysurvey
        fields='__all__'

    def create(self,validated_data):
        if 'files' in self.context['request'].data:
            phone=self.context['request'].data.get('files')
            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            # if customers.objects.filter(email=self.context['request'].user.email).exists():
            #     validated_data['customer']=customers.objects.get(email=self.context['request'].user.email)
            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
                content_type=content_type.split(':')[1]
            except Exception as e:
                raise serializers.ValidationError({'error': 'Invalid file phones'})
            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='survey_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        code=''
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='ordinary-survey-{}'.format(code)
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        validated_data['industry']=validated_data['occupation']
        validated_data.pop('occupation')
        survay=ordinarysurvey.objects.create(**validated_data)
        return survay

    def update(self,instance,validated_data):
        if 'phones' in self.context['request'].data and self.context['request'].data.get('phones') != instance.phones:
            phone=self.context['request'].data.get('phones')
            # if self.context['request'].user.is_superuser:
            #     validated_data['customer']=self.context['request'].data.get('customer')
            # else:
            #     validated_data['customer']=self.context['request'].user
            try:
                # Split the image data into content type and base64-encoded data
                content_type, phone_data = phone.split(';base64,')
                decoded_file = base64.b64decode(phone_data)
                content_type=content_type.split(':')[1]
            except Exception as e:
                raise serializers.ValidationError({'error': 'Invalid file phones'})
            # Create an InMemoryUploadedFile from the decoded image data
            phone_file = InMemoryUploadedFile(
                file=BytesIO(decoded_file),
                field_name=None,
                name='survey_phone{}'.format(mimetypes.guess_extension(content_type, strict=False)),
                content_type=content_type,
                size=len(decoded_file),
                charset=None,
            )
            validated_data['phones']=phone_file
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class DemographicSurveySerializer(serializers.ModelSerializer):
    # phones = serializers.FileField(read_only=True)
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)
    occupation=serializers.PrimaryKeyRelatedField(queryset=industries.objects.all(),write_only=True,required=False)
    industrydetail=IndustrySerializer(read_only=True,source='industry')
    locationdetail=LocationSerializer(read_only=True,source='location')

    class Meta:
        model=demographicsurvey
        fields='__all__'

    def create(self,validated_data):
        # if 'files' in self.context['request'].data:
        #     phone=self.context['request'].data.get('files')
        #     # if self.context['request'].user.is_superuser:
        #     #     validated_data['customer']=self.context['request'].data.get('customer')
        #     # else:
        #     if customers.objects.filter(email=self.context['request'].user.email).exists():
        #         validated_data['customer']=customers.objects.get(email=self.context['request'].user.email)
        #     try:
        #         # Split the image data into content type and base64-encoded data
        #         content_type, phone_data = phone.split(';base64,')
        #         decoded_file = base64.b64decode(phone_data)
        #     except Exception as e:
        #         raise serializers.ValidationError({'error': 'Invalid file phones'})
        #     # Create an InMemoryUploadedFile from the decoded image data
        #     phone_file = InMemoryUploadedFile(
        #         file=BytesIO(decoded_file),
        #         field_name=None,
        #         name='uploaded_image.jpg',
        #         content_type=content_type,
        #         size=len(decoded_file),
        #         charset=None,
        #     )
        #     validated_data['phones']=phone_file
        code=''
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='demograhic-survay-{}'.format(code)
        validated_data['industry']=validated_data['occupation']
        validated_data.pop('occupation')
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        survay=demographicsurvey.objects.create(**validated_data)
        return survay

    # def update(self,instance,validated_data):
    #     if 'phones' in self.context['request'].data and self.context['request'].data.get('phones') != instance.phones:
    #         phone=self.context['request'].data.get('phones')
    #         # if self.context['request'].user.is_superuser:
    #         #     validated_data['customer']=self.context['request'].data.get('customer')
    #         # else:
    #         #     validated_data['customer']=self.context['request'].user
    #         try:
    #             # Split the image data into content type and base64-encoded data
    #             content_type, phone_data = phone.split(';base64,')
    #             decoded_file = base64.b64decode(phone_data)
    #         except Exception as e:
    #             raise serializers.ValidationError({'error': 'Invalid file phones'})
    #         # Create an InMemoryUploadedFile from the decoded image data
    #         phone_file = InMemoryUploadedFile(
    #             file=BytesIO(decoded_file),
    #             field_name=None,
    #             name='uploaded_image.jpg',
    #             content_type=content_type,
    #             size=len(decoded_file),
    #             charset=None,
    #         )
    #         validated_data['phones']=phone_file
    #     for field in validated_data:
    #         setattr(instance, field, validated_data[field])
    #     instance.save()
    #     return instance

class InternalSurveySerializer(serializers.ModelSerializer):
    # phones = serializers.FileField(read_only=True)
    customer=CustomersSerializer(read_only=True)
    servicedetail=ServiceSerializer(read_only=True,source='service')
    ref_number=serializers.CharField(read_only=True)
    industrydetail=IndustrySerializer(read_only=True,source='industry')
    locationdetail=LocationSerializer(read_only=True,source='location')
    occupation=serializers.PrimaryKeyRelatedField(queryset=industries.objects.all(),write_only=True,required=False)

    class Meta:
        model=internalsurvey
        fields='__all__'

    def create(self,validated_data):
        # if 'files' in self.context['request'].data:
        #     phone=self.context['request'].data.get('files')
        #     # if self.context['request'].user.is_superuser:
        #     #     validated_data['customer']=self.context['request'].data.get('customer')
        #     # else:
        #     if customers.objects.filter(email=self.context['request'].user.email).exists():
        #         validated_data['customer']=customers.objects.get(email=self.context['request'].user.email)
        #     try:
        #         # Split the image data into content type and base64-encoded data
        #         content_type, phone_data = phone.split(';base64,')
        #         decoded_file = base64.b64decode(phone_data)
        #     except Exception as e:
        #         raise serializers.ValidationError({'error': 'Invalid file phones'})
        #     # Create an InMemoryUploadedFile from the decoded image data
        #     phone_file = InMemoryUploadedFile(
        #         file=BytesIO(decoded_file),
        #         field_name=None,
        #         name='uploaded_image.jpg',
        #         content_type=content_type,
        #         size=len(decoded_file),
        #         charset=None,
        #     )
        #     validated_data['phones']=phone_file
        code=''
        digits = [i for i in range(0,10)]
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        validated_data['ref_number']='internal-survey-{}'.format(code)
        validated_data['customer']=customers.objects.get(id=self.context['request'].user.id)
        validated_data['industry']=validated_data['occupation']
        validated_data.pop('occupation')
        survay=internalsurvey.objects.create(**validated_data)
        return survay

class UserWalletSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    userdetail=UsersSerializer(read_only=True,source='user')

    class Meta:
        model = userwallet
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    userdetail=UsersSerializer(read_only=True,source='user')

    class Meta:
        model = wallet
        fields = '__all__'

    def create(self,validated_data):
        w=wallet.objects.create(**validated_data)
        digits = [i for i in range(0,10)]
        code = ''
        for i in range(20):
            index = math.floor(random.random()*10)
            code += str(digits[index])
        # wallet=userwallet.objects.filter(user=validated_data['user'])
        if userwallet.objects.filter(user=validated_data['user']).exists():
            wallet=userwallet.objects.get(user=validated_data['user'])
        else:
            wallet=userwallet.objects.create(user=validated_data['user'],balance=0.0)
        us=wallet.user
        tx_ref = 'WALLET-DEPOSIT-{}-{}'.format(us.id,code)
        print(f'tx_ref{tx_ref}')
        data = {
            'email': us.email,
            'amount': validated_data['amount'],
            'first_name': us.first_name if us.first_name else us.username,
            'last_name': us.last_name if us.last_name else us.username,
            'tx_ref': tx_ref,
            # 'phone_number': us.company_phone,
            # optional
            #'callback_url': 'https://7969-196-191-60-134.ngrok-free.app/UserManagment/verifypayment/{}'.format(tx_ref),
            'callback_url': 'https://gmsmessaging.pythonanywhere.com/api/verifywalletpayment/{}/{}/'.format(w.id,tx_ref),
            # 'return_url': 'https://d3a9-196-191-61-222.ngrok-free.app/wallet',
            'customization': {
                'title': 'wallet deposit',
                'description': 'deposit to GMS wallet',
            }
        }
        chapa = Chapa(chapakey, response_format='json')
        # print(f'chapa - {chapa.initialize(**data)}')
        # print(f'data {data}')
        try:
            # print(f'chapa - {chapa.initialize(**data)}')
            resp = chapa.initialize(**data)
            time.sleep(1)
            w.checkoutdata=resp
            # order.status='payment initialized'
            w.save()
            # print(f'insurance payment data {order.checkoutdata}')
        except:
            raise ValidationErrors('chappa connection error')
        print(f'response {resp}')
        if resp['status'] == 'success':
            # w=wallet.objects.create(**validated_data)
            return w
            # print(f'response {resp}')
        else:
            raise ValidationErrors(resp['message'])

class paymentserializer(serializers.ModelSerializer):
    wallet=serializers.PrimaryKeyRelatedField(queryset=wallet.objects.all(),write_only=True)
    amount=serializers.FloatField()

    class Meta:
        model=wallet
        fields=('wallet','amount')
        # fields='__all__'

    def create(self, validated_data):
        digits = [i for i in range(0,10)]
        code = ''
        for i in range(20):
            index = math.floor(random.random()*10)
            # otp += str(digits[index])
            code += str(digits[index])
        # order=InsoranceOrder.objects.get(id=validated_data['id'])
        # order=validated_data['id']
        # if order.insurancetype.name=='Product'  or order.insurancetype.name=='product':
        #     # us = Users.objects.get(email=order.product.user.email)
        #     us=order.product.user
        # elif order.insurancetype.name=='Warehouse'  or order.insurancetype.name=='warehouse':
        #     us=order.warehouse.admin
        # elif order.insurancetype.name=='Storage Type'  or order.insurancetype.name=='storage type':
        #     us=order.mapping.warehouse.admin
        # print(us)
        wallet=validated_data['wallet']
        us=wallet.user
        tx_ref = 'INSURANCE-PAYMENT-{}-{}'.format(us.id,code)

        print(f'tx_ref{tx_ref}')
        data = {
            'email': us.email,
            'amount': validated_data['amount'],
            'first_name': us.first_name if us.first_name else us.username,
            'last_name': us.last_name if us.last_name else us.username,
            'tx_ref': tx_ref,
            # 'phone_number': us.company_phone,
            # optional
            #'callback_url': 'https://7969-196-191-60-134.ngrok-free.app/UserManagment/verifypayment/{}'.format(tx_ref),
            'callback_url': 'https://gmsmessaging.pythonanywhere.com/api/verifywalletpayment/{}/{}/'.format(wallet.id,tx_ref),
            # 'return_url': 'https://d3a9-196-191-61-222.ngrok-free.app/wallet',
            'customization': {
                'title': 'insurance order',
                'description': 'Payment for your Insurance Order',
            }
        }

        chapa = Chapa(chapakey, response_format='json')
        # print(f'chapa - {chapa.initialize(**data)}')
        # print(f'data {data}')

        try:
            # print(f'chapa - {chapa.initialize(**data)}')
            resp = chapa.initialize(**data)
            time.sleep(1)
            # order.checkoutdata=resp
            # order.status='payment initialized'
            # order.save()
            # print(f'insurance payment data {order.checkoutdata}')
        except:
            raise ValidationErrors('chappa connection error')
        print(f'response {resp}')
        if resp['status'] == 'success':
            return resp
            # print(f'response {resp}')
        else:
            raise ValidationErrors(resp['message'])

