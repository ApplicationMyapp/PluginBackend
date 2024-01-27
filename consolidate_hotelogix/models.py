from django.db import models
import jsonfield

# Create your models here.

class hotellogixlogin(models.Model):
    branch=models.CharField(max_length=100,null=True)
    category=models.CharField(max_length=100,null=True)
    sundryaccode=models.CharField(max_length=100,null=True)
    gstin=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    saveas=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    zip=models.CharField(max_length=100,null=True)
    address1=models.CharField(max_length=100,null=True)
    ledger_settings=models.JSONField()
    mjseries=models.CharField(max_length=50)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


class syncmanualJournal(models.Model):
    Journalnumber=models.CharField(max_length=100,null=True)
    date=models.CharField(max_length=100,null=True)
    Revenuecode=models.CharField(max_length=100,null=True)
    Revenuename=models.CharField(max_length=100,null=True)
    Narration=models.CharField(max_length=100,null=True)
    creditAmount=models.CharField(max_length=100,null=True)
    debitAmount=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=300,null=True)
    Status=models.CharField(max_length=300,null=True)
    jsondata=jsonfield.JSONField(null=True)
    branch=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


class syncCreditList(models.Model):
    number=models.CharField(max_length=100,null=True)
    date=models.CharField(max_length=100,null=True)
    State=models.CharField(max_length=100,null=True)
    billAmount=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=300,null=True)
    Status=models.CharField(max_length=300,null=True)
    jsondata=jsonfield.JSONField(null=True)
    branch=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)