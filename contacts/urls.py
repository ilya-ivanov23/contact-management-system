from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet, basename='contact')

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('import-csv/', views.import_csv, name='import_csv'),
    path('api/', include(router.urls)),
]
