from django.db import models
from django.utils import timezone
import jsonfield
from datetime import datetime
from django.contrib.auth.models import User as DjangoUser
# from rest_framework.authtoken.models import Token

class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)


class XML_UserToken(models.Model):
    token=models.CharField(max_length=100,primary_key=True)
    username=models.CharField(max_length=100,null=True)
    branch=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



# Create your models here.
class XML_syncData(models.Model):
    compid=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    syncType=models.CharField(max_length=100,null=True)
    date=models.DateTimeField(default=timezone.now)
    xmldata=models.TextField()
    filedate=models.CharField(max_length=100,null=True)
    token=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)
    
    def __str__(self):
        return f"{self.xmldata}"

class XML_UserData(models.Model):
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
    companyid=models.CharField(max_length=100,null=True)
    token=models.CharField(max_length=100,null=True)
    walkingcustomer=models.CharField(max_length=100,null=True)
    mjseries=models.CharField(max_length=100,null=True)
    clientid=models.CharField (max_length=100,null=True)
    clientsecret=models.CharField (max_length=100,null=True)
    autoSync=models.CharField (max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class syncmanualJournal(models.Model):
    Journalnumber=models.CharField(max_length=100,null=True)
    date=models.CharField(max_length=100,null=True)
    Narration=models.CharField(max_length=100,null=True)
    creditAmount=models.CharField(max_length=100,null=True)
    debitAmount=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=300,null=True)
    Status=models.CharField(max_length=300,null=True)
    jsondata=jsonfield.JSONField(null=True)
    branch=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)


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
    synccl=models.CharField(max_length=100,default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)


class CustomerModelSync(models.Model):
    voucher_field=models.CharField(max_length=100,null=True)
    date_field=models.CharField(max_length=100,null=True)
    compid_field=models.CharField(max_length=100,null=True)
    remark_field=models.CharField(max_length=500,null=True)
    status_field=models.CharField(max_length=300,null=True)
    jsondata_field=jsonfield.JSONField(null=True)
    branch_field=models.CharField(max_length=100,null=True)
    synctype_field=models.CharField(max_length=100,default=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)