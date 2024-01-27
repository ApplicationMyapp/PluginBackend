# Generated by Django 3.2 on 2024-01-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canaraSpring', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditnote_records',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='creditnotesyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='customersyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='expenses_records',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='expensesyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='invoicesyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='product_records',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='productsyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='receipt_records',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='receiptsyncupdate',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='sale_invoice_records',
            name='upadated_at',
        ),
        migrations.AddField(
            model_name='creditnote_records',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='creditnotesyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='customersyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='expenses_records',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='expensesyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='invoicesyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='product_records',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='productsyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='receipt_records',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='receiptsyncupdate',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='sale_invoice_records',
            name='updatad_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='creditnote_records',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='customer_records',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='expenses_records',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product_records',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='receipt_records',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='sale_invoice_records',
            name='compid',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sale_invoice_records',
            name='remark',
            field=models.TextField(null=True),
        ),
    ]
