# Generated by Django 3.2 on 2023-09-12 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='commfailedrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('invoicecode', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='commrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('invoicecode', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='depositfailedrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Narration', models.CharField(max_length=100, null=True)),
                ('Credit_Amount', models.CharField(max_length=100, null=True)),
                ('Debit_Amount', models.CharField(max_length=100, null=True)),
                ('depcode', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='depositrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Narration', models.CharField(max_length=100, null=True)),
                ('Credit_Amount', models.CharField(max_length=100, null=True)),
                ('Debit_Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('depcode', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hotellogixlogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('hotelid', models.CharField(max_length=100, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('gstin', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('saveas', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('zip', models.CharField(max_length=100, null=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('ledger_settings', models.JSONField()),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='invoicerecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Customer_Name', models.CharField(max_length=100, null=True)),
                ('Invoice_Amount', models.CharField(max_length=100, null=True)),
                ('Due_Amount', models.CharField(max_length=100, null=True)),
                ('Received_Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.JSONField()),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('invoicecode', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='invoicerecordfailed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Customer_Name', models.CharField(max_length=100, null=True)),
                ('Invoice_Amount', models.CharField(max_length=100, null=True)),
                ('invoicecode', models.CharField(max_length=100, null=True)),
                ('Remark', models.JSONField()),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='paymentfailedrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('paymentcode', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='paymentrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=100, null=True)),
                ('Date', models.CharField(max_length=100, null=True)),
                ('Amount', models.CharField(max_length=100, null=True)),
                ('Remark', models.CharField(max_length=500, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('Requested_json', models.JSONField()),
                ('Response_json', models.JSONField()),
                ('branchid', models.CharField(max_length=100, null=True)),
                ('paymentcode', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
