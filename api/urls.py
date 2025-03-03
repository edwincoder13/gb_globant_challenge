from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import departments_view_set
from .views import jobs_view_set
from .views import csv_upload_rds
from .views import hired_employees_view_set
from .views import get_numberofemployees_hired
from .views import get_numberofemployees_avg

router = DefaultRouter()
router.register(r'departaments', departments_view_set)
router.register(r'jobs', jobs_view_set)
router.register(r'hired_employees', hired_employees_view_set)

urlpatterns = [
    path('api/', include(router.urls)),
    path('csv_upload_rds/', csv_upload_rds.as_view(), name='csv_upload_rds'),
    path('get_numberofemployees_hired/', get_numberofemployees_hired.as_view(), name='get_numberofemployees_hired'),
    path('get_numberofemployees_avg/', get_numberofemployees_avg.as_view(), name='get_numberofemployees_avg'),
]
