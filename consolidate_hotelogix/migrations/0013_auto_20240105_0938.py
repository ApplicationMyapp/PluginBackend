# Generated by Django 3.2 on 2024-01-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidate_hotelogix', '0012_auto_20231030_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotellogixlogin',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='hotellogixlogin',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='synccreditlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='synccreditlist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='syncmanualjournal',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='syncmanualjournal',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
