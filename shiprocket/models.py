from django.db import models

# Create your models here.

class Shiprocketlogin(models.Model):
    # api_key=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=100)
    gstin=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    cemail=models.CharField(max_length=100)
    cphone=models.CharField(max_length=100)
    cname=models.CharField(max_length=100)
    channelid=models.CharField(max_length=100)
    pickup_location=models.CharField(max_length=100)
    companyid=models.CharField(max_length=100)
    dimension_status=models.CharField(max_length=100)
    weight=models.CharField(max_length=100)
    length=models.CharField(max_length=100)
    breadth=models.CharField(max_length=100)
    height=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


class showorderdetails(models.Model):
    SalesOrderNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100,null=True)
    orderdate=models.CharField(max_length=100,null=True)
    frompincode=models.CharField(max_length=100,null=True)
    topincode=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    shippingaddress=models.CharField(max_length=254,null=True)
    posted_at=models.CharField(max_length=100,null=True)
    ordertype=models.CharField(max_length=100,null=True)
    weight=models.CharField(max_length=100,null=True)
    length=models.CharField(max_length=100,null=True)
    breadth=models.CharField(max_length=100,null=True)
    height=models.CharField(max_length=100,null=True)
    shipmentno=models.CharField(max_length=100,null=True)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)




class check_availability_data(models.Model):
    SalesOrderNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    orderdate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    ordertype=models.CharField(max_length=100)
    mode=models.CharField(max_length=100,default='SURFACE')
    availability=models.CharField(max_length=100)
    returnable=models.CharField(max_length=100,default='Yes')
    courier_agent=models.CharField(max_length=100)
    weight=models.CharField(max_length=100,null=True)
    length=models.CharField(max_length=100,null=True)
    breadth=models.CharField(max_length=100,null=True)
    height=models.CharField(max_length=100,null=True)
    shipmentno=models.CharField(max_length=100,null=True)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)




class popup_check_data(models.Model):
    statusid=models.CharField(max_length=100,null=True)
    courier_id=models.CharField(max_length=100,null=True)
    courier_name=models.CharField(max_length=100,null=True)
    etd=models.CharField(max_length=100,null=True)
    freight_charge=models.CharField(max_length=100,null=True)
    min_weight=models.CharField(max_length=100,null=True)
    pickup_availability=models.CharField(max_length=100,null=True)
    pod_available=models.CharField(max_length=100,null=True)
    rating=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)



class invoicedetails(models.Model):
    InvoiceNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    Invoicedate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    shipWeight=models.CharField(max_length=100,null=True)
    shipHeight=models.CharField(max_length=100,null=True)
    shipBreadth=models.CharField(max_length=100,null=True)
    shipLength=models.CharField(max_length=100,null=True)
    shipSurface=models.CharField(max_length=100,null=True)
    pinCodeAvailability=models.CharField(max_length=100,null=True)
    json=models.JSONField(null=True)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class validate_invoice_data(models.Model):
    InvoiceNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    Invoicedate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    shipWeight=models.CharField(max_length=100,null=True)
    shipHeight=models.CharField(max_length=100,null=True)
    shipBreadth=models.CharField(max_length=100,null=True)
    shipLength=models.CharField(max_length=100,null=True)
    shipSurface=models.CharField(max_length=100,null=True)
    pinCodeAvailability=models.CharField(max_length=100,null=True)
    json=models.JSONField(null=True)
    Remark=models.TextField()
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


class creditnotedetails(models.Model):
    CreditnoteNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    Creditnotedate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    json=models.JSONField(null=True)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class credit_check_availability(models.Model):
    CreditnoteNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    Creditnotedate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    json=models.JSONField(null=True)
    companyid=models.CharField(max_length=100,null=True)
    mode=models.CharField(max_length=100,default='SURFACE')
    availability=models.CharField(max_length=100)
    courier_agent=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class credit_popup_check_data(models.Model):
    statusid=models.CharField(max_length=100,null=True)
    courier_id=models.CharField(max_length=100,null=True)
    courier_name=models.CharField(max_length=100,null=True)
    etd=models.CharField(max_length=100,null=True)
    freight_charge=models.CharField(max_length=100,null=True)
    min_weight=models.CharField(max_length=100,null=True)
    pickup_availability=models.CharField(max_length=100,null=True)
    pod_available=models.CharField(max_length=100,null=True)
    rating=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class validate_credit_data(models.Model):
    CreditnoteNo=models.CharField(max_length=100)
    customername=models.CharField(max_length=100)
    Creditnotedate=models.CharField(max_length=100)
    frompincode=models.CharField(max_length=100)
    topincode=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    shippingaddress=models.CharField(max_length=254)
    json=models.JSONField(null=True)
    Remark=models.TextField()
    mode=models.CharField(max_length=100,null=True)
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class credit_awb(models.Model):
    status=models.CharField(max_length=100,null=True)
    CreditnoteNo=models.CharField(max_length=100)
    credit_data=models.JSONField()
    awb_data=models.JSONField()
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)


class invoice_awb(models.Model): 
    status=models.CharField(max_length=100,null=True)
    InvoiceNo=models.CharField(max_length=100)
    invoice_data=models.JSONField()
    awb_data=models.JSONField()
    dispatch_data=models.JSONField()
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

class invoice_awb_failed(models.Model): 
    status=models.CharField(max_length=100,null=True)
    InvoiceNo=models.CharField(max_length=100)
    invoice_data=models.JSONField()
    awb_data=models.JSONField()
    companyid=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    







