from celery import shared_task
from typing import Tuple
import csv

from .models import Invoice


@shared_task(name='task_save2db')
def task_save2db(file_name) -> Tuple[int, str]:
    """
    Save all the files in the tmp to the database.
    :return:
    """
    batch_size = 5000
    with open(f"{file_name}", 'r') as f:
        csv_file = csv.DictReader(f, quotechar='"', delimiter=',')
        csv_file.fieldnames = [name.replace(' ', '_').lower() for name in csv_file.fieldnames]
        nrows = 0
        rows = []
        for row in csv_file:
            rows.append(Invoice(**row))
            nrows += 1
            if nrows == batch_size:
                rows = []
                Invoice.objects.using('company').bulk_create(rows, batch_size=batch_size)

        Invoice.objects.using('company').bulk_create(rows, batch_size=batch_size)
