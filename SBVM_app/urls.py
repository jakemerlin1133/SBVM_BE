# SBVM_app/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet  # Or your actual view

router = DefaultRouter()
router.register(r'students', StudentViewSet)  # Or another route name

urlpatterns = router.urls
