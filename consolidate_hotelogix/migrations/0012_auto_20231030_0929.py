# Generated by Django 3.2 on 2023-10-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidate_hotelogix', '0011_syncmanualjournal_mjseries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syncmanualjournal',
            name='mjseries',
        ),
        migrations.AddField(
            model_name='hotellogixlogin',
            name='mjseries',
            field=models.CharField(default='Auto', max_length=50),
            preserve_default=False,
        ),
    ]
