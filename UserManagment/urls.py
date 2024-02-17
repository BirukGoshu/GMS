from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from SMS.urls import router as smsrouter

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'register',views.RegisterUser, basename='register')
router.register(r'login',views.LoginUser, basename='login')
router.register(r'account',views.AccountViewSet,basename='account')
router.register(r'customer',views.CustomerViewSet,basename='customer')
router.register(r'api',views.APIViewSet,basename='api')
router.register(r'location',views.LocationViewSet,basename='location')
router.register(r'group',views.GroupViewSet,basename='group')
router.register(r'currentuser',views.CurrentUser,basename='currentuser')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(smsrouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/',views.CustomObtainAuthToken.as_view()),
]