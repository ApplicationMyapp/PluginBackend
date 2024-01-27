from django.db import models
import jsonfield

# Create your models here.
class userSettings(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    branchname=models.CharField(max_length=200)
    branch=models.CharField(max_length=100)
    branchid=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    saveas=models.CharField(max_length=100)
    compid=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    gstin=models.CharField(max_length=100)
    address1=models.CharField(max_length=200)
    JWTToken=models.CharField(max_length=500)
    userId=models.CharField(max_length=10)
    divisionid=models.CharField(max_length=10)
    ledgersetting=jsonfield.JSONField(null=True)
    created_at= models.DateTimeField(auto_now_add=True,null=True)
    updated_at= models.DateTimeField(auto_now=True,null=True)


# ------------------- Last Update Manage ------------------- 

class CustomerSyncUpdate(models.Model):
    lastcustomerdate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class InvoiceSyncUpdate(models.Model):
    lastinvoicedate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class ProductSyncUpdate(models.Model):
    lastproductdate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class CreditNoteSyncUpdate(models.Model):
    lastcreditnotedate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class ExpenseSyncUpdate(models.Model):
    lastexpensedate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class ReceiptSyncUpdate(models.Model):
    lastreceiptdate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

class InventoryDateSyncUpdate(models.Model):
    lastinventorydate=models.CharField(max_length=100,default="")
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

# ------------------- Last Update Manage ------------------- 


class Customer_records(models.Model):
    customer_name=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    account_no= models.CharField(max_length=100)
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    lastsyncdate=models.CharField(max_length=100)
    requestjson=models.JSONField()
    responsejson=models.JSONField()
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)

 


class Sale_Invoice_records(models.Model):
    inv_no=models.CharField(max_length=100)
    inv_date=models.CharField(max_length=100)
    customer_name=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    compid=models.CharField(max_length=100,null=True)
    branch=models.CharField(max_length=100)
    lastsyncdate=models.CharField(max_length=100)
    requestjson=models.JSONField()
    responsejson=models.JSONField()
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



class Product_records(models.Model):
    product_code=models.CharField(max_length=100)
    product_name=models.CharField(max_length=100)
    group_name=models.CharField(max_length=100)
    lastsyncdate=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    requestjson=models.JSONField()  # canara Spring Json
    responsejson=models.JSONField() # Accounting Json
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)


class CreditNote_records(models.Model):
    number=models.CharField(max_length=100)
    debitamount=models.CharField(max_length=100)
    creditamount=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    status=models.CharField(max_length=50)
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    requestjson=models.JSONField()  # canara Spring Json
    responsejson=models.JSONField() # Accounting Json
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



class Expenses_records(models.Model):
    number=models.CharField(max_length=100)
    debitamount=models.CharField(max_length=100)
    creditamount=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    status=models.CharField(max_length=50)
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    requestjson=models.JSONField()  # canara Spring Json
    responsejson=models.JSONField() # Accounting Json
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



class Receipt_records(models.Model):
    number=models.CharField(max_length=100)
    debitamount=models.CharField(max_length=100)
    creditamount=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    status=models.CharField(max_length=50)
    compid=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    requestjson=models.JSONField()  # canara Spring Json
    responsejson=models.JSONField() # Accounting Json
    remark=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updatad_at=models.DateField(auto_now=True,null=True)



