from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import InvoiceSerializer, UploadSerializer
from .models import Invoice
from .filters import InvoiceFilter

from WebApp import celery_app
from rest_framework.decorators import action

from datetime import datetime
import os


# ViewSets define the view behavior.
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.using('company').all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ('get',)
    filter_backends = [DjangoFilterBackend]
    filter_class = InvoiceFilter
    filterset_fields = ["uuid", "date", "invoice_number", "value", "haircut_percent", "daily_fee_percent", "currency",
                        "revenue_source", "customer", "expected_payment_duration"]

    @action(methods=["get"], detail=True, url_name="get-advance", url_path="get-advance")
    def get_advance(self, request, *args, **kwargs):
        revenue_source = request.data.get('revenue_source')
        invoices = Invoice.objects.using('company').filter(
            revenue_source=revenue_source) if revenue_source else Invoice.objects.using('company').all()
        return invoices


# ViewSets define the view behavior.
class UploadViewSet(viewsets.ViewSet):
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.data['upload_file']
        data = file_uploaded.read().decode('utf-8')

        file_path = f"{os.getcwd()}/tmp/{datetime.now().timestamp()}.csv"
        with open(file_path, "w") as file:
            # Create the writer object with tab delimiter
            file.write(data)

        celery_app.send_task('task_save2db', kwargs={"file_name": file_path}, queue="default")
        return Response(f"POST API and you have uploaded a csv file")
