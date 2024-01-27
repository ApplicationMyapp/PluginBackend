from django.shortcuts import render
# Create your views here.
from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core import serializers
from rest_framework.parsers import JSONParser

from rest_framework import status
import datetime
from pytz import timezone
import pytz

import requests
import json
from .models import Shiprocketlogin,showorderdetails,check_availability_data,invoicedetails,creditnotedetails,credit_awb,invoice_awb,popup_check_data,credit_check_availability,credit_popup_check_data,validate_credit_data,validate_invoice_data,invoice_awb_failed
import pandas as pd

# from datetime import datetime

# new urls for sandbox and local use 
acc_login="https://booksapi.hostbooks.in/securitycenter/user/login"
acc_val_user="https://booksapi.hostbooks.in/securitycenter/user/validateUserLogin"
branch="https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url="https://booksapi.hostbooks.in/hostbook/api/transaction/data"
acc_update_url="https://booksapi.hostbooks.in/hostbook/api/update/transaction"

# for live server 
# acc_val_user="https://inapiaccounts.hostbooks.com/user/validateUserLogin"
# branch="https://in2accounts.hostbooks.com/api/master/list"
# acc_txn_url="https://in2accounts.hostbooks.com/api/transaction/data"
# acc_update_url="https://in2accounts.hostbooks.com/api/update/transaction"

# ////////************function for Accounting log in ****************/////////////////////////////////////////////

