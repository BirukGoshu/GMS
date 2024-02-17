from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
#from UserManagment.urls import *

router = routers.DefaultRouter()
router.register(r'sms', views.SMSViewSet, basename='sms')
router.register(r'bulksms', views.BulkSMSViewSet, basename='bulksms')
router.register(r'content', views.AllCampaignViewSet, basename='content')
router.register(r'onlydatacampaign', views.OnlyDataCampaignViewSet, basename='onlydatacampaign')
router.register(r'allcampaign',views.AllCampaignWhitelistViewSet,basename='allcampaign')
router.register(r'ordinarysurvey',views.SurveyViewSet,basename='ordinarysurvey')
router.register(r'demographicsurvey',views.DemographicSurveyViewSet,basename='demographicsurvey')
router.register(r'internalsurvey',views.InternalSurveyViewSet,basename='internalsurvey')
router.register(r'template',views.TemplateViewSet,basename='template')
router.register(r'businesstypes', views.BussinessTypeViewSet, basename='businesstypes')
router.register(r'industries', views.IndustryViewSet, basename='industries')
router.register(r'packagesubscription', views.PackageSubscriptionViewSet, basename='packagesubscription')
router.register(r'category',views.CategoryViewSet,basename='category')
router.register(r'subcategory',views.SubCategoryViewSet,basename='subcategory')
router.register(r'customcategory',views.CustomCategoryViewSet,basename='customcategory')
router.register(r'service', views.ServiceViewSet, basename='service')
router.register(r'wallet', views.WalletViewSet, basename = 'wallet')
router.register(r'userwallet',views.UserWalletViewSet,basename='userwallet')
router.register(r'walletpayment',views.WalletPaymentViewSet,basename='walletpayment')

urlpatterns = [
    path('', include(router.urls)),
    path('verifywalletpayment/<int:id>/<slug:slug>/',views.verifywalletpayment,name='walletpayment'),
    #path('usermanagment' , include('UserManagment.urls')),
]
