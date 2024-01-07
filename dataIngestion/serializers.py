from rest_framework.serializers import ModelSerializer, Serializer, FileField
from .models import Invoice
# Serializers define the API representation.

class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


# Serializers define the API representation.
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']