# accounting login and branch api for live and sandbox 
# branch api starts
@api_view(['GET', 'POST'])
def branchapi(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("branchapi get request in try")

        except:
            return Response("branchapi get request in except")


    if request.method == "POST":
        try:
            global compid,preserve,valuetoken
            compid=request.data['compid']
            preserve=request.data['preservekey']
            accounting = acc_val_user
            headers = {
                "x-version": "IND",
                "x-preserveKey":  preserve,
                "x-company":  compid,
                "x-forwarded-portal":  "true",
                "Content-Type": "application/json"
            }
            r = requests.get(accounting, headers=headers)
            token3 = r.json()
            valuetoken = token3['data']['user']['accessToken']
            url =branch

            payload = json.dumps({
                "page": 1,
                "limit": 20,
                "entityType": "BRANCH"
            })
            headers = {
                    "x-auth-token": valuetoken,
                    "x-preserveKey":  preserve,
                    "x-company":  compid,
                    "Content-Type": "application/json"
            }

            response = requests.post( url, headers=headers, data=payload)
            res=response.json()
            print(res)
            data=[]
            for x in res['data']['master']['list']:
                obj={}
                obj['branch']=x['name']
                obj['gstin']=x['gstin']
                obj['state']=x['branchAddress']['state']
                obj['city']=x['branchAddress']['city']
                obj['zip']=x['branchAddress']['zip']
                obj['address1']=x['branchAddress']['address1']


                data.append(obj)

            return Response(data)
        except:
            return Response("please fill all the required fields in your Branches")


# /////////////////////////*************Accounting login function ends *****************************///////////////////////////////
# branch api and account login  for local use 

# @api_view(['GET', 'POST'])
# def branchapi(request, **kwargs):
#     if request.method == "GET":
#         try:
#             return Response("branchapi get request in try")

#         except:
#             return HttpResponse("branchapi get request in except")


#     if request.method == "POST":
#         try:
#             global preserve,valuetoken,compid
#             url1 =acc_login
#             add_item = {
#                         # "username": "ashish.baranwal@hostbooks.com",
#                         # "password":  "12345678"
#                         # "username": "piyushqa2018a@gmail.com",
#                         # "password":  "test@123"
#                         # "username": "kalash.aggarwal@hostbooks.com",
#                         # "password":  "hostbooks@123"
#                         "username": "anilkashyap@burgerbae.in",
#                         "password":  "Bxbsocials#2023"
                        
#                     }
#             r = requests.post(url1, json=add_item)
#             token = r.json()
#             # print(token)
#             valuetoken = token['data']['user']['accessToken']
#             preserve = token['data']['user']['preserveKey']
#             # compid="389B7CCF-2F78-AC7B-ECD8-87FDEDE3E083"
#             # compid="89EC4CF1-864B-3C5C-33E1-1F69301FB8BA"
#             compid="3AEC0EB2-FF16-962F-952A-83848FC4723E"
#             print(valuetoken)
#             print(preserve)
#             url2 =acc_val_user
#             headers = {
#                 "x-version": "IND",
#                 "x-preserveKey":  preserve,
#                 # "x-company":  "F941FF61-7FAA-DD71-919B-1AE3F013013E",

#                 "x-company": compid,
#                 # "x-company":  companyUID,
#                 "x-forwarded-portal":  "true",
#                 "Content-Type": "application/json"
#             }
#             r = requests.get(url2, headers=headers)
#             # print("url2",r.json())
#             token3 = r.json()
#             url = branch
#             payload = json.dumps({
#                 "page": 1,
#                 "limit": 20,
#                 "entityType": "BRANCH"
#             })
#             headers = {
#                     "x-auth-token": valuetoken,
#                     "x-preserveKey":  preserve,
#                     "x-company":  compid,
#                     "Content-Type": "application/json"
#             }

#             response = requests.post( url, headers=headers, data=payload)
#             res=response.json()
#             print(res)
#             data=[]
#             for x in res['data']['master']['list']:
#                 obj={}
#                 obj['branch']=x['name']
#                 obj['gstin']=x['gstin']
#                 obj['state']=x['branchAddress']['state']
#                 obj['city']=x['branchAddress']['city']
#                 obj['zip']=x['branchAddress']['zip']
#                 obj['address1']=x['branchAddress']['address1']


#                 data.append(obj)

#             return Response(data)
#         except:
#             return Response("please fill all the required fields in your Branches")

# ////////////////////////////////shiprocket login starts /////////////////////////////////////////////////////////////////////////

@api_view(['GET', 'POST','PUT'])
def shiprocketlogin(request, **kwargs):
    if request.method == "GET":
        try:
            data=Shiprocketlogin.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("No Data Found")


    if request.method == "POST":
        try:
            # shiprocketlogin starts
            global shiptoken
            url1="https://apiv2.shiprocket.in/v1/external/auth/login"
            headers={
                "Content-Type":"application/json"
            }
            add_item={
                # "email": "piyushqa2018b@gmail.com",
                # "password": "Test@2022"
                "email": request.data['email'],
                "password": request.data['password']
            }
            r1 = requests.post(url1, json=add_item)
            res = r1.json()
            shiptoken=r1.json()['token']
            a=Shiprocketlogin(email=request.data['email'],password=request.data['password'],gstin=request.data['gstin'],branch=request.data['branch'],cemail=request.data['cemail'],cphone=request.data['cphone'], cname=request.data['cname'],companyid=compid,channelid=request.data['channelid'],pickup_location=request.data['pickup_location'],dimension_status=request.data['dimension'],weight=request.data['weight'],length=request.data['length'],breadth=request.data['breadth'],height=request.data['height'])
            a.save(using="shiprocket")
            return Response("LOGIN SUCCESSFULLY")

        except:
            return Response("UNAUTHORIZED ACCESS")

    if request.method == 'PUT':
        try:
            print(request.data['id'])
            print(request.data['email'])
            print(request.data['password'])
            print(request.data['gstin'])
            print(request.data['branch'])
            print(request.data['cemail'])
            print(request.data['cphone'])
            print(request.data['cname'])
            print(request.data['channelid'])
            print(request.data['pickup_location'])
            a=Shiprocketlogin.objects.using("shiprocket").filter(id=request.data['id']).update(email=request.data['email'],password=request.data['password'],gstin=request.data['gstin'],branch=request.data['branch'],cemail=request.data['cemail'],cphone=request.data['cphone'], cname=request.data['cname'],companyid=compid,channelid=request.data['channelid'],pickup_location=request.data['pickup_location'],dimension_status=request.data['dimension'],weight=request.data['weight'],length=request.data['length'],breadth=request.data['breadth'],height=request.data['height'])
            return Response("Account update successfully")
        except:
            return Response("Some data is missing Please fill data carefully")



@api_view(['GET', 'POST','DELETE'])
def show_order(request, **kwargs):
    if request.method == "GET":
        try:
            data=[]
            checked_data=check_availability_data.objects.using("shiprocket").filter(companyid=compid).values()
            if len(checked_data) == 0:
                salesorder=showorderdetails.objects.using("shiprocket").filter(companyid=compid).values()
                return Response(salesorder)
            else:
                for x in checked_data:
                    SalesOrderNo=x['SalesOrderNo']
                    sales=showorderdetails.objects.using("shiprocket").filter(companyid=compid).values()
                    salesdata=showorderdetails.objects.using("shiprocket").filter(SalesOrderNo=SalesOrderNo,companyid=compid)
                    salesdata.delete()
                for y in sales:
                    data.append(y)
                return Response(data)
            # salesorder=showorderdetails.objects.filter(companyid=compid).values()
            # return Response(salesorder)

        except:
            return HttpResponse("Getting Data...........Unsuccessful")


    if request.method == "POST":
        try:
           
            # Accountinglogin()
            # print(request.data)
            startdate=request.data['startdate']
            enddate=request.data['enddate']
            sd= datetime.datetime.strptime(startdate,"%Y-%m-%dT%H:%M:%S.%fZ")
            snd=str(sd.astimezone(timezone('Asia/Kolkata')).date())
            newdat=snd.split("-")
            newstartdate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(newstartdate)
            ed= datetime.datetime.strptime(enddate,"%Y-%m-%dT%H:%M:%S.%fZ")
            end=str(ed.astimezone(timezone('Asia/Kolkata')).date())
            newdat=end.split("-")
            newenddate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(newenddate)
            print(valuetoken)
            print(preserve)
            print(compid)
            url3 = acc_txn_url
            payload={
                "txnShipmentDataFlag": 1,
                "startDate": str(newstartdate),
                # "endDate": "09-12-2022",
                "endDate": str(newenddate),
                "webhook": 1,
                "page": 1,
                "limit": 20
                }
            headers={
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid

            }
            r1 = requests.post(url3, json=payload,  headers=headers)
            res=r1.json()
            print(res)
            shipments=res['data']['transaction']['txnShipmentData']
            if shipments != None or shipments != []:
                a=showorderdetails.objects.all()
                a.delete()
                for x in shipments:
                    print(x)
                    pinCodeAvailability=x['pinCodeAvailability']
                    if pinCodeAvailability == False:
                        print("if condition")
                        shipmentno=x['number']
                        weight=x['weight']
                        length=x['length']
                        breadth=x['breadth']
                        height=x['height']
                        SalesOrderNo=x['salesOrder']['number']
                        # print("kalash in show shipments")
                        customername=x['salesOrder']['shipCustomerName']
                        # ['shipBillingName']
                        orderdate=int(x['date'])
                        my_datetime = datetime.datetime.fromtimestamp(orderdate / 1000)
                        zone=my_datetime.astimezone(timezone('Asia/Kolkata'))
                        dat=zone.strftime("%Y-%m-%d")
                        newdat=dat.split("-")
                        newdate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
                        ordertype=x['salesOrder']['shipmentDetail']['shipPaymentType']
                        frompincode=x['salesOrder']['branch']['branchAddress']['zip']
                        topincode=x['salesOrder']['shipAddress']['zip']
                        state=x['salesOrder']['shipAddress']['state']
                        city=x['salesOrder']['shipAddress']['city']
                        shippingaddress=x['salesOrder']['shipAddress']['address1']
                        posted_at= datetime.datetime.now()
                        a=showorderdetails(SalesOrderNo=SalesOrderNo,customername=customername,frompincode=frompincode,topincode=topincode,orderdate=newdate,state=state, city=city, shippingaddress=shippingaddress,posted_at=posted_at,ordertype=ordertype,weight=weight,length=length,breadth=breadth,height=height,shipmentno=shipmentno,companyid=compid)
                        a.save(using="shiprocket")
                        print("data saved successfully")
                    else:
                        print(f"{x['salesOrder']['number']} has availability")
                return Response("Shipments fetch Successfully")
            else:
                return Response("No Data Found")
        except:
            return Response("Get Shipments Failed Because some data is missing in sales order from HB Accounting or you did not choose date range")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=showorderdetails.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Shipment Delete Successfully")
        except:
            return Response("Shipment Delete Failed")



@api_view(['GET', 'POST','PUT','DELETE'])
def check_availability(request, **kwargs):
    if request.method == "GET":
        try:
            data=check_availability_data.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return HttpResponse("check_availability get request in except")


    if request.method == "POST":
        try:
            if request.data != []:
                for x in request.data:
                    print("check")
                    cod=x['ordertype']
                    if cod == "paid":
                        cod=0
                    else:
                        cod=1
                    if x['dimension_status'] == "Custom":
                        weight=x['cusweight']
                        length=x['cuslength']
                        breadth=x['cusbreadth']
                        height=x['cusheight']
                    else:
                        weight=x['weight']
                        length=x['length']
                        breadth=x['breadth']
                        height=x['height']
                    # shiprocketlogin starts
                    url1="https://apiv2.shiprocket.in/v1/external/auth/login"
                    headers={
                        "Content-Type":"application/json"
                    }
                    add_item={
                        "email": x['email'],
                        "password":x['pwd']
                        # "email": request.data['email'],
                        # "password": request.data['password']
                    }
                    r1 = requests.post(url1, json=add_item)
                    res = r1.json()
                    # print("this is data for check availibility-----------",res)
                    shiptoken=r1.json()['token']
                    url2="https://apiv2.shiprocket.in/v1/external/courier/serviceability"
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer" + shiptoken
                    }
                    add_item={
                        "pickup_postcode": x['frompincode'],
                        "delivery_postcode": x['topincode'],
                        "cod":cod,
                        "weight":weight,
                        "mode": x['mode'],
                    }
                    r2 = requests.get(url2, json=add_item ,headers=headers)
                    res = r2.json()
                    print("kalash is here ")
                    print(res)
                    SalesOrderNo=x['SalesOrderNo']
                    customername=x['customername']
                    orderdate= x['orderdate']
                    ordertype=x['ordertype']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    mode=x['mode']
                    returnable=x['returnable']
                    weight=weight
                    lengthorder=length
                    breadth=breadth
                    height=height
                    shipment=x['shipmentno']
                    length=len(res)
                    if length == 2 or length == 3:
                        availability="NO"
                        courier_agent=res['message']
                        a=check_availability_data(SalesOrderNo=SalesOrderNo,customername=customername,orderdate=orderdate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,ordertype=ordertype,mode=mode,availability=availability,returnable=returnable,courier_agent=courier_agent,weight=weight,length=lengthorder,breadth=breadth,height=height,shipmentno=shipment,companyid=compid)
                        a.save(using="shiprocket")
                    else:
                        availability="YES"
                        if res['data']['shiprocket_recommended_courier_id'] != None:                            
                            courierid= res['data']['shiprocket_recommended_courier_id']
                        else:
                            courierid=""
                        availcomp=res['data']['available_courier_companies']
                        for x in availcomp:
                            availid=x['courier_company_id']
                            couriername=x['courier_name']
                            if availid == courierid:
                                courier_agent=str(courierid)+"-"+couriername
                            status_id=SalesOrderNo
                            etd=x['etd']
                            freight_charge=x['freight_charge']
                            min_weight=x['min_weight']
                            pickup_availability=x['pickup_availability']
                            pod_available=x['pod_available']
                            rating=x['rating']
                            b=popup_check_data(statusid=status_id,courier_id=availid,courier_name=couriername,etd=etd,freight_charge=freight_charge,min_weight=min_weight,pickup_availability=pickup_availability,pod_available=pod_available,rating=rating)
                            b.save(using="shiprocket") 
                            print("data saved")
                        a=check_availability_data(SalesOrderNo=SalesOrderNo,customername=customername,orderdate=orderdate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,ordertype=ordertype,mode=mode,availability=availability,returnable=returnable,courier_agent=courier_agent,weight=weight,length=lengthorder,breadth=breadth,height=height,shipmentno=shipment,companyid=compid)
                        a.save(using="shiprocket")
                    b=showorderdetails.objects.using("shiprocket").filter(SalesOrderNo=SalesOrderNo,companyid=compid)
                    b.delete()
                return Response("Availability Check Successfully")
            else:
                return Response("Please Select Shipment for Availability Check")
        except:
            print("i am in except")
            return Response("Availability Check Failed!!!")
    
    if request.method == "PUT":
        try:
            id=request.data['status_id']
            name=request.data['name']
            a=check_availability_data.objects.using("shiprocket").filter(SalesOrderNo=id,companyid=compid).update(courier_agent=name)
            return Response("Update Courier Agent Successfully.....")
        except:
            return Response("Update Courier Agent Failed!!!")
    
    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=check_availability_data.objects.using("shiprocket").filter(id=id)
                for row in a.values():
                    salesorderno=row['SalesOrderNo']
                    b=popup_check_data.objects.using('shiprocket').filter(statusid=salesorderno)
                    print("kalash in loop")
                    b.delete()
                a.delete()
            return Response("Shipment Delete Successfully")
        except:
            return Response("Shipment Delete Failed")



