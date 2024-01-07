from django_filters import FilterSet, RangeFilter
from .models import Invoice

class InvoiceFilter(FilterSet):
    value = RangeFilter()
    date = RangeFilter()
    class Meta:
        model = Invoice
        fields = '__all__'