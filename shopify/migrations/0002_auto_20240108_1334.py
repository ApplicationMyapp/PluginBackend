# Generated by Django 3.2 on 2024-01-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sales_order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sales_order',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='shopify',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shopify',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sync',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='sync',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