@api_view(['GET', 'POST','DELETE'])
def get_invoice(request, **kwargs):
    if request.method == "GET":
        try:
            data=[]
            awb_data=invoice_awb.objects.using("shiprocket").filter(companyid=compid).values()
            if len(awb_data) == 0:
                invoice=invoicedetails.objects.using("shiprocket").filter(companyid=compid).values()
                return Response(invoice)
            else:
                for x in awb_data:
                    InvoiceNo=x['InvoiceNo']
                    invoice=invoicedetails.objects.using("shiprocket").filter(companyid=compid).values()
                    invoicedata=invoicedetails.objects.using("shiprocket").filter(InvoiceNo=InvoiceNo,companyid=compid)
                    invoicedata.delete()
                for y in invoice:
                    # print(y)
                    data.append(y)
                # print(data)
                return Response(data)
            # invoice=invoicedetails.objects.filter(companyid=compid).values()
            # return Response(invoice)

        except:
            return Response("get_invoice get request in except")


    if request.method == "POST":
        try:
            # ///////////////////////////////////Accounting Login //////////////////////////////////////////////////
            # Accountinglogin()
            print(request.data)
            startdate=request.data['stdate']
            enddate=request.data['endate']
            sd= datetime.datetime.strptime(startdate,"%Y-%m-%dT%H:%M:%S.%fZ")
            snd=str(sd.astimezone(timezone('Asia/Kolkata')).date())
            newdat=snd.split("-")
            INV_newstartdate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(INV_newstartdate)
            ed= datetime.datetime.strptime(enddate,"%Y-%m-%dT%H:%M:%S.%fZ")
            end=str(ed.astimezone(timezone('Asia/Kolkata')).date())
            newdat=end.split("-")
            INV_newenddate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(INV_newenddate)
            print(valuetoken)
            print(preserve)
            print(compid)

            # //////////////////////////////Accounting LOgin end ///////////////////////////////////////////////////
            url3 =acc_txn_url
            payload={
                "invoiceDataFlag": 1,
                "startDate": str(INV_newstartdate),
                "endDate": str(INV_newenddate),
                "webhook": 1,
                "page": 1,
                "limit": 20
                }
            headers={
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid

            }
            r1 = requests.post(url3, json=payload,  headers=headers)
            res=r1.json()
            print(res)
            df = pd.DataFrame(res)
            invoicedata=df['data']['transaction']['invoiceData']
            if invoicedata != []:
                a=invoicedetails.objects.all()
                a.delete()
                for x in invoicedata:
                    if x['shipmentDetail']['awbNumber'] is None:
                        InvoiceNo=x['number']
                        customername=x['contact']['name']
                        datetime_str=x['date']/1000
                        Invoicedate= datetime.datetime.fromtimestamp(datetime_str).astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
                        frompincode=x['branch']['branchAddress']['zip']
                        topincode=x['shipAddress']['zip']
                        state=x['shipAddress']['state']
                        city=x['shipAddress']['city']
                        shippingaddress=x['shipAddress']['address1']
                        shipLength=x['shipmentDetail']['shipLength']
                        shipBreadth=x['shipmentDetail']['shipBreadth']
                        shipHeight=x['shipmentDetail']['shipHeight']
                        shipWeight=x['shipmentDetail']['shipWeight']
                        pinCodeAvailability=x['shipmentDetail']['pinCodeAvailability']
                        shipSurface=x['shipmentDetail']['shipSurface']
                        jsonn=x
                        a=invoicedetails(InvoiceNo=InvoiceNo,customername=customername,Invoicedate=Invoicedate,frompincode=frompincode,topincode=topincode,state=state, city=city, shippingaddress=shippingaddress,shipLength=shipLength,shipBreadth=shipBreadth,shipHeight=shipHeight,shipWeight=shipWeight,pinCodeAvailability=pinCodeAvailability,shipSurface=shipSurface,json=jsonn,companyid=compid)
                        a.save(using="shiprocket")
                    else:
                        print(f"{x['number']} has AWB number already")
                return Response("Invoices fetch Successfully")
            else:
                return Response("No Data Found")
        except:
            print("i am in except")
            return Response("Invoices fetch failed because either you forgot to choose date range or some data did not fill in invoice like shipping address etc.")
    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=invoicedetails.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Invoice Delete Successfully")
        except:
            return Response("Invoice Delete Failed")



@api_view(['GET', 'POST','DELETE'])
def get_creditnote(request, **kwargs):
    if request.method == "GET":
        try:
            data=[]
            checked_data=credit_awb.objects.using("shiprocket").filter(companyid=compid).values()
            if len(checked_data) == 0:
                salesorder=creditnotedetails.objects.using("shiprocket").filter(companyid=compid).values()
                return Response(salesorder)
            else:
                for x in checked_data:
                    CreditnoteNo=x['CreditnoteNo']
                    sales=creditnotedetails.objects.using("shiprocket").filter(companyid=compid).values()
                    salesdata=creditnotedetails.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                    salesdata.delete()
                for y in sales:
                    data.append(y)
                return Response(data)
            # salesorder=creditnotedetails.objects.filter(companyid=compid).values()
            # return Response(salesorder)
        except:
            return Response("get_creditnote get request in except")


    if request.method == "POST":
        try:
            print(request.data)
            startdate=request.data['startdate']
            enddate=request.data['enddate']
            sd= datetime.datetime.strptime(startdate,"%Y-%m-%dT%H:%M:%S.%fZ")
            snd=str(sd.astimezone(timezone('Asia/Kolkata')).date())
            newdat=snd.split("-")
            newstartdate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(newstartdate)
            ed= datetime.datetime.strptime(enddate,"%Y-%m-%dT%H:%M:%S.%fZ")
            end=str(ed.astimezone(timezone('Asia/Kolkata')).date())
            newdat=end.split("-")
            newenddate=newdat[2]+"-"+newdat[1]+"-"+newdat[0]
            print(newenddate)
            # ///////////////////////////////////Accounting Login //////////////////////////////////////////////////
            # Accountinglogin()
            # //////////////////////////////Accounting LOgin end ///////////////////////////////////////////////////
            url3 = acc_txn_url
            payload={
                "creditNoteDataFlag": 1,
                "startDate": str(newstartdate),
                "endDate": str(newenddate),
                "webhook": 1,
                "page": 1,
                "limit": 20
                }
            headers={
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid

            }
            r1 = requests.post(url3, json=payload,  headers=headers)
            res=r1.json()
            print(res)
            creditNoteData=res['data']['transaction']['creditNoteData']
            if creditNoteData != []:
                a=creditnotedetails.using("shiprocket").objects.all()
                a.delete()
                for x in creditNoteData:
                    try:
                        if x['shipmentDetail']['awbNumber'] is None:
                            CreditnoteNo=x['number']
                            customername=x['contact']['name']
                            datetime_str=x['date']/1000
                            Creditnotedate= datetime.datetime.fromtimestamp(datetime_str).astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
                            frompincode=x['branch']['branchAddress']['zip']
                            topincode=x['billAddress']['zip']
                            state=x['billAddress']['state']
                            city=x['billAddress']['city']
                            shippingaddress=x['billAddress']['address1']
                            jsonn=x
                            a=creditnotedetails(CreditnoteNo=CreditnoteNo,customername=customername,Creditnotedate=Creditnotedate,frompincode=frompincode,topincode=topincode,state=state, city=city, shippingaddress=shippingaddress,json=jsonn,companyid=compid)
                            a.save(using="shiprocket")
                        else:
                            print(f"{x['number']} has AWB Number already")
                    except Exception as e:
                        print(e)
                return Response("Credit Note Fetch Successfully")   
            else:
                return Response("No Data Found")   
        except:
            print("i am in except")
            return Response("Please Select Date Range ")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=creditnotedetails.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Credit Note Delete Successfully")
        except:
            return Response("Credit Note Delete Failed")



