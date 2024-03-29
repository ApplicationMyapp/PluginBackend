# Generated by Django 3.2.16 on 2023-04-12 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shiprocket', '0002_invoice_awb_dispatch_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='invoice_awb_failed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, null=True)),
                ('InvoiceNo', models.CharField(max_length=100)),
                ('invoice_data', models.JSONField()),
                ('awb_data', models.JSONField()),
                ('companyid', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
