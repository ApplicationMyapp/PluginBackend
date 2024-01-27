from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    compid=models.CharField(max_length=100)
    responsedata=models.JSONField()
    remark=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



class TransactionList(models.Model):
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    compid=models.CharField(max_length=100)
    voucherno=models.CharField(max_length=100)
    responsedata=models.JSONField()
    remark=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)
    
