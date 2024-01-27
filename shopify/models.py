from django.db import models
import jsonfield
# Create your models here.
class Shopify(models.Model):
    token=models.CharField(max_length=100)
    storename=models.CharField(max_length=100)
    gstin=models.CharField(max_length=100,null=True)
    branch=models.CharField(max_length=100,null=True)
    transaction1=models.CharField(max_length=100,null=True)
    storecode=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    lastsync=models.CharField(max_length=100,null=True)
    datetime1=models.CharField(max_length=100,null=True)
    ccode=models.CharField(max_length=100,null=True)
    ccodepre=models.CharField(max_length=100,null=True)
    stage=models.CharField(max_length=100,null=True,default="True")
    gst_rates=models.CharField(max_length=100,null=True,default="True")
    manage_attribute=models.CharField(max_length=100,null=True,default="True")
    gst_param = jsonfield.JSONField(null=True)
    suspense=models.CharField(max_length=100,null=True,default="True")
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)


    
class Customer(models.Model):
    code=models.CharField(max_length=100,null=True)
    customer_name=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    batch=models.CharField(max_length=100,null=True)
    mobile=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=400,null=True)
    module_type=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    storecode=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class Sales(models.Model):
    invoice_no=models.CharField(max_length=100,null=True)
    customer_name=models.CharField(max_length=100,null=True)
    amount=models.CharField(max_length=100,null=True)
    date=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=400,null=True)
    batch=models.CharField(max_length=100,null=True)
    module_type=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    storecode=models.CharField(max_length=100,null=True)
    postjson = jsonfield.JSONField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class Sales_order(models.Model):
    so_no=models.CharField(max_length=100,null=True)
    customer_name=models.CharField(max_length=100,null=True)
    so_amount=models.CharField(max_length=100,null=True)
    so_date=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    remark=models.CharField(max_length=400,null=True)
    batch=models.CharField(max_length=100,null=True)
    module_type=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    storecode=models.CharField(max_length=100,null=True)
    postjson = jsonfield.JSONField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class Sync(models.Model):
    batch=models.CharField(max_length=100,null=True)
    module_type=models.CharField(max_length=100,null=True)
    date=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    total_record=models.CharField(max_length=100,null=True)
    success_record=models.CharField(max_length=100,null=True)
    fail_record=models.CharField(max_length=100,null=True)
    compid=models.CharField(max_length=100,null=True)
    storecode=models.CharField(max_length=100,null=True)
    recordjson = jsonfield.JSONField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)