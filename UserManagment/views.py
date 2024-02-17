from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, generics, permissions, serializers, response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from django.contrib.auth.models import auth
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core import serializers as ser
import json
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
# from .exceptions import ValidationErrors

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False,methods=['POST'])
    def logout(self,request):
        user=request.user
        print(f'logout user {user.email}')
        # us=auth.authenticate(email=user.email)
        # print(f'us = {us}')
        token=Token.objects.filter(user=user)
        print(f'token={token}')
        token.delete()
        return response.Response('logout succesful')

class CurrentUser(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # @action(detail=False, methods=['GET'])
    def list(self, request):
        # Retrieve the current user
        user = request.user
        if customers.objects.filter(email=user.email).exists():
            customer=customers.objects.get(email=user.email)
            userdata=CustomersSerializer(customer).data
        elif staff.objects.filter(email=user.email).exists():
            s=staff.objects.get(email=user.email)
            userdata=StaffSerializer(s).data
        else:
            userdata=UsersSerializer(user).data
        return response.Response(userdata)

    def update(self,request,pk=None):
        uid=request.data.get('id')
        user = Users.objects.get(id=uid)
        if customers.objects.filter(email=user.email).exists():
            customer=customers.objects.filter(email=user.email)
            serializer=CustomersSerializer(customer, data=request.data,context={'request':request}, partial=True)
            if serializer.is_valid():
                print('valid customer update')
                serializer.save()
                return response.Response(serializer.data)
            else:
                # print(serializer)
                return response.Response(serializer.errors, status=422)
            # userdata=CustomersSerializer(customer).data
        elif staff.objects.filter(email=user.email).exists():
            s=staff.objects.get(email=user.email)
            serializer=StaffSerializer(s, data=request.data,context={'request':request}, partial=True)
            if serializer.is_valid():
                print('valid staff update')
                serializer.save()
                return response.Response(serializer.data)
            else:
                # print(serializer)
                return response.Response(serializer.errors, status=422)
            # userdata=StaffSerializer(s).data
        else:
            # userdata=UsersSerializer(user).data
            serializer=UsersSerializer(users.objects.get(email=user.email), data=request.data,context={'request':request}, partial=True)
            if serializer.is_valid():
                print('valid user update')
                serializer.save()
                return response.Response(serializer.data)
            else:
                # print(serializer)
                return response.Response(serializer.errors, status=422)


class GroupViewSet(viewsets.ModelViewSet):
    queryset=group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, pk=None):
        serializer = GroupSerializer(group.objects.get(id=request.data['id']),data=request.data,context={'request':request}, partial=True)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            # print(serializer)
            return response.Response(serializer.errors, status=422)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]

class APIViewSet(viewsets.ModelViewSet):
    queryset=API.objects.all()
    serializer_class=APISerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class LocationViewSet(viewsets.ModelViewSet):
    queryset=Location.objects.all()
    serializer_class=LocationSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = customers.objects.all()
    serializer_class = CustomersSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginUser(GenericViewSet,ListModelMixin):
    queryset = users.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        if request.data['email'] and request.data['password']:
            email = request.data['email']
            password = request.data['password']
            # u=authe.sign_in_with_email_and_password(email,password),u['idToken']]
            # us = users.objects.get(username=username)
            user = auth.authenticate(email=email, password=password)
            if user:
                if user.disabled==False:
                    auth.login(request, user)
                    return response.Response('{} successfully logged in'.format(user.email))
                else:
                    return response.Response('{} account has been disabled please contact our staff'.format(user.email),status=422)
            else:
                return response.Response('invalid creds',status=422)
        elif request.data['email'] and request.data['code']:
            email = request.data['email']
            code = request.data['code']
            user = users.objects.get(email=email)
            #u=authe.sign_in_with_email_and_password(email,us.password)
            if user and user.otp==code:
                if user.disabled==False:
                    auth.login(request, user)
                    return response.Response('{} successfully logged in'.format(user.email))
                else:
                    return response.Response('{} account has been disabled please contact our staff'.format(user.email),status=422)
            else:
                return response.Response('Please Check your username or OTP')
        else:
            return response.Response('Valid credentials not supplied',status=422)

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomTokenSerializer()
    def post(self, request, *args, **kwargs):
        #user = Users.objects.get(email=request.data['email'])
        email = request.data['email']
        password = request.data['password']
        try:
            user = auth.authenticate(email=email,password=password)
            if user and user.disabled==False:
                token = Token.objects.get_or_create(user=user)[0].key
                u = ser.serialize("json",users.objects.filter(email=request.data['email']))
                use = json.loads(u)[0]
                resp = {}
                resp.update(use['fields'])
                return response.Response({'token': token, 'user': resp})
            else:
                    return response.Response('{} account has been disabled please contact our staff'.format(user.username))
        except Exception as e:
            print(f'error in auth with {e}')
            return response.Response('Invalid credentials provided', status=422)

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        user=self.request.user
        if customers.objects.filter(email=user.email).exists():
            return customers.objects.get(email=user.email)
        elif staff.objects.filter(email=user.email).exists():
            return saff.objects.get(email=user.email)
        else:
            return user

    def get_queryset(self):
        user=self.request.user
        if customers.objects.filter(email=user.email).exists():
            return customers.objects.filter(email=user.email)
        elif staff.objects.filter(email=user.email).exists():
            return saff.objects.filter(email=user.email)
        else:
            return users.objects.filter(email=user.email)

    def get_serializer_class(self):
        obj = self.get_object()
        if isinstance(obj,customers):
            return CustomersSerializer
        elif isinstance(obj,staff):
            return StaffSerializer
        else:
            return UsersSerializer

    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(obj)
            return response.Response(serializer.data)
        except Exception as e:
            return response.Response(e, status=422)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self,request,pk=None):
        uid=request.data.get('id')
        user=users.objects.get(id=uid)
        if customers.objects.filter(email=user.email).exists():
            serializer=CustomersSerializer(customers.objects.get(email=user.email),data=request.data,context={'request':request},partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data,status=200)
            else:
                return response.Response(serializer.errors,status=422)
        elif staff.objects.filter(email=user.email).exists():
            serializer=StaffSerializer(staff.objects.get(email=user.email),data=request.data,context={'request':request},partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data,status=200)
            else:
                return response.Response(serializer.errors,status=422)
        else:
            serializer=UsersSerializer(users.objects.get(email=user.email),data=request.data,context={'request':request},partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data,status=200)
            else:
                return response.Response(serializer.errors,status=422)

class RegisterUser(CreateModelMixin, GenericViewSet):
    model = customers
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]