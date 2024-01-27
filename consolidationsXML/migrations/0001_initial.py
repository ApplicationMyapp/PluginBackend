# Generated by Django 3.2 on 2023-12-23 12:52

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModelSync',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_field', models.CharField(max_length=100, null=True)),
                ('date_field', models.CharField(max_length=100, null=True)),
                ('compid_field', models.CharField(max_length=100, null=True)),
                ('remark_field', models.CharField(max_length=500, null=True)),
                ('status_field', models.CharField(max_length=300, null=True)),
                ('jsondata_field', jsonfield.fields.JSONField(null=True)),
                ('branch_field', models.CharField(max_length=100, null=True)),
                ('synctype_field', models.CharField(default=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='syncCreditList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, null=True)),
                ('date', models.CharField(max_length=100, null=True)),
                ('State', models.CharField(max_length=100, null=True)),
                ('billAmount', models.CharField(max_length=100, null=True)),
                ('compid', models.CharField(max_length=100, null=True)),
                ('remark', models.CharField(max_length=300, null=True)),
                ('Status', models.CharField(max_length=300, null=True)),
                ('jsondata', jsonfield.fields.JSONField(null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('synccl', models.CharField(default=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='syncmanualJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Journalnumber', models.CharField(max_length=100, null=True)),
                ('date', models.CharField(max_length=100, null=True)),
                ('Narration', models.CharField(max_length=100, null=True)),
                ('creditAmount', models.CharField(max_length=100, null=True)),
                ('debitAmount', models.CharField(max_length=100, null=True)),
                ('compid', models.CharField(max_length=100, null=True)),
                ('remark', models.CharField(max_length=300, null=True)),
                ('Status', models.CharField(max_length=300, null=True)),
                ('jsondata', jsonfield.fields.JSONField(null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='XML_syncData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compid', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('syncType', models.CharField(max_length=100, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('xmldata', models.TextField()),
                ('token', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='XML_UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('sundryaccode', models.CharField(max_length=100, null=True)),
                ('gstin', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('saveas', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('zip', models.CharField(max_length=100, null=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('ledger_settings', models.JSONField()),
                ('companyid', models.CharField(max_length=100, null=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('walkingcustomer', models.CharField(max_length=100, null=True)),
                ('mjseries', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='XML_UserToken',
            fields=[
                ('token', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
