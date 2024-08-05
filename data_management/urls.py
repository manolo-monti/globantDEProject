from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, JobViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]