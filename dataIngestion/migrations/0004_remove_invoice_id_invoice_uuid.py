# Generated by Django 4.1.13 on 2024-01-05 13:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("dataIngestion", "0003_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="id",
        ),
        migrations.AddField(
            model_name="invoice",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
