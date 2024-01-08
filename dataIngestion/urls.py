from django.urls import path, include
from rest_framework import routers
from .views import InvoiceViewSet, UploadViewSet, BaseTemplateView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoice-upload', UploadViewSet, basename='invoice-upload')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('home', BaseTemplateView.as_view(), name='home'),
    path('', include(router.urls)),
]
