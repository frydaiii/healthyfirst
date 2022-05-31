"""healthyfirst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from healthyfirst.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', views.PersonViewSet, basename='users')
router.register(r'premises', views.PremiseViewSet, basename='premises')
router.register(r'certificate', views.CertificateViewSet, basename='certificate')
router.register(r'businesstype', views.BusinessTypeViewSet, basename='businesstype')
router.register(r'inspectionplan', views.InspectionPlanViewSet, basename='inspectionplan')
router.register(r'sample', views.SampleViewSet, basename='sample')
router.register(r'area', views.AreaViewSet, basename='area')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
