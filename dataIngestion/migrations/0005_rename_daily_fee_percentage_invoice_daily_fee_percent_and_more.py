# Generated by Django 4.1.13 on 2024-01-05 13:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dataIngestion", "0004_remove_invoice_id_invoice_uuid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoice",
            old_name="daily_fee_percentage",
            new_name="daily_fee_percent",
        ),
        migrations.RenameField(
            model_name="invoice",
            old_name="haircut_percentage",
            new_name="haircut_percent",
        ),
    ]