from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .serializers import InvoiceSerializer, UploadSerializer
from .models import Invoice
from .filters import InvoiceFilter

from WebApp import celery_app
from rest_framework.decorators import action

from datetime import datetime
import os
import pandas as pd


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

    @action(methods=["get"], detail=False, url_name="get-sources", url_path="get-sources")
    def get_sources(self, request, *args, **kwargs):
        sources = Invoice.objects.using('company').order_by().values_list('revenue_source').distinct()
        source_list = [source[0] for source in sources]  # Extracting the string from each tuple
        return render(request, 'select_source.html', {'revenueSources': source_list})

    @action(methods=["get"], detail=False, url_name="get-advance", url_path="get-advance")
    def get_advance(self, request, *args, **kwargs):
        revenue_source = request.query_params.get('revenue_source')
        invoices = Invoice.objects.using('company').filter(
            revenue_source=revenue_source) if revenue_source else Invoice.objects.using('company').all()
        df = pd.DataFrame(list(invoices.values()))
        # Make sure all types are float. Not Decimal from DB.
        df['value'] = df['value'].astype(float)
        df['haircut_percent'] = df['haircut_percent'].astype(float)
        df['daily_fee_percent'] = df['daily_fee_percent'].astype(float)

        # What is the value after haircut
        df['value_after_haircut'] = df['value'] * (1 - df['haircut_percent'] * 0.01)
        # Value of advance after deducting daily fee.
        df['advance'] = df['value_after_haircut'] * (
                1 - df['daily_fee_percent'] * df['expected_payment_duration'] * 0.01)
        df['value_after_daily_fee'] = df['value'] - df['advance']
        df = df.groupby('revenue_source').agg(
            {
                "value": "sum",
                "value_after_haircut": "sum",
                "value_after_daily_fee": "sum",
                "advance": "sum",
            }
        ).reset_index()
        data = zip(df.to_dict(orient='list').values())

        return render(request, 'visualization.html', {"data": data})


# ViewSets define the view behavior.
class UploadViewSet(viewsets.ViewSet):
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return render(request, 'upload_file.html')

    def create(self, request):
        file_uploaded = request.data['file']
        data = file_uploaded.read().decode('utf-8')

        file_path = f"{os.getcwd()}/tmp/{datetime.now().timestamp()}.csv"
        with open(file_path, "w") as file:
            # Create the writer object with tab delimiter
            file.write(data)

        celery_app.send_task('task_save2db', kwargs={"file_name": file_path}, queue="default")
        return render(request, 'upload_success.html')


class BaseTemplateView(TemplateView):
    template_name = 'base.html'  # Specify the template name