@api_view(['GET', 'POST','PUT','DELETE'])
def credit_availabilitycheck(request, **kwargs):
    if request.method == "GET":
        try:
            data=credit_check_availability.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("check_availability get request in except")


    if request.method == "POST":
        try:
            if request.data != []:
                for x in request.data:
                    print("check--------------",x)
                    # cod=x['json']['shipmentDetail']['shipPaymentType']
                    # if cod == "paid":
                    #     cod=0
                    # else:
                    #     cod=1
                    if x['dimension_status'] == "Custom":
                        weight=x['weight']
                        mode='Surface'
                    else:
                        weight=x['json']['shipmentDetail']['shipWeight']
                        mode=x['json']['shipmentDetail']['shipSurface']

                    # shiprocketlogin starts
                    url1="https://apiv2.shiprocket.in/v1/external/auth/login"
                    headers={
                        "Content-Type":"application/json"
                    }
                    add_item={
                        "email": x['email'],
                        "password":x['password']
                        # "email": request.data['email'],
                        # "password": request.data['password']
                    }
                    r1 = requests.post(url1, json=add_item)
                    res = r1.json()
                    # print("this is data for check availibility-----------",res)
                    shiptoken=r1.json()['token']
                    url2="https://apiv2.shiprocket.in/v1/external/courier/serviceability"
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer" + shiptoken
                    }
                    add_item={
                        "pickup_postcode": x['topincode'],
                        "delivery_postcode": x['frompincode'],
                        "cod":0,
                        "weight":weight,
                        # "mode": x['json']['shipmentDetail']['shipSurface'],
                        "mode":mode,
                        # "is_return":1
                    }

                    r2 = requests.get(url2, json=add_item ,headers=headers)
                    res = r2.json()
                    print("-----------------Amar is here ---------------")
                    print(res)
                    CreditnoteNo=x['CreditnoteNo']
                    customername=x['customername']
                    Creditnotedate=x['Creditnotedate']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    jsonn=x['json']
                    # mode=x['json']['shipmentDetail']['shipSurface']
                    mode=mode
                    length=len(res)
                    if length == 2 or length == 3:
                        availability="NO"
                        courier_agent=res['message']
                        a=credit_check_availability(CreditnoteNo=CreditnoteNo,customername=customername,Creditnotedate=Creditnotedate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,companyid=compid,json=jsonn,mode="Surface",availability=availability,courier_agent=courier_agent)
                        a.save(using="shiprocket")
                    else:
                        availability="YES"
                        courierid= res['data']['shiprocket_recommended_courier_id']
                        availcomp=res['data']['available_courier_companies']
                        courier_agent=""
                        for x in availcomp:
                            availid=x['courier_company_id']
                            couriername=x['courier_name']
                            if availid == courierid:
                                courier_agent=str(courierid)+"-"+couriername
                            status_id=CreditnoteNo
                            etd=x['etd']
                            freight_charge=x['freight_charge']
                            min_weight=x['min_weight']
                            pickup_availability=x['pickup_availability']
                            pod_available=x['pod_available']
                            rating=x['rating']
                            b=credit_popup_check_data(statusid=status_id,courier_id=availid,courier_name=couriername,etd=etd,freight_charge=freight_charge,min_weight=min_weight,pickup_availability=pickup_availability,pod_available=pod_available,rating=rating)
                            b.save(using="shiprocket") 
                            print("data saved")
                        a=credit_check_availability(CreditnoteNo=CreditnoteNo,customername=customername,Creditnotedate=Creditnotedate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,companyid=compid,json=jsonn,mode="Surface",availability=availability,courier_agent=courier_agent)
                        a.save(using="shiprocket")
                    b=creditnotedetails.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                    b.delete()
                return Response("Availability Check Successfully")
            else:
                return Response("Please Select Credit Note for Availability Check")
        except Exception as e:
            print("i am in except-----------",e)
            return Response("Availability Check Failed!!!")
    
    if request.method == "PUT":
        try:
            id=request.data['status_id']
            name=request.data['name']
            a=credit_check_availability.objects.using("shiprocket").filter(CreditnoteNo=id,companyid=compid).update(courier_agent=name)
            return Response("Update Courier Agent Successfully.....")
        except:
            return Response("Update Courier Agent Failed!!!")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=credit_check_availability.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Credit Note Delete Successfully")
        except:
            return Response("Credit Note Delete Failed")


# Starts API for AWB Generation of Invoice 

