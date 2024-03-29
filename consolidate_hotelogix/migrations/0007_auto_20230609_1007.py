# Generated by Django 3.2.16 on 2023-06-09 10:07

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consolidate_hotelogix', '0006_auto_20230529_0755'),
    ]

    operations = [
        migrations.CreateModel(
            name='syncCreditList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Journalnumber', models.CharField(max_length=100, null=True)),
                ('date', models.CharField(max_length=100, null=True)),
                ('Revenuecode', models.CharField(max_length=100, null=True)),
                ('Revenuename', models.CharField(max_length=100, null=True)),
                ('Narration', models.CharField(max_length=100, null=True)),
                ('creditAmount', models.CharField(max_length=100, null=True)),
                ('debitAmount', models.CharField(max_length=100, null=True)),
                ('compid', models.CharField(max_length=100, null=True)),
                ('remark', models.CharField(max_length=100, null=True)),
                ('Status', models.CharField(max_length=100, null=True)),
                ('jsondata', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='hotellogixlogin',
            name='sundryaccode',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
