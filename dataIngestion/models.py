from django.db import models

# Create your models here.

from django.db import models
import uuid

class Invoice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField("date published")
    invoice_number = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    haircut_percent = models.DecimalField(max_digits=10, decimal_places=2)
    daily_fee_percent = models.DecimalField(max_digits=10, decimal_places=5)
    currency = models.CharField(max_length=10)
    revenue_source = models.CharField(max_length=40)
    customer = models.CharField(max_length=40)
    expected_payment_duration = models.IntegerField(help_text="number of days until payment")