@api_view(['GET', 'POST','DELETE'])
def generate_awb_invoice(request, **kwargs):
    if request.method == "GET":
        try:
            data=invoice_awb.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("generate_awb_invoice get request except ")


    if request.method == "POST":
        try:
            for x in request.data:
                invoiceno=x['InvoiceNo']
                channelid=x['channelid']
                pickloc=x['pickloc']
                customername=x['customername']
                Invoicedate=x['Invoicedate']
                frompincode=x['frompincode']
                topincode=x['topincode']
                jsonnn=x['json']
                cemail=x['cemail']
                cphone=x['cphone']
                cname=x['cname']
                email=x['email']
                password=x['password']
                dimension_status=x['dimension_status']
                if dimension_status == "Custom":
                    weight=x['weight']
                    length=x['length']
                    breadth=x['breadth']
                    height=x['height']
                else:
                    length=jsonnn['shipmentDetail']['shipLength'] 
                    breadth=jsonnn['shipmentDetail']['shipBreadth']
                    height=jsonnn['shipmentDetail']['shipHeight']
                    weight=jsonnn['shipmentDetail']['shipWeight']
                print("kalash is here ---------------------------")
                func=awb_invoicedata(jsonnn,channelid,pickloc,cemail,cphone,cname,email,password,weight,length,breadth,height)
                print(func)
                if 'status_code' in func:
                    status=func['status_code']
                else:
                    status=func['status']
                if status == 1:
                    status="Generated"
                    print("I am in save awb number")
                    a=invoice_awb(status=status,InvoiceNo=invoiceno,invoice_data=x,awb_data=func,dispatch_data="null",companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_invoice_data.objects.using("shiprocket").filter(InvoiceNo=invoiceno,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                elif status == 0:
                    status="Failed"
                    func['payload']['order_created']="Nil"
                    func['payload']['awb_generated']="Nil"
                    func['payload']['label_generated']="Nil"
                    func['payload']['pickup_generated']="Nil"
                    print("I am in save awb number")
                    a=invoice_awb_failed(status=status,InvoiceNo=invoiceno,invoice_data=x,awb_data=func,companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_invoice_data.objects.using("shiprocket").filter(InvoiceNo=invoiceno,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                else:
                    status="Failed"
                    func['payload']={}
                    func['payload']['order_created']="Nil"
                    func['payload']['awb_generated']="Nil"
                    func['payload']['label_generated']="Nil"
                    func['payload']['pickup_generated']="Nil"
                    func['payload']['message']=func['message']
                    for error in func['errors'].keys():
                        func['payload'][error]=func['errors'][error]
                    print("I am in save awb number")
                    a=invoice_awb_failed(status=status,InvoiceNo=invoiceno,invoice_data=x,awb_data=func,companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_invoice_data.objects.using("shiprocket").filter(InvoiceNo=invoiceno,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                print(func)
            return Response("Generate AWB Successfully.......")      
        except:
            return Response("Generation of AWB Failed!!!")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=invoice_awb.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Invoice Delete Successfully")
        except:
            return Response("Invoice Delete Failed")


def awb_invoicedata(y,channelid,pickloc,cemail,cphone,cname,email,passwrd,weight,length,breadth,height):
     # shiprocketlogin starts
    global shiptoken
    url1="https://apiv2.shiprocket.in/v1/external/auth/login"
    headers={
        "Content-Type":"application/json"
    }
    add_item={
        "email": email,
        "password": passwrd
        # "email": request.data['email'],
        # "password": request.data['password']
    }
    r1 = requests.post(url1, json=add_item)
    res = r1.json()
    shiptoken=r1.json()['token']
    print("klash is her------------------------")
    url2="https://apiv2.shiprocket.in/v1/external/shipments/create/forward-shipment"
    headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer" + shiptoken
                }
    payment_method=y['shipmentDetail']['shipPaymentType']
    if payment_method == "Paid":
        payment_method="Prepaid"
    else:
        payment_method="COD"
    datetime_str=y['date']/1000
    orderdate= datetime.datetime.fromtimestamp(datetime_str).strftime('%Y-%m-%d')
    item_array=[]
    for item in y['lineItems']:
        obj={}
        obj={
                            "name":item['proInventory']['name'],                                           
                            "sku":item['proInventory']['inventoryCode'],
                            "units": item['quantity'],
                            # "hsn": y['lineItems'][0]['hsnSac'],
                            "selling_price":item['unitPrice'],
                            # "tax":y['lineItems'][0]['gstAmount'], 
                            # "discount": y['lineItems'][0]['discountAmount'] + y['lineItems'][0]['addDiscountAmount']
            }
        item_array.append(obj)
    json_item={
                "courier_id":"",
                "order_id":y['number'],
                "order_date": orderdate,
                "channel_id": channelid,
                # "billing_customer_name": y['contact']['name'],
                "billing_customer_name": y['billAddress']['name'],
                "billing_last_name":"",
                # "billing_email": y['contact']['contactPerson'][0]['emailAddress'],
                "billing_email": y['billAddress']['email'],
                "billing_address": y['billAddress']['address1'],
                "billing_city": y['billAddress']['city'],
                "billing_pincode": y['billAddress']['zip'],
                "billing_state": y['billAddress']['state'], 
                "billing_country": y['billAddress']['country'], 
                "billing_phone":y['billAddress']['mobile'],
                "shipping_is_billing": False,
                # "shipping_customer_name":y['contact']['name'],
                "shipping_customer_name":y['shipAddress']['name'],
                "shipping_address": y['shipAddress']['address1'],
                "shipping_city": y['shipAddress']['city'], 
                "shipping_state": y['shipAddress']['state'],
                "shipping_country": y['shipAddress']['country'],
                "shipping_pincode": y['shipAddress']['zip'], 
                "shipping_email": y['shipAddress']['email'],
                "shipping_phone":y['shipAddress']['mobile'], 
                "order_items": item_array,
                "payment_method": payment_method, 
                "sub_total": y['totalTaxableAmount'],
                "length": length, 
                "breadth": breadth, 
                "height": height, 
                "weight":weight, 
                "pickup_location": pickloc, 
                # "customer_gstin": "y['customerGstin']",
                "customer_gstin": y['companyGstin'],
                "vendor_details": {
                        "email":cemail,
                        "phone": cphone, 
                        "name":cname,
                        "address": y['branch']['branchAddress']['address1'], 
                        "city": y['branch']['branchAddress']['city'], 
                        "state": y['branch']['branchAddress']['state'], 
                        "country": y['branch']['branchAddress']['country'],
                        "pin_code":y['branch']['branchAddress']['zip'],
                        "pickup_location": pickloc                }
    }
    print("kalsh in function -------------------------------")
    r2 = requests.post(url2, json=json_item,headers=headers)
    res = r2.json()
    return res


#API for validation data in credit note for AWB Generation 
@api_view(['GET', 'POST','DELETE'])
def validateinvoice(request, **kwargs):
    if request.method == "GET":
        try:
            data=validate_invoice_data.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("validateinvoice get request in except")


    if request.method == "POST":
        try:
            # print(request.data)
            for x in request.data:
                item_array=[]
                if "lineItems" in x['json']:
                    for item in x['json']['lineItems']:
                        obj={}
                        obj={
                            "name":item['proInventory']['name'] or "null",                                          
                            "sku":item['proInventory']['inventoryCode'] or "null",
                            "units": item['quantity'] or "null",
                            # "hsn": y['lineItems'][0]['hsnSac'],
                            "selling_price":item['unitPrice'] or "null",
                            # "tax":y['lineItems'][0]['gstAmount'], 
                            # "discount": y['lineItems'][0]['discountAmount'] + y['lineItems'][0]['addDiscountAmount']
                            }
                        item_array.append(obj)
                obj={
                            "courier_id":"",
                            "order_id":x['InvoiceNo'] or "null",
                            "order_date":x['Invoicedate'] or "null",
                            "channel_id": x['channelid'] or "null",
                            # "billing_customer_name": y['contact']['name'],
                            "billing_customer_name": x['json']['billAddress']['name'] or "null",
                            "billing_last_name":"",
                            # "billing_email": y['contact']['contactPerson'][0]['emailAddress'],
                            "billing_email": x['json']['billAddress']['email'] or "null",
                            "billing_address": x['json']['billAddress']['address1'] or "null",
                            "billing_city": x['json']['billAddress']['city'] or "null",
                            "billing_pincode": x['json']['billAddress']['zip'] or "null",
                            "billing_state": x['json']['billAddress']['state'] or "null",
                            "billing_country": x['json']['billAddress']['country'] or "null", 
                            "billing_phone":x['json']['billAddress']['mobile'] or "null",
                            "shipping_is_billing": False,
                            # "shipping_customer_name":y['contact']['name'],
                            "shipping_customer_name":x['json']['shipAddress']['name'] or "null",
                            "shipping_address": x['json']['shipAddress']['address1'] or "null",
                            "shipping_city": x['json']['shipAddress']['city'] or "null",
                            "shipping_state": x['json']['shipAddress']['state'] or "null",
                            "shipping_country": x['json']['shipAddress']['country'] or "null",
                            "shipping_pincode": x['json']['shipAddress']['zip'] or "null",
                            "shipping_email": x['json']['shipAddress']['email'] or "null",
                            "shipping_phone":x['json']['shipAddress']['mobile'] or "null", 
                            "order_items": item_array,
                            "payment_method": x['json']['shipmentDetail']['shipPaymentType'] or "null", 
                            "sub_total": x['json']['totalTaxableAmount'] or "null",
                            "length": x['shipLength'] or "null",
                            "breadth": x['shipBreadth'] or "null",
                            "height": x['shipHeight'] or "null",
                            "weight":x['shipWeight'] or "null",
                            "pickup_location": x['pickloc'] or "null",
                            # "customer_gstin": "y['customerGstin']",
                            "customer_gstin": x['json']['companyGstin'] or "null",
                            "vendor_details": {
                                    "email":x['cemail'] or "null",
                                    "phone": x['cphone'] or "null",
                                    "name":x['cname'] or "null",
                                    "address": x['json']['branch']['branchAddress']['address1'] or "null",
                                    "city": x['json']['branch']['branchAddress']['city'] or "null",
                                    "state": x['json']['branch']['branchAddress']['state'] or "null",
                                    "country": x['json']['branch']['branchAddress']['country'] or "null",
                                    "pin_code":x['json']['branch']['branchAddress']['zip'] or "null",
                                    "pickup_location": x['pickloc'] or "null"
                                               }
                }
                Remark=""
                for key in obj.keys():
                    if obj[key] == "null" or obj[key] == []:
                        Remark+=key + ","
                    else:
                        pass
                if Remark == "":
                    InvoiceNo=x['InvoiceNo']
                    customername=x['customername']
                    Invoicedate=x['Invoicedate']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    shipLength=x['shipLength']
                    shipBreadth=x['shipBreadth']
                    shipHeight=x['shipHeight']
                    shipWeight=x['shipWeight']
                    pinCodeAvailability=x['pinCodeAvailability']
                    shipSurface=x['shipSurface']
                    jsonn=x['json']
                    message="Data Validated Successfully"
                    a=validate_invoice_data(InvoiceNo=InvoiceNo,customername=customername,Invoicedate=Invoicedate,frompincode=frompincode,topincode=topincode,state=state, city=city, shippingaddress=shippingaddress,shipLength=shipLength,shipBreadth=shipBreadth,shipHeight=shipHeight,shipWeight=shipWeight,pinCodeAvailability=pinCodeAvailability,shipSurface=shipSurface,json=jsonn,companyid=compid,Remark=message)
                    a.save()
                else:
                    InvoiceNo=x['InvoiceNo']
                    customername=x['customername']
                    Invoicedate=x['Invoicedate']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    shipLength=x['shipLength']
                    shipBreadth=x['shipBreadth']
                    shipHeight=x['shipHeight']
                    shipWeight=x['shipWeight']
                    pinCodeAvailability=x['pinCodeAvailability']
                    shipSurface=x['shipSurface']
                    jsonn=x['json']
                    message=Remark + "have null value So please fill their values"
                    a=validate_invoice_data(InvoiceNo=InvoiceNo,customername=customername,Invoicedate=Invoicedate,frompincode=frompincode,topincode=topincode,state=state, city=city, shippingaddress=shippingaddress,shipLength=shipLength,shipBreadth=shipBreadth,shipHeight=shipHeight,shipWeight=shipWeight,pinCodeAvailability=pinCodeAvailability,shipSurface=shipSurface,json=jsonn,companyid=compid,Remark=message)
                    a.save(using="shiprocket")
                b=invoicedetails.objects.using("shiprocket").filter(InvoiceNo=x['InvoiceNo'],companyid=compid)
                b.delete()
            return Response("Data Validation Successful")
        except Exception as e:
            print("\nerror is --------------------------",e)
            return Response("Data Validation failed")
    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=validate_invoice_data.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Invoice Delete Successfully")
        except:
            return Response("Invoice Delete Failed")


# starts API for AWB Generation of credit note 

@api_view(['GET', 'POST','DELETE'])
def generate_awb_creditnote(request, **kwargs):
    if request.method == "GET":
        try:
            data=credit_awb.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("generate_awb_creditnote get request except ")


    if request.method == "POST":
        try:
            for x in request.data:
                CreditnoteNo=x['CreditnoteNo']
                channelid=x['channelid']
                pickloc=x['pickloc']
                customername=x['customername']
                Creditnotedate=x['Creditnotedate']
                frompincode=x['frompincode']
                topincode=x['topincode']
                jsonnn=x['json']
                cemail=x['cemail']
                cphone=x['cphone']
                cname=x['cname']
                email=x['email']
                password=x['password']
                dimension_status=x['dimension_status']
                if dimension_status == "Custom":
                    weight=x['weight']
                    length=x['length']
                    breadth=x['breadth']
                    height=x['height']
                else:
                    length=jsonnn['shipmentDetail']['shipLength'] 
                    breadth=jsonnn['shipmentDetail']['shipBreadth']
                    height=jsonnn['shipmentDetail']['shipHeight']
                    weight=jsonnn['shipmentDetail']['shipWeight']
                print("kalash is here ---------------------------")
                func=awb_creditnotedata(jsonnn,channelid,pickloc,cemail,cphone,cname,email,password,weight,length,breadth,height)
                # print(func)
                if 'status_code' in func:
                    status=func['status_code']
                else:
                    status=func['status']
                if status == 1:
                    status="Success"
                    print("I am in save awb number")
                    a=credit_awb(status=status,CreditnoteNo=CreditnoteNo,credit_data=x,awb_data=func,companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_credit_data.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                elif status == 0:
                    status="Failed"
                    func['payload']['order_created']="Nil"
                    func['payload']['awb_generated']="Nil"
                    # func['payload']['label_generated']="Nil"
                    func['payload']['pickup_generated']="Nil"
                    print("I am in save awb number")
                    a=credit_awb(status=status,CreditnoteNo=CreditnoteNo,credit_data=x,awb_data=func,companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_credit_data.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                else:
                    status="Failed"
                    func['payload']={}
                    func['payload']['order_created']="Nil"
                    func['payload']['awb_generated']="Nil"
                    # func['payload']['label_generated']="Nil"
                    func['payload']['pickup_generated']="Nil"
                    func['payload']['message']=func['message']
                    for error in func['errors'].keys():
                        func['payload'][error]=func['errors'][error]
                    print("I am in save awb number")
                    a=credit_awb(status=status,CreditnoteNo=CreditnoteNo,credit_data=x,awb_data=func,companyid=compid)
                    a.save(using="shiprocket")
                    print("data saved")
                    b=validate_credit_data.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                    b.delete()
                    print("delete data from nginvoice")
                print(func)
            return Response("Generate AWB Successfully.......")      
        except:
            return Response("Generation of AWB Failed!!!")
    
    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=credit_awb.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Credit Note Delete Successfully")
        except:
            return Response("Credit Note Delete Failed")


def awb_creditnotedata(y,channelid,pickloc,cemail,cphone,cname,email,passwrd,weight,length,breadth,height):
     # shiprocketlogin starts
    global shiptoken
    url1="https://apiv2.shiprocket.in/v1/external/auth/login"
    headers={
        "Content-Type":"application/json"
    }
    add_item={
        "email": email,
        "password": passwrd
        # "email": request.data['email'],
        # "password": request.data['password']
    }
    r1 = requests.post(url1, json=add_item)
    res = r1.json()
    shiptoken=r1.json()['token']
    print("klash is her------------------------")
    url2="https://apiv2.shiprocket.in/v1/external/shipments/create/return-shipment"
    headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer" + shiptoken
                }
    # payment_method=y['category']['options']
    # if payment_method == "Paid":
    #     payment_method="Prepaid"
    datetime_str=y['date']/1000
    notedate= datetime.datetime.fromtimestamp(datetime_str).strftime('%Y-%m-%d') 
    item_array=[]
    for item in y['lineItems']:
        obj={}
        obj={
                "sku": item['proInventory']['inventoryCode'],
                "name": item['proInventory']['name'],
                "units": item['quantity'],
                "selling_price":item['unitPrice']
            }
        item_array.append(obj)

    json_item={
            "order_id": y['number'],
            "order_date": notedate,
            "channel_id": channelid,
            "pickup_customer_name": y['billAddress']['name'],
            # "pickup_last_name": "",
            # "company_name":"",
            "pickup_address": y['billAddress']['address1'],
            # "pickup_address_2": "",
            "pickup_city": y['billAddress']['city'],
            "pickup_state": y['billAddress']['state'],
            "pickup_country": y['billAddress']['country'],
            "pickup_pincode":y['billAddress']['zip'],
            # "pickup_email": y['contact']['email'],
            "pickup_phone":y['billAddress']['mobile'],
            # "pickup_isd_code": "",
            "shipping_customer_name": cname,
            # "shipping_last_name": "",
            "shipping_address": y['branch']['branchAddress']['address1'],
            # "shipping_address_2": "",
            "shipping_city": y['branch']['branchAddress']['city'],
            "shipping_country":y['branch']['branchAddress']['country'],
            "shipping_pincode":y['branch']['branchAddress']['zip'],
            "shipping_state": y['branch']['branchAddress']['state'],
            "shipping_email":cemail,
            # "shipping_isd_code": "",
            "shipping_phone":cphone,
            "order_items": item_array,
            "payment_method": "Prepaid",
            "sub_total":y['totalTaxableAmount'],
            "length":length,
            "breadth":breadth,
            "height":height,
            "weight":weight
            # "request_pickup":""
    }
    print("kalsh in function -------------------------------")
    r2 = requests.post(url2, json=json_item,headers=headers)
    res = r2.json()
    return res


#API for validation data in credit note for AWB Generation 
@api_view(['GET', 'POST','DELETE'])
def validatecredit(request, **kwargs):
    if request.method == "GET":
        try:
            data=validate_credit_data.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("validatecredit get request in except")


    if request.method == "POST":
        try:
            # print(request.data)
            for x in request.data:
                item_array=[]
                print("this is data------------------",x)
                if "lineItems" in x['json']:
                    for item in x['json']['lineItems']:
                        obj={}
                        obj={
                                "sku": item['proInventory']['inventoryCode'] or "null",
                                "name": item['proInventory']['name'] or "null",
                                "units": item['quantity'] or "null",
                                "selling_price":item['unitPrice'] or "null"
                            }
                        item_array.append(obj)
                
                if x['dimension_status'] == "Custom":
                    vpaymentMethod=0
                    vlength = x['length']
                    vbreadth = x['breadth']
                    vheight = x['height']
                    vweight =  x['weight']
                    vmode = x['mode']
                else:
                    vpaymentMethod = x['json']['shipmentDetail']['shipPaymentType']
                    vlength = x['json']['shipmentDetail']['shipLength']
                    vbreadth = x['json']['shipmentDetail']['shipBreadth']
                    vheight = x['json']['shipmentDetail']['shipHeight']
                    vweight = x['json']['shipmentDetail']['shipWeight']
                    vmode = x['json']['shipmentDetail']['shipSurface']

                obj={
                        "order_id": x['CreditnoteNo'] or "null",
                        "order_date":x['Creditnotedate'] or "null",
                        "channel_id": x['channelid'] or "null",
                        "pickup_customer_name": x['json']['billAddress']['name'] or "null",
                        # "pickup_last_name": "",
                        # "company_name":"",
                        "pickup_address": x['json']['billAddress']['address1'] or "null",
                        # "pickup_address_2": "",
                        "pickup_city": x['json']['billAddress']['city'] or "null",
                        "pickup_state": x['json']['billAddress']['state'] or "null",
                        "pickup_country": x['json']['billAddress']['country'] or "null",
                        "pickup_pincode":x['json']['billAddress']['zip'] or "null",
                        # "pickup_email": y['contact']['email'],
                        "pickup_phone":x['json']['billAddress']['mobile'] or "null",
                        # "pickup_isd_code": "",
                        "shipping_customer_name": x['cname'] or "null",
                        # "shipping_last_name": "",
                        "shipping_address": x['json']['branch']['branchAddress']['address1'] or "null",
                        # "shipping_address_2": "",
                        "shipping_city": x['json']['branch']['branchAddress']['city'] or "null",
                        "shipping_country":x['json']['branch']['branchAddress']['country'] or "null",
                        "shipping_pincode":x['json']['branch']['branchAddress']['zip'] or "null",
                        "shipping_state": x['json']['branch']['branchAddress']['state'] or "null",
                        "shipping_email": x['cemail'] or "null",
                        # "shipping_isd_code": "", 
                        "shipping_phone":x['cphone'] or "null",
                        "order_items": item_array,
                        "payment_method": vpaymentMethod,
                        "sub_total":x['json']['totalTaxableAmount'] or "null",
                        "length":vlength,
                        "breadth":vbreadth,
                        "height":vheight,
                        "weight":vweight
                        # "request_pickup":""
                }
                Remark=""
                for key in obj.keys():
                    if obj[key] == "null" or obj[key] == []:
                        Remark+=key + ","
                    else:
                        pass
                if Remark == "":
                    CreditnoteNo=x['CreditnoteNo']
                    customername=x['customername']
                    Creditnotedate=x['Creditnotedate']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    jsonn=x['json']
                    mode=vmode
                    message="Data Validated Successfully"
                    a=validate_credit_data(CreditnoteNo=CreditnoteNo,customername=customername,Creditnotedate=Creditnotedate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,json=jsonn,mode=mode,Remark=message,companyid=compid)
                    a.save(using="shiprocket")
                else:
                    CreditnoteNo=x['CreditnoteNo']
                    customername=x['customername']
                    Creditnotedate=x['Creditnotedate']
                    frompincode=x['frompincode']
                    topincode=x['topincode']
                    state=x['state']
                    city=x['city']
                    shippingaddress=x['shippingaddress']
                    jsonn=x['json']
                    mode=vmode
                    message=Remark + "have null value So please fill their values"
                    a=validate_credit_data(CreditnoteNo=CreditnoteNo,customername=customername,Creditnotedate=Creditnotedate,frompincode=frompincode,topincode=topincode,state=state,city=city,shippingaddress=shippingaddress,json=jsonn,mode=mode,Remark=message,companyid=compid)
                    a.save(using="shiprocket")
                b=credit_check_availability.objects.using("shiprocket").filter(CreditnoteNo=x['CreditnoteNo'],companyid=compid)
                b.delete()
            return Response("Data Validation Successful")
        except Exception as e:
            print("\n this is error---------------",e)
            return Response("Data Validation failed")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=validate_credit_data.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Credit Note Delete Successfully")
        except:
            return Response("Credit Note Delete Failed")


# API for getting popup data
@api_view(['POST'])
def get_popup_check_data(request, **kwargs):
    if request.method == "POST":
        try:
            id=request.data['id']
            print(id)
            data=popup_check_data.objects.using("shiprocket").filter(statusid=id).values()
            print("kalash")
            return Response(data)

        except:
            return Response("No popup data!!!!!!!")

# API for getting popup data
@api_view(['POST'])
def get_popup_credit_data(request, **kwargs):
    if request.method == "POST":
        try:
            id=request.data['id']
            print(id)
            data=credit_popup_check_data.objects.using("shiprocket").filter(statusid=id).values()
            print("kalash")
            return Response(data)

        except:
            return Response("No Data Found")

# update shipment in HB Accounting after availability check 
@api_view(['GET', 'POST'])
def updateshipment(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("updateshipment get request in try")

        except:
            return HttpResponse("updateshipment get request in except")


    if request.method == "POST":
        try:
            # Accountinglogin()
            if request.data != []:
                postarray=[]
                for x in request.data:
                    shipno=x['shipmentno']
                    if x['availability'] == "NO":
                        avail=False
                        agent=""
                        agentcode=""
                    else:
                        avail=True
                        agent=x['courier_agent']
                        code=agent.split('-')
                        agentcode=code[0]
                    if x['weight'] == None:
                        weight=""
                    else:
                        weight=x['weight']
                    if x['length'] == None:
                        length=""
                    else:
                        length=x['length']
                    if x['breadth'] == None:
                        breadth=""
                    else:
                        breadth=x['breadth']
                    if x['height'] == None:
                        height=""
                    else:
                        height=x['height']
                    obj={}
                    obj={
                            "number": shipno,
                            "date": x['orderdate'],
                            "courierPartnerName": agent,
                            "courierPartnerCode": agentcode,
                            "weight":weight ,
                            "length": length,
                            "breadth": breadth,
                            "height": height,
                            "surface": x['mode'],
                            "pinCodeAvailability": avail      
                        }
                    postarray.append(obj)
                url = acc_update_url

                payload ={
                    "invoiceDataList": [],
                    "shipmentDataList": postarray
                }

                headers = {
                        "x-auth-token": valuetoken,
                        "x-preserveKey":  preserve,
                        "x-company":  compid,
                        "Content-Type": "application/json"
                }
                print("update payload --->",payload)
                response = requests.put( url, headers=headers, json=payload)
                res=response.json()
                print(res)
                if res['message'] == "Updated successfully":
                    for x in request.data:
                        shipno=x['shipmentno']
                        a=check_availability_data.objects.using("shiprocket").filter(shipmentno=shipno,companyid=compid)
                        a.delete()
                    return Response("Update shipment successfully")
                else:
                    return Response("Update shipment failed!!!")
            else:
                return Response("Please Select Shipment for Updation")
        except:
            return Response("Update shipment Failed!!!")


# update invoice in HB Accounting after AWB Generation
@api_view(['GET', 'POST'])
def updateinvoice(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("updateinvoice get request in try")

        except:
            return HttpResponse("updateinvoice get request in except")


    if request.method == "POST":
        try:
            # Accountinglogin()
            print(request.data)
            postarr=[]
            if request.data != []:
                for x in request.data:
                    date=x['invoice_data']['Invoicedate']
                    newdate=date.split('-')
                    invoicedate=newdate[2]+"-"+newdate[1]+"-"+newdate[0]
                    if x['invoice_data']['dimension_status'] == "Custom":
                        weight=x['invoice_data']['weight']
                        length=x['invoice_data']['length']
                        breadth=x['invoice_data']['breadth']
                        height=x['invoice_data']['height']
                    else:
                        weight=x['invoice_data']['shipWeight']
                        length=x['invoice_data']['shipLength']
                        breadth=x['invoice_data']['shipBreadth']
                        height=x['invoice_data']['shipHeight']
                    obj={}
                    obj={
                            "number": x['InvoiceNo'],
                            "invoiceDate": invoicedate,
                            "courierPartnerName": x['awb_data']['payload']['courier_name'],
                            "courierPartnerCode": x['awb_data']['payload']['courier_company_id'],
                            "awbNumber": x['awb_data']['payload']['awb_code'],
                            "awbPrintUrl": x['awb_data']['payload']['label_url']+","+x['awb_data']['payload']['manifest_url'],
                            "dispatchStatus": x['status'],
                            "shipWeight": weight,
                            "shipLength": length,
                            "shipBreadth": breadth,
                            "shipHeight": height,
                            "shipSurface": x['invoice_data']['shipSurface'],
                            "pinCodeAvailability":x['invoice_data']['pinCodeAvailability']     
                    }
                    postarr.append(obj)
                print(postarr)
                url = acc_update_url

                payload ={
                    "invoiceDataList": postarr,
                    "shipmentDataList":[]
                }

                headers = {
                        "x-auth-token": valuetoken,
                        "x-preserveKey":  preserve,
                        "x-company":  compid,
                        "Content-Type": "application/json"
                }

                response = requests.put( url, headers=headers, json=payload)
                res=response.json()
                print(res)
                if res['message'] == "Updated successfully":
                    return Response("Update Invoice Successfully")
                else:
                    return Response("Update Invoice Failed!!!")
            else:
                return Response("Please select Invoice for updation")
        except:
            return Response("Update Invoice Failed!!!")


# update invoice in HB Accounting after AWB Generation
@api_view(['GET', 'POST'])
def updatecredit(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("updatecredit get request in try")

        except:
            return HttpResponse("updatecredit get request in except")


    if request.method == "POST":
        try:
            # Accountinglogin()
            print(request.data)
            postarr=[]
            if request.data != []:
                for x in request.data:
                    date=x['credit_data']['Creditnotedate']
                    newdate=date.split('-')
                    invoicedate=newdate[2]+"-"+newdate[1]+"-"+newdate[0]
                    if x['credit_data']['dimension_status'] == "Custom":
                        weight=x['credit_data']['weight']
                        length=x['credit_data']['length']
                        breadth=x['credit_data']['breadth']
                        height=x['credit_data']['height']
                    else:
                        weight=x['credit_data']['json']['shipmentDetail']['shipWeight']
                        length=x['credit_data']['json']['shipmentDetail']['shipLength']
                        breadth=x['credit_data']['json']['shipmentDetail']['shipBreadth']
                        height=x['credit_data']['json']['shipmentDetail']['shipHeight']
                    obj={}
                    obj={
                            "number": x['CreditnoteNo'],
                            "invoiceDate": invoicedate,
                            "courierPartnerName": x['awb_data']['payload']['courier_name'],
                            "courierPartnerCode": x['awb_data']['payload']['courier_company_id'],
                            "awbNumber": x['awb_data']['payload']['awb_code'],
                            "awbPrintUrl":"",
                            "dispatchStatus": x['status'],
                            "shipWeight":weight,
                            "shipLength": length,
                            "shipBreadth":breadth,
                            "shipHeight": height,
                            "shipSurface": x['credit_data']['json']['shipmentDetail']['shipSurface'],
                            "pinCodeAvailability":x['credit_data']['json']['shipmentDetail']['pinCodeAvailability']     
                    }
                    postarr.append(obj)
                print(postarr)
                url = acc_update_url

                payload ={
                    "creditNoteDataList": postarr,
                    "shipmentDataList":[]
                }

                headers = {
                        "x-auth-token": valuetoken,
                        "x-preserveKey":  preserve,
                        "x-company":  compid,
                        "Content-Type": "application/json"
                }

                response = requests.put( url, headers=headers, json=payload)
                res=response.json()
                print(res)
                if res['message'] == "Updated successfully":
                    for b in request.data:
                        CreditnoteNo=b['CreditnoteNo']
                        a=credit_awb.objects.using("shiprocket").filter(CreditnoteNo=CreditnoteNo,companyid=compid)
                        a.delete()
                    return Response("Update Creditnote Successfully")
                else:
                    return Response("Update Creditnote Failed!!!")
            else:
                return Response("Please select Creditnote for updation")
        except:
            return Response("Update Creditnote Failed!!!")


# Get Dispatch Status of invoice API
@api_view(['GET', 'POST','DELETE'])
def dispatch_status_inv(request, **kwargs):
    if request.method == "GET":
        try:
            data=invoice_awb_failed.objects.using("shiprocket").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("Data Not Found!!!")


    if request.method == "POST":
        try:
            # Accountinglogin()
            # print(request.data)
            if request.data != []:
                for x in request.data:
                    awbno=x['awb_data']['payload']['awb_code']
                    url1="https://apiv2.shiprocket.in/v1/external/auth/login"
                    headers={
                        "Content-Type":"application/json"
                    }
                    add_item={
                        "email":x['invoice_data']['email'],
                        "password": x['invoice_data']['password']
                        # "email": request.data['email'],
                        # "password": request.data['password']
                    }
                    r1 = requests.post(url1, json=add_item)
                    res = r1.json()
                    shiptoken=r1.json()['token']
                    print("klash is her------------------------")
                    url2="https://apiv2.shiprocket.in/v1/external/courier/track/awbs"
                    headers={
                                    "Content-Type": "application/json",
                                    "Authorization": "Bearer" + shiptoken
                                }
                    payload={ 
                        "awbs": [awbno]
                        }
                    response = requests.post( url2, headers=headers, json=payload)
                    res=response.json()
                    print(res)
                    dispatch_data=res[awbno]['tracking_data']
                    if len(dispatch_data) > 2:
                        status=res[awbno]['tracking_data']['shipment_track'][0]['current_status']
                    else:
                        status=res[awbno]['tracking_data']['error']
                    a=invoice_awb.objects.using("shiprocket").filter(companyid=compid,awb_data=x['awb_data']).update(dispatch_data=dispatch_data,status=status)
                return Response("Check Dispatch Status Successfully")
            else:
                return Response("Please select Invoice for checking dispatch status")
        except:
            return Response("Check Dispatch Status Failed!!!")

    if request.method == "DELETE":
        try:
            ids=request.GET.get("id").split(",")
            for id in ids:
                a=invoice_awb_failed.objects.using("shiprocket").filter(id=id)
                a.delete()
            return Response("Invoice Delete Successfully")
        except:
            return Response("Invoice Delete Failed")



