from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework import status
import requests
import json
import datetime
from datetime import datetime, timedelta
from .models import hotellogixlogin,depositrecord,paymentrecord,invoicerecord,commrecord,invoicerecordfailed,depositfailedrecord,paymentfailedrecord,commfailedrecord
from . import Accounting
from django.db.models import Q

# ////////************function for Accounting log in ****************/////////////////////////////////////////////

#All New urls for sandbox and local use 
branch="https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url="https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url="https://booksapi.hostbooks.in/hostbook/api/master/add"
hotelogix_url="https://hotelogix.net/"

# all urls for live server
# branch="https://in2accounts.hostbooks.com/api/master/list"
# acc_txn_url="https://in2accounts.hostbooks.com/api/transaction/add"
# acc_mas_url="https://in2accounts.hostbooks.com/api/master/add"
# hotelogix_url="https://www.staygrid.com/"

# /////////////////////////*************Accounting login function ends *****************************///////////////////////////////

def update_inv_status(inv_code,paycodes,hotelid,token,inv_status):
    print(inv_code)
    print(hotelid)
    print(token)
    print(inv_status)
    print(paycodes)
    if paycodes != []:
        for pay_code in paycodes:
            url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/hotel"
            headers={
                        "RQ-HOTELID":hotelid,
                        "RQ-AUTH-TOKEN":token
                    }
            payload={
                    "Invoices": {
                        # "INV-3910466": "SUCCESS",
                        # "INV-3910354": "FAILED"
                        inv_code:inv_status
                    },
                    "Payments":{
                        pay_code:inv_status
                    } 
            }
            r=requests.post(url, headers=headers , json=payload)
            res=r.json()
            print(res)
    else:
        url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/hotel"
        headers={
                    "RQ-HOTELID":hotelid,
                    "RQ-AUTH-TOKEN":token
                }
        payload={
                "Invoices": {
                    # "INV-3910466": "SUCCESS",
                    # "INV-3910354": "FAILED"
                    inv_code:inv_status
                },
                "Payments":{} 
        }
        r=requests.post(url, headers=headers , json=payload)
        res=r.json()
        print(res)
    print("update invoice status json response")

def update_dep_status(dep_code,hotelid,token):
    print(dep_code)
    print(hotelid)
    print(token)
    url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/dep"
    headers={
                "RQ-HOTELID":hotelid,
                "RQ-AUTH-TOKEN":token
            }
    payload={
            "Invoices": {
                dep_code:"SUCCESS"
            },
            "Payments": {}
    }
    r=requests.post(url, headers=headers , json=payload)
    res=r.json()
    print(res)
    print("update invoice status json response")

def update_pay_status(pay_code,hotelid,token):
    print(pay_code)
    print(hotelid)
    print(token)
    url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/payments"
    headers={
                "RQ-HOTELID":hotelid,
                "RQ-AUTH-TOKEN":token
            }
    payload={
            "Invoices": {},
            "Payments": {
                pay_code:"SUCCESS"
            }
    }
    r=requests.post(url, headers=headers , json=payload)
    res=r.json()
    print(res)
    print("update invoice status json response")

def update_comm_status(inv_code,hotelid,token):
    print(inv_code)
    print(hotelid)
    print(token)
    url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/comm"
    headers={
                "RQ-HOTELID":hotelid,
                "RQ-AUTH-TOKEN":token
            }
    payload={
            "Invoices": {
                inv_code:"SUCCESS"
            },
            "Payments": {}
    }
    r=requests.post(url, headers=headers , json=payload)
    res=r.json()
    print(res)
    print("update invoice status json response")

# ////////////////////////////////hotellogix login starts /////////////////////////////////////////////////////////////////////////

@api_view(['GET', 'POST','PUT'])
def hotelogixlogin(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            data=hotellogixlogin.objects.using("hotel").filter(companyid=compid).values()
            return Response(data)

        except:
            return Response("hotellogix login get request in except")


    if request.method == "POST":
        try:
            print(request.data)
            user=request.data['user']
            password=request.data['password']
            hotelid=request.data['hotelid']
            branch=request.data['branch']
            category=request.data['category']
            # transaction1=request.data['transaction1']
            # addnote1=request.data['addnote1']
            gstin=request.data['gstin']
            state=request.data['state']
            saveas=request.data['saveas']
            city=request.data['city']
            zip=request.data['zip']
            address1=request.data['address1']
            ledger_settings=request.data['ledger_settings']
            # startdate=request.data['startdate']
            compid=request.data['compid']
            contactcode=request.data['contactcode']
            contactname=request.data['contactname']
            walk_contactcode=request.data['walk_contactcode']
            walk_contactname=request.data['walk_contactname']

            a=hotellogixlogin(user=user,password=password,hotelid=hotelid,branch=branch,category=category,gstin=gstin,state=state,saveas=saveas,city=city,zip=zip,address1=address1,companyid=compid,ledger_settings=ledger_settings,contact_code=contactcode,contact_name=contactname,walk_contact_code=walk_contactcode,walk_contact_name=walk_contactname)
            a.save(using="hotel")
            return Response("LOGIN SUCCESSFULLY")

        except:
            return Response("UNAUTHORIZED ACCESS")

    if request.method == "PUT":
        try:
            print(request.data)
            id=request.data['id']
            user=request.data['user']
            password=request.data['password']
            hotelid=request.data['hotelid']
            branch=request.data['branch']
            category=request.data['category']
            gstin=request.data['gstin']
            state=request.data['state']
            saveas=request.data['saveas']
            city=request.data['city']
            zip=request.data['zip']
            address1=request.data['address1']
            ledger_settings=request.data['ledger_settings']
            # startdate=request.data['startdate']
            compid=request.data['compid']
            contactcode=request.data['contactcode']
            contactname=request.data['contactname']
            walk_contactcode=request.data['walk_contactcode']
            walk_contactname=request.data['walk_contactname']

            a=hotellogixlogin.objects.using("hotel").filter(id=id).update(user=user,password=password,hotelid=hotelid,branch=branch,category=category,gstin=gstin,state=state,saveas=saveas,city=city,zip=zip,address1=address1,companyid=compid,ledger_settings=ledger_settings,contact_code=contactcode,contact_name=contactname,walk_contact_code=walk_contactcode,walk_contact_name=walk_contactname)

            return Response("Data update successfully")
        except:
            return Response("data update failed please fill data carefully")
        

# branch api starts
@api_view(['GET', 'POST'])
def branchlist(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("branchapi get request in try")

        except:
            return HttpResponse("branchapi get request in except")


    if request.method == "POST":
        try:
            # Accounting login starts
            global compid,preserve,valuetoken
            compid, preserve = request.data['compid'], request.data['preservekey']
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']

            # Accounting Login ends
            url = branch
            payload = json.dumps({
                "page": 1,
                "limit": 500,
                "entityType": "BRANCH"
            })
            headers = {
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid,
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, data=payload)
            res_branch = response.json()
            print("Branches---->", res_branch)


            payload = json.dumps({
                "page": 1,
                "limit": 500,
                "entityType": "CATEGORY"
            })
            headers = {
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid,
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, data=payload)
            res_cat = response.json()


            data_branch = []
            for x in res_branch['data']['master']['list']:
                obj = {}
                obj['branch'] = x['name']
                obj['gstin'] = x['gstin']
                obj['state'] = x['branchAddress']['state']
                obj['city'] = x['branchAddress']['city']
                obj['zip'] = x['branchAddress']['zip']
                obj['address1'] = x['branchAddress']['address1']
                data_branch.append(obj)

            data_cat = []
            for y in res_cat['data']['master']['list']:
                obj = {}
                obj['category'] = y['options']
                data_cat.append(obj)

            costcodeurl = branch
            header2 = {
                "x-auth-token": valuetoken,
                "x-preserveKey":  preserve,
                "x-company":  compid,
                "Content-Type": "application/json"
            }
            body2 = {
                "entityType": "COST_CENTER",
                "allTxnFlag": 1,
                "webhook": 1,
                "page": 1,
                "limit": 500
            }
            acresponse = requests.post(costcodeurl, headers=header2, json=body2)
            costcode = acresponse.json()
            return Response({"Branch": data_branch, "Category": data_cat,"costCenter": costcode['data']['master']['list']})
        
        except:
            return Response("Please fill all the required fields in your Branches and Categories")

         
# sync deposit API starts
@api_view(['GET', 'POST','DELETE'])
def SyncDeposit(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=depositrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Narration","Credit_Amount","Debit_Amount","Remark","Status","companyid","branchid","depcode").order_by('-id')
            return Response(data)
        except:
            return Response("sync deposit get request in except")


    if request.method == "POST":
        try:
            # Accounting login starts 
            compid,preserve=request.data['compid'],request.data['preservekey']
            login=Accounting.Accounting_login(preserve,compid)
            compid,preserve,valuetoken=login['compid'],login['preservekey'],login['token']
            # Accounting Login ends
            hotelid=request.data['hotelid']
            token=request.data['token']
            branch=request.data['branch']
            gstin=request.data['gstin']
            ledger_settings=request.data['ledger_settings']
            fromdate=request.data['fromdate']
            todate=request.data['todate']
            branchid=request.data['branch_id']
            print("Start Date ----->",fromdate)
            print("End Date ----->",todate)
            for page in range(1,1000):
                hlurl=hotelogix_url+"v/accountingledger/ledgers/actype/tpa/dtype/dep"
                headers={
                    "RQ-HOTELID":hotelid,
                    "RQ-AUTH-TOKEN":token,
                    "RQ-PAGE":"1"
                }
                payload={
                    "fromDate": fromdate,
                    "toDate": todate
                }
                r=requests.post(hlurl, headers=headers ,json=payload)
                res=r.json()
                print(res)
                print(page)
                print("json response")
                if "Invoices" not in res:
                    print("data over")
                    if page > 1:
                        return Response("SYNC DEPOSIT  SUCCESSFULLY")
                    else:
                        return Response("No Records Found !!!")
                else:
                    for x in res['Invoices']:
                        try:
                            invoiceno=hotelid+"-"+x['InvoiceNumber']
                            invoicecode=x['InvoiceCode']
                            invoice_date=x['Date']
                            print("before updatation")
                            update_dep_status(invoicecode,hotelid,token)
                            print("after updatation")
                            print("Invoice Date ------>",invoice_date)
                            jarray=[]
                            for y in x['Payments']:
                                if y['description'] != None:
                                    desc=y['description']
                                else:
                                    desc="Booking Advance"
                                code=y['Account']['Code']
                                for row in ledger_settings:
                                    code=y['Account']['Code'].lower()
                                    acc_code=row['ledgerCode'].lower()
                                    if acc_code == code:
                                        code=row['Acc_Code']
                                        break
                                    else:
                                        code="Not Found"
                                # if code == y['Account']['Code']:
                                #     code="Not Found"
                                amount=y['Amount']
                                obj={}
                                if float(amount) < 0:
                                    # print(abs(amount))
                                    obj={
                                            "description": desc,
                                            "accountCode": code,
                                            # "taxRateName": "Tax Exempt (0%)", // Not required
                                            # "costCenter": null, // Not required
                                            "creditAmount": -(float(amount)),
                                            "debitAmount":None
                                        }
                                    jarray.append(obj)
                                elif float(amount) == 0:
                                    print("elif condi in deposit")
                                else:
                                    obj={
                                            "description": desc,
                                            "accountCode": code,
                                            # "taxRateName": "Tax Exempt (0%)", // Not required
                                            # "costCenter": null, // Not required
                                            "creditAmount": None,
                                            "debitAmount":amount,
                                        }
                                    jarray.append(obj)

                            for z in x['LineItems']:
                                if z['Description'] != None:
                                    linedesc=z['Description']
                                else:
                                    linedesc="Booking Advance"
                                lineamcode=z['AccountCode']
                                for row in ledger_settings:
                                    lineamcode=z['AccountCode']
                                    acc_code=row['ledgerCode']
                                    if acc_code == lineamcode:
                                        lineamcode=row['Acc_Code']
                                        break
                                    else:
                                        lineamcode="Not Found"
                                # if lineamcode == z['AccountCode']:
                                #     lineamcode="Not Found"
                                lineunitamount=z['UnitAmount']
                                obj={}
                                if float(lineunitamount) < 0:
                                    obj={
                                            "description": linedesc,
                                            "accountCode": lineamcode,
                                            # "taxRateName": "Tax Exempt (0%)", // Not required
                                            # "costCenter": null, // Not required
                                            "creditAmount": None,
                                            "debitAmount":-(float(lineunitamount))
                                        }
                                    jarray.append(obj)
                                elif float(lineunitamount) == 0:
                                    print("elif condi in deposit")
                                else:
                                    obj={
                                            "description": linedesc,
                                            "accountCode": lineamcode,
                                            # "taxRateName": "Tax Exempt (0%)", // Not required
                                            # "costCenter": null, // Not required
                                            "creditAmount": lineunitamount,
                                            "debitAmount":None
                                        }
                                    jarray.append(obj)
                            restype=x['Type']
                            resdate=x['Date']
                            dataarr=resdate.split("-")
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            print("kalash is here")
                            print(jarray)
                            debit=0
                            credit=0
                            noMatchCode=0
                            for j in jarray:
                                print("kalash in loop")
                                if j['debitAmount'] != None:
                                    debit+=float(j['debitAmount'])
                                if j['creditAmount'] != None:
                                    credit+=float(j['creditAmount'])
                                if j['accountCode'] == "Not Found":
                                    noMatchCode+=1
                            if noMatchCode == 0:
                                accountingurl=acc_txn_url
                                headers={
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }
                                add_item={
                                    "journalList": [
                                        {
                                            "taxRateFlag": "false",
                                            "branch": branch,
                                            "category": "Service",
                                            "number": invoiceno,
                                            "debitAmount": debit,
                                            "creditAmount": credit,
                                            "companyGstin": gstin,
                                            "manualJournalDetail": jarray,
                                            "narration":restype,
                                            "reportflag": 1,
                                            "autoReversingDate": None,
                                            "date":newdate,
                                            "amount": 0,
                                            "taxType": "NTAX",
                                            "status": "MJPT",
                                            "txnStatus": "TRPN",
                                        "typeCode":"JMJ",
                                        }
                                    ]
                                }
                                r=requests.post(accountingurl,json=add_item, headers=headers)
                                res=r.json()
                                print(res)
                                print("accounting response")
                                print(add_item)
                                # currenttime=datetime.now().strftime('%H:%M:%S')
                                # print(currenttime)
                                if res['message'] == "Batch Data Added successfully":
                                    a=depositrecord(Number=invoiceno,Date=newdate,Narration=restype,Credit_Amount=round(credit,2),Debit_Amount=round(debit,2),Remark=res['message'],Status="SUCCESS",companyid=compid,Response_json=x,Requested_json=add_item,branchid=branchid,depcode=invoicecode)
                                    a.save()
                                elif res['message'] == "Some Data is not valid and other batch data added successfully":
                                    if "fieldErrors" in res:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
                                    else:
                                        message=res['errorList'].values()
                                    a=depositfailedrecord(Number=invoiceno,Date=newdate,Narration=restype,Credit_Amount=round(credit,2),Debit_Amount=round(debit,2),depcode=invoicecode,Remark=message,Status="FAILED",companyid=compid,Response_json=x,Requested_json=add_item,branchid=branchid)
                                    a.save(using="hotel")
                                else:
                                    a=depositfailedrecord(Number=invoiceno,Date=newdate,Narration=restype,Credit_Amount=round(credit,2),Debit_Amount=round(debit,2),depcode=invoicecode,Remark=res['message'],Status="FAILED",companyid=compid,Response_json=x,Requested_json=add_item,branchid=branchid)
                                    a.save(using="hotel")
                            else:
                                add_item={
                                    "journalList": [
                                        {
                                            "taxRateFlag": "false",
                                            "branch": branch,
                                            "category": "Service",
                                            "number": invoiceno,
                                            "debitAmount": debit,
                                            "creditAmount": credit,
                                            "companyGstin": gstin,
                                            "manualJournalDetail": jarray,
                                            "narration":restype,
                                            "reportflag": 1,
                                            "autoReversingDate": None,
                                            "date":newdate,
                                            "amount": 0,
                                            "taxType": "NTAX",
                                            "status": "MJPT",
                                            "txnStatus": "TRPN",
                                        "typeCode":"JMJ",
                                        }
                                    ]
                                }
                                message="Account code did not match please add in your Ledger setting"
                                a=depositfailedrecord(Number=invoiceno,Date=newdate,Narration=restype,Credit_Amount=round(credit,2),Debit_Amount=round(debit,2),depcode=invoicecode,Remark=message,Status="FAILED",companyid=compid,Response_json=x,Requested_json=add_item,branchid=branchid)
                                a.save(using="hotel")
                        except Exception as e:
                            print("error is -----",e)
                            message=f"{e} is missing in Hotelogix JSON"
                            restype=x['Type']
                            resdate=x['Date']
                            dataarr=resdate.split("-")
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            invoiceno=x['InvoiceNumber']
                            invoicecode=x['InvoiceCode']
                            debit=0
                            credit=0
                            if len(jarray) != 0:
                                for j in jarray:
                                    print("kalash in loop")
                                    if j['debitAmount'] != None:
                                        debit+=float(j['debitAmount'])
                                    if j['creditAmount'] != None:
                                        credit+=float(j['creditAmount'])
                            else:
                                debit=float(0)
                                credit=float(0)
                            add_item={
                                        "journalList": [
                                            {
                                                "taxRateFlag": "false",
                                                "branch": branch,
                                                "category": "Service",
                                                "number": invoiceno,
                                                "debitAmount": debit,
                                                "creditAmount": credit,
                                                "companyGstin": gstin,
                                                "manualJournalDetail": jarray,
                                                "narration":restype,
                                                "reportflag": 1,
                                                "autoReversingDate": None,
                                                "date":newdate,
                                                "amount": 0,
                                                "taxType": "NTAX",
                                                "status": "MJPT",
                                                "txnStatus": "TRPN",
                                            "typeCode":"JMJ",
                                            }
                                        ]
                                    }
                            a=depositfailedrecord(Number=invoiceno,Date=newdate,Narration=restype,Credit_Amount=round(credit,2),Debit_Amount=round(debit,2),depcode=invoicecode,Remark=message,Status="FAILED",companyid=compid,Response_json=x,Requested_json=add_item,branchid=branchid)
                            a.save(using="hotel")


            return Response("SYNC DEPOSIT  SUCCESSFULLY")

        except:
            return Response("SYNC DEPOSIT FAILED!!!!!")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=depositrecord.objects.using("hotel").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed !!!")


# sync Customers & Invoices API starts
@api_view(['GET', 'POST','DELETE'])
def SyncInvoice(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=invoicerecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Customer_Name","Date","Invoice_Amount","Due_Amount","Received_Amount","Remark","Status","companyid","branchid","invoicecode").order_by('-id')
            return Response(data)

        except:
            return Response("Customers & Invoices get request in except")


    if request.method == "POST":
        try:
            # Accounting login starts 
            compid,preserve=request.data['compid'],request.data['preservekey']
            login=Accounting.Accounting_login(preserve,compid)
            compid,preserve,valuetoken=login['compid'],login['preservekey'],login['token']
            # Accounting Login ends
            hotelid=request.data['hotelid']
            token=request.data['token']
            gstin=request.data['gstin']
            branch=request.data['branch']
            state=request.data['state']
            saveas=request.data['saveas']
            city=request.data['city']
            zip=request.data['zip']
            address1=request.data['address1']
            # add variables for contact code and name by kalash 
            contact_code=request.data['contact_code']
            contact_name=request.data['contact_name']
            walk_contact_code=request.data['walk_contact_code']
            walk_contact_name=request.data['walk_contact_name']
            # ends
            ledger_settings=request.data['ledger_settings']
            fromdate=request.data['fromdate']
            todate=request.data['todate']
            branchid=request.data['branch_id']
            print("Start Date ----->",fromdate)
            print("End Date ----->",todate)
            total_invs=0
            success_invs=0
            failed_invs=0
            for page in range(1,1000):
                print("in loop")
                hlurl=hotelogix_url+"v/accountingledger/ledgers/actype/tpa/dtype/hotel"
                headers={
                    "RQ-HOTELID":hotelid,
                    "RQ-AUTH-TOKEN":token,
                    "RQ-PAGE":"1"
                }
                payload={
                    "fromDate": fromdate,
                    "toDate": todate
                }
                r=requests.post(hlurl, headers=headers ,json=payload)
                res=r.json()
                print(res)
                print(page)
                print("json response")
                if "Invoices" not in res:
                    print("data over")
                    if page > 1:
                        return Response({
                            "message":"SYNC CUSTOMERS & INVOICES SUCCESSFULLY",
                            "Total_Invoices":total_invs,
                            "Success_Invoices":success_invs,
                            "Failed_Invoices":failed_invs
                        })
                    else:
                        return Response({
                            "message":"No Records Found !!!",
                            "Total_Invoices":total_invs,
                            "Success_Invoices":success_invs,
                            "Failed_Invoices":failed_invs
                        })
                        # return Response("No Records Found !!!")
                else:
                    total_invs+=len(res['Invoices'])
                    for x in res['Invoices']:
                        ErrorFileJson={}
                        try:
                            inv_status="SUCCESS"
                            invoice_code=x['InvoiceCode']
                            paycode_array=[]
                            if "Payments" in x:
                                for pay in x['Payments']:
                                    print("kalash in payment")
                                    code=pay['PaymentCode']
                                    paycode_array.append(code)
                            update_inv_status(invoice_code,paycode_array,hotelid,token,inv_status)
                            inputdate=x['Date']
                            
                            if "CompanyName" not in x:
                                print("Main If part-------------")
                                if "CompanyName" in x['Contact']:
                                    con_name=x['Contact']['CompanyName']
                                    if len(x['Contact']['CompanyName']) == 0:
                                        final_con_name=walk_contact_name
                                        final_con_code=walk_contact_code
                                    else:
                                        pass
                                    print("Main IF x['Contact']['CompanyName'] -----------------",con_name)
                                else:
                                    con_name=x['Contact']['Name']
                                    final_con_name=walk_contact_name
                                    final_con_code=walk_contact_code
                                    print("Main else x['Contact']['Name']-----------------",con_name)
                            else:
                                print("Main Else part----------")
                                if "CompanyName" in x:
                                    con_name=x['CompanyName']
                                    if len(x['CompanyName']) == 0:
                                        final_con_name=walk_contact_name
                                        final_con_code=walk_contact_code
                                    else:
                                        pass
                                    print("If x['CompanyName']---------------",con_name)
                                else:
                                    con_name=x['Contact']['Name']
                                    final_con_name=walk_contact_name
                                    final_con_code=walk_contact_code
                                    print("Else ---------------",con_name)
                            print("Company ------Finally-------",con_name)
                            # Add new condition for contact code and name by kalash
                            if len(con_name) == 0:
                                bill_ship_name=con_name
                                final_con_name=contact_name
                                final_con_code=contact_code
                                if "FirstName" in x['Contact']:
                                    final_first_name=x['Contact']['FirstName']
                                else:
                                    final_first_name=""
                            else:
                                bill_ship_name=con_name
                                final_con_name=con_name
                                final_con_code=x['Contact']['ContactNumber']
                                if "FirstName" in x['Contact']:
                                    final_first_name=x['Contact']['FirstName']
                                else:
                                    final_first_name=""
                                if "CompanyName" in x['Contact']:
                                    if len(x['Contact']['CompanyName']) == 0:
                                        final_con_name=walk_contact_name
                                        final_con_code=walk_contact_code
                                    else:
                                        pass
                                else:
                                    final_con_name=walk_contact_name
                                    final_con_code=walk_contact_code
                            # ends
                            if x['IsRefunded'] == True:
                                print("if cond con name ---->",con_name)
                                print("i am in if cond......")
                                txntype="SCN"
                                # inv_status="SUCCESS"
                                # invoice_code=x['InvoiceCode']
                                # paycode_array=[]
                                # if "Payments" in x:
                                #     for pay in x['Payments']:
                                #         print("kalash in payment")
                                #         code=pay['PaymentCode']
                                #         paycode_array.append(code)
                                # update_inv_status(invoice_code,paycode_array,hotelid,token,inv_status)
                                # inputdate=x['Date']
                                dataarr=inputdate.split("-")
                                newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                print(newdate)
                                inputduedate=x['DueDate']
                                dataarr=inputduedate.split("-")
                                newduedate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                print(newduedate)
                                cus_add_item={}
                                inv_add_item={}
                                linearray=[]
                                transcode_arr=[]
                                for y in x['LineItems']:
                                    accode=y['AccountCode']
                                    for row in ledger_settings:
                                        accode=y['AccountCode']
                                        acc_code=row['ledgerCode']
                                        if acc_code == accode:
                                            accode=row['Acc_Code']
                                            break
                                        else:
                                            accode="Not Found"
                                    if accode == "Not Found":
                                        return Response (f"{y['AccountCode']} is missing in ledger settings")
                                    else:
                                        pass
                                    # if accode == y['AccountCode']:
                                    #     accode="Not Found"
                                    if y['ParentTransCode'] == "" or y['ParentTransCode'] == None:
                                        if y['TransCode'] not in transcode_arr:
                                            obj={}
                                            if "Taxes" in y:
                                                for m in y['Taxes']:
                                                    # if m['TaxCode'] != "SERVICECHARGE" or m['TaxCode'] != "SERVICECHARGER" or m['TaxCode'] != "SGST1" or m['TaxCode'] != "CGSTP":
                                                    print(m['TaxCode'].lower())
                                                    if "vat" in ((m['TaxCode']).lower()):
                                                        # # code for discount making
                                                        # vat_dis=0
                                                        # for line in x['LineItems']:
                                                        #     if float(line['UnitAmount']) < 0:
                                                        #         if "Taxes" in line:
                                                        #             for tax in line['Taxes']:
                                                        #                 if (float(tax['UnitAmount']) < 0) and ("vat" in ((tax['TaxCode']).lower())):
                                                        #                     vat_dis+=-(float(line['UnitAmount']))
                                                        # # code for discount making ends
                                                        obj={
                                                            "saleType": "Normal",
                                                            "quantity": y['Quantity'],
                                                            "unitPrice": abs(float(y['UnitAmount'])),
                                                            "amount": 0,
                                                            "description": y['Description'],
                                                            "taxRateName": m['TaxRate'],
                                                            "gstRate":None,
                                                            "billOfSupplyGst":"Non-GST",
                                                            "hsnSac": y['hsncode'],
                                                            "type": "Goods",
                                                            "unitName": "Units",
                                                            "accountCode": accode,
                                                            "Transcode":y['TransCode']
                                                        }
                                                        linearray.append(obj)
                                                    
                                                    if "service" in ((m['TaxCode']).lower()):
                                                        # code for discount making
                                                        # serv_dis=0
                                                        # for line in x['LineItems']:
                                                        #     if float(line['UnitAmount']) < 0:
                                                        #         if "Taxes" in line:
                                                        #             for tax in line['Taxes']:
                                                        #                 if (float(tax['UnitAmount']) < 0) and ("service" in ((tax['TaxCode']).lower())):
                                                        #                     serv_dis+=-(float(tax['UnitAmount']))
                                                        # code for discount making ends
                                                        cess=0
                                                        for t in y['Taxes']:
                                                            if (("cess" in ((t['TaxCode']).lower())) and ((t['ParentTaxCode'] == ((m['TaxCode']).lower())) or (t['ParentTaxCode'] == ((m['TaxCode']).lower())))):
                                                                cess+=float(t['UnitAmount'])
                                                        print("kalash in first cond")
                                                        taxrate=0
                                                        for c in y['Taxes']:
                                                            if ((c['ParentTaxCode'] == ((m['TaxCode']).lower())) or (c['ParentTaxCode'] == ((m['TaxCode']).lower()))):
                                                                taxrate+=float(c['TaxRate'])
                                                        print(taxrate)
                                                        if taxrate == 0 and cess == 0:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": y['Quantity'],
                                                                "unitPrice": abs(float(y['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": m['Description'],
                                                                "taxRateName": m['TaxRate'],
                                                                "gstRate":None,
                                                                "billOfSupplyGst":"Non-GST",
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                            }
                                                        elif taxrate == 0 and cess != 0:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": y['Quantity'],
                                                                "unitPrice": abs(float(y['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": m['Description'],
                                                                "taxRateName": m['TaxRate'],
                                                                "gstRate":None,
                                                                "cess":cess,
                                                                "flatCessFlag":True,
                                                                "billOfSupplyGst":"Non-GST",
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                            }
                                                        elif taxrate != 0 and cess == 0:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": m['Quantity'],
                                                                "unitPrice": abs(float(m['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": m['Description'],
                                                                "taxRateName":"0",
                                                                "gstRate":taxrate,
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                            }
                                                        else:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": m['Quantity'],
                                                                "unitPrice": abs(float(m['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": m['Description'],
                                                                "taxRateName": "0",
                                                                "gstRate":taxrate,
                                                                "cess":cess,
                                                                "flatCessFlag":True,
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                            }
                                                        linearray.append(obj)
                                                    
                                                    if ("sgst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                        print("second cond")
                                                        # code for discount making
                                                        # sgst_dis=0
                                                        # for line in x['LineItems']:
                                                        #     if float(line['UnitAmount']) < 0:
                                                        #         if "Taxes" in line:
                                                        #             for tax in line['Taxes']:
                                                        #                 if ("sgst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                        #                     sgst_dis+=-(float(line['UnitAmount']))
                                                        # code for discount making ends
                                                        taxpercentage =float(m['TaxRate'])*2
                                                        cess=0
                                                        for t in y['Taxes']:
                                                            if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                cess+=float(t['UnitAmount'])
                                                        if cess == 0:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": y['Quantity'],
                                                                "unitPrice": abs(float(y['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": y['Description'],
                                                                "taxRateName": "0",
                                                                "gstRate":taxpercentage,
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                                        }
                                                        else:
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": y['Quantity'],
                                                                "unitPrice": abs(float(y['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": y['Description'],
                                                                "taxRateName": "0",
                                                                "gstRate":taxpercentage,
                                                                "cess":cess,
                                                                "flatCessFlag":True,
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                                        }
                                                        linearray.append(obj)
                                                    if ("igst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                            print("second cond")
                                                            # code for discount making
                                                            # igst_dis=0
                                                            # for line in x['LineItems']:
                                                            #     if float(line['UnitAmount']) < 0:
                                                            #         if "Taxes" in line:
                                                            #             for tax in line['Taxes']:
                                                            #                 if ("igst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                            #                     igst_dis+=-(float(line['UnitAmount']))
                                                            # code for discount making ends
                                                            taxpercentage =float(m['TaxRate'])
                                                            cess=0
                                                            for t in y['Taxes']:
                                                                if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                    cess+=float(t['UnitAmount'])
                                                            if cess == 0:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": y['Description'],
                                                                    "taxRateName": "0",
                                                                    "gstRate":taxpercentage,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                            }
                                                            else:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": y['Description'],
                                                                    "taxRateName": "0",
                                                                    "gstRate":taxpercentage,
                                                                    "cess":cess,
                                                                    "flatCessFlag":True,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                            }
                                                            linearray.append(obj)
                                            else:
                                                # code for discount making
                                                # main_dis=0
                                                # for line in x['LineItems']:
                                                #     if float(line['UnitAmount']) < 0:
                                                #         if "Taxes" not in line:
                                                #             main_dis+=-(float(line['UnitAmount']))
                                                # code for discount making ends
                                                obj={
                                                    "saleType": "Normal",
                                                    "quantity": y['Quantity'],
                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                    "amount": 0,
                                                    "description": y['Description'],
                                                    "taxRateName": "0",
                                                    "gstRate":0,#change from None to 0
                                                    "discount":abs(float(y['DiscAmount'])) if "DiscAmount" in y else 0,# if condition by Amarpal
                                                    # "billOfSupplyGst":"Non-GST",
                                                    "hsnSac": y['hsncode'],
                                                    "type": "Goods",
                                                    "unitName": "Units",
                                                    "accountCode": accode,
                                                    "Transcode":y['TransCode']
                                                    }
                                                linearray.append(obj)
                                        else:
                                            pass
                                        transcode_arr.append(y['TransCode'])
                                    else:
                                        for lt in x['LineItems']:
                                            if y['ParentTransCode'] == lt['TransCode']:
                                                if y['ParentTransCode'] in transcode_arr:
                                                    for ob in linearray:
                                                        if ob['Transcode'] == y['ParentTransCode']:
                                                            ob['discount'] = abs(float(y['UnitAmount']))
                                                        else:
                                                            pass
                                                else:
                                                    obj={}
                                                    if "Taxes" in lt:
                                                        for m in lt['Taxes']:
                                                            # if m['TaxCode'] != "SERVICECHARGE" or m['TaxCode'] != "SERVICECHARGER" or m['TaxCode'] != "SGST1" or m['TaxCode'] != "CGSTP":
                                                            print(m['TaxCode'].lower())
                                                            if "vat" in ((m['TaxCode']).lower()):
                                                                # # code for discount making
                                                                # vat_dis=0
                                                                # for line in x['LineItems']:
                                                                #     if float(line['UnitAmount']) < 0:
                                                                #         if "Taxes" in line:
                                                                #             for tax in line['Taxes']:
                                                                #                 if (float(tax['UnitAmount']) < 0) and ("vat" in ((tax['TaxCode']).lower())):
                                                                #                     vat_dis+=-(float(line['UnitAmount']))
                                                                # # code for discount making ends
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": lt['Quantity'],
                                                                    "unitPrice": abs(float(lt['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": lt['Description'],
                                                                    "taxRateName": m['TaxRate'],
                                                                    "gstRate":None,
                                                                    "billOfSupplyGst":"Non-GST",
                                                                    "hsnSac": lt['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":lt['TransCode'],
                                                                    "discount":abs(float(y['UnitAmount']))
                                                                }
                                                                linearray.append(obj)
                                                            
                                                            if "service" in ((m['TaxCode']).lower()):
                                                                # code for discount making
                                                                # serv_dis=0
                                                                # for line in x['LineItems']:
                                                                #     if float(line['UnitAmount']) < 0:
                                                                #         if "Taxes" in line:
                                                                #             for tax in line['Taxes']:
                                                                #                 if (float(tax['UnitAmount']) < 0) and ("service" in ((tax['TaxCode']).lower())):
                                                                #                     serv_dis+=-(float(tax['UnitAmount']))
                                                                # code for discount making ends
                                                                cess=0
                                                                for t in lt['Taxes']:
                                                                    if (("cess" in ((t['TaxCode']).lower())) and ((t['ParentTaxCode'] == ((m['TaxCode']).lower())) or (t['ParentTaxCode'] == ((m['TaxCode']).lower())))):
                                                                        cess+=float(t['UnitAmount'])
                                                                print("kalash in first cond")
                                                                taxrate=0
                                                                for c in lt['Taxes']:
                                                                    if ((c['ParentTaxCode'] == ((m['TaxCode']).lower())) or (c['ParentTaxCode'] == ((m['TaxCode']).lower()))):
                                                                        taxrate+=float(c['TaxRate'])
                                                                print(taxrate)
                                                                if taxrate == 0 and cess == 0:
                                                                    obj={
                                                                        "saleTltpe": "Normal",
                                                                        "quantity": lt['Quantity'],
                                                                        "unitPrice": abs(float(lt['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": m['Description'],
                                                                        "taxRateName": m['TaxRate'],
                                                                        "gstRate":None,
                                                                        "billOfSupplyGst":"Non-GST",
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                    }
                                                                elif taxrate == 0 and cess != 0:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": lt['Quantity'],
                                                                        "unitPrice": abs(float(lt['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": m['Description'],
                                                                        "taxRateName": m['TaxRate'],
                                                                        "gstRate":None,
                                                                        "cess":cess,
                                                                        "flatCessFlag":True,
                                                                        "billOfSupplyGst":"Non-GST",
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                    }
                                                                elif taxrate != 0 and cess == 0:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": m['Quantity'],
                                                                        "unitPrice": abs(float(m['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": m['Description'],
                                                                        "taxRateName":"0",
                                                                        "gstRate":taxrate,
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                    }
                                                                else:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": m['Quantity'],
                                                                        "unitPrice": abs(float(m['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": m['Description'],
                                                                        "taxRateName": "0",
                                                                        "gstRate":taxrate,
                                                                        "cess":cess,
                                                                        "flatCessFlag":True,
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                    }
                                                                linearray.append(obj)
                                                            
                                                            if ("sgst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                                print("second cond")
                                                                # code for discount making
                                                                # sgst_dis=0
                                                                # for line in x['LineItems']:
                                                                #     if float(line['UnitAmount']) < 0:
                                                                #         if "Taxes" in line:
                                                                #             for tax in line['Taxes']:
                                                                #                 if ("sgst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                                #                     sgst_dis+=-(float(line['UnitAmount']))
                                                                # code for discount making ends
                                                                taxpercentage =float(m['TaxRate'])*2
                                                                cess=0
                                                                for t in lt['Taxes']:
                                                                    if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                        cess+=float(t['UnitAmount'])
                                                                if cess == 0:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": lt['Quantity'],
                                                                        "unitPrice": abs(float(lt['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": lt['Description'],
                                                                        "taxRateName": "0",
                                                                        "gstRate":taxpercentage,
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                                }
                                                                else:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": lt['Quantity'],
                                                                        "unitPrice": abs(float(lt['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": lt['Description'],
                                                                        "taxRateName": "0",
                                                                        "gstRate":taxpercentage,
                                                                        "cess":cess,
                                                                        "flatCessFlag":True,
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                                }
                                                                linearray.append(obj)
                                                            if ("igst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                                    print("second cond")
                                                                    # code for discount making
                                                                    # igst_dis=0
                                                                    # for line in x['LineItems']:
                                                                    #     if float(line['UnitAmount']) < 0:
                                                                    #         if "Taxes" in line:
                                                                    #             for tax in line['Taxes']:
                                                                    #                 if ("igst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                                    #                     igst_dis+=-(float(line['UnitAmount']))
                                                                    # code for discount making ends
                                                                    taxpercentage =float(m['TaxRate'])
                                                                    cess=0
                                                                    for t in lt['Taxes']:
                                                                        if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                            cess+=float(t['UnitAmount'])
                                                                    if cess == 0:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": lt['Description'],
                                                                            "taxRateName": "0",
                                                                            "gstRate":taxpercentage,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                                    }
                                                                    else:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": lt['Description'],
                                                                            "taxRateName": "0",
                                                                            "gstRate":taxpercentage,
                                                                            "cess":cess,
                                                                            "flatCessFlag":True,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                                    }
                                                                    linearray.append(obj)
                                                    else:
                                                        # code for discount making
                                                        # main_dis=0
                                                        # for line in x['LineItems']:
                                                        #     if float(line['UnitAmount']) < 0:
                                                        #         if "Taxes" not in line:
                                                        #             main_dis+=-(float(line['UnitAmount']))
                                                        # code for discount making ends
                                                        obj={
                                                            "saleType": "Normal",
                                                            "quantity": lt['Quantity'],
                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                            "amount": 0,
                                                            "description": lt['Description'],
                                                            "taxRateName": "0",
                                                            "gstRate":0,#change from None to 0
                                                            "discount":abs(float(lt['DiscAmount'])) if "DiscAmount" in lt else 0,# if condition by Amarpal
                                                            # "billOfSupplyGst":"Non-GST",
                                                            "hsnSac": lt['hsncode'],
                                                            "type": "Goods",
                                                            "unitName": "Units",
                                                            "accountCode": accode,
                                                            "Transcode":lt['TransCode']
                                                            }
                                                        linearray.append(obj)
                                                    transcode_arr.append(y['TransCode'])

                                for lts in linearray:
                                    del lts['Transcode']
                                print("in lineitems")
                                if "Addresses" not in x:
                                    print("kalash in address condition")
                                    # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                    #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                    # else:
                                    #     contactph=None
                                    if (x['Contact']['CompanyGstin'] == None) or (x['Contact']['CompanyGstin'] == ""):
                                        contactgstin=""
                                        cus_add_item={
                                        "contactList": [
                                            {
                                                "name": final_con_name,
                                                "accountNumber": final_con_code,
                                                "employee": False,
                                                "vendor": False,
                                                "customer": True,
                                                "primaryType": "customer",
                                                # "contactPerson": [
                                                #     {
                                                #         # "emailAddress": contactemail,
                                                #         "firstName": final_first_name,
                                                #         #  "lastName": x['Contact']['LastName'] or "",
                                                #         "primeFlag": 1
                                                #     }
                                                # ],
                                            # "mobile": contactph,
                                            "status": "COAC",
                                            }
                                        ]
                                    }
                                    else:
                                        contactgstin=x['Contact']['CompanyGstin']
                                        cus_add_item={
                                        "contactList": [
                                            {
                                                "name": final_con_name,
                                                "accountNumber": final_con_code,
                                                "employee": False,
                                                "vendor": False,
                                                "customer": True,
                                                "primaryType": "customer",
                                                # "contactPerson": [
                                                #     {
                                                #         # "emailAddress": contactemail,
                                                #         "firstName": final_first_name,
                                                #         #  "lastName": x['Contact']['LastName'] or "",
                                                #         "primeFlag": 1
                                                #     }
                                                # ],
                                            # "mobile": contactph,
                                                "contactGstin":[{
                                                "number": contactgstin,
                                                "verified": False,
                                                "billingAddress": {
                                                    "addressGSTIN": contactgstin,
                                                    "address1": address1,
                                                    "city": city,
                                                    "state": state,
                                                    "zip": zip,
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "BADR"
                                                },
                                                "shippingAddress": {
                                                    "addressGSTIN": contactgstin,
                                                    "address1": address1,
                                                    "city": city,
                                                    "state": state,
                                                    "zip": zip,
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "SADR"
                                                },
                                                "defaultGstin": True
                                            }],
                                            "status": "COAC",
                                            }
                                        ]
                                    }
                                    
                                    inv_add_item={
                                        "creditNoteList": [
                                            {
                                                "contactCode":final_con_code,
                                                "contactName":final_con_name,
                                                "placeSupplyName": state,
                                                "typeCode": "SSCN",
                                                "category": "",
                                                "originalInvoiceNumber": "",
                                                "originalInvoiceDate": "",
                                                "withMaterialFlag": False,
                                                "issueDate": "", 
                                                "number":x['InvoiceNumber'],
                                                "flatDiscountFlag":True,
                                                "roundFlag": False,
                                                "taxRateFlag":True,
                                                "currencyCode": "INR",
                                                "branch": branch,
                                                "date": newdate,
                                                "reference": x['ParentInvoiceNumber'],
                                                "customerGstin": contactgstin,
                                                "companyGstin": gstin,
                                                "txnType": "SCN",
                                                "taxType": "ETAX",
                                                "status": "SCNAP",
                                                "gstnType": "B2B",
                                                "billAddress": {
                                                    "name":bill_ship_name,
                                                    "address1": address1,
                                                    "city":city,
                                                    "state":state,
                                                    "zip":zip,
                                                    "country": "INDIA",
                                                    "pan": "",
                                                    "gstin":None,
                                                    "type": "BADR"	
                                                    
                                                },
                                                "shipAddress": {
                                                    "name":bill_ship_name,
                                                    "address1": address1,
                                                    "city":city,
                                                    "state":state,
                                                    "zip":zip,
                                                    "country": "INDIA",
                                                    "pan": "",
                                                    "gstin":None,
                                                    "type": "SADR"
                                                },
                                                    
                                                "amount": 0,
                                                "lineItems": linearray
                                            }
                                        ]
                                    }   
                                elif x['Contact']['CompanyGstin'] == "null":
                                    print("kalassh in elif condition in customer")
                                    # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                    #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                    # else:
                                    #     contactph=None
                                    cus_add_item={
                                        "contactList": [
                                            {
                                                "name": final_con_name,
                                                "accountNumber": final_con_code,
                                                "employee": False,
                                                "vendor": False,
                                                "customer": True,
                                                "primaryType": "customer",
                                                # "contactPerson": [
                                                #     {
                                                #         # "emailAddress": contactemail,
                                                #         "firstName": final_first_name,
                                                #         #"lastName": x['Contact']['LastName'] or "",
                                                #         "primeFlag": 1
                                                #     }
                                                # ],
                                            # "mobile": contactph,
                                                "address": [
                                                {
                                                    "addressGSTIN": None,
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city": x['Contact']['Addresses']['Address']['City'],
                                                    "state": None,
                                                    "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    # "telephone": contactph,
                                                    "type": "PADR"
                                                }
                                            ],
                                            "status": "COAC",
                                            }
                                        ]
                                    }
                                    inv_add_item={
                                        "creditNoteList": [
                                            {
                                                "contactCode": final_con_code,
                                                "contactName":  final_con_name,
                                                "placeSupplyName": state,
                                                "typeCode": "SSCN",
                                                "category": "",
                                                "originalInvoiceNumber": "",
                                                "originalInvoiceDate": "",
                                                "withMaterialFlag": False,
                                                "issueDate": "", 
                                                "number":x['InvoiceNumber'],
                                                "flatDiscountFlag":True,
                                                "roundFlag": False,
                                                "taxRateFlag":True,
                                                "currencyCode": "INR",
                                                "branch": branch,
                                                "date": newdate,
                                                "reference":x['ParentInvoiceNumber'],
                                                "customerGstin":None,
                                                "companyGstin": gstin,
                                                "txnType": "SCN",
                                                "taxType": "ETAX",
                                                "status": "SCNAP",
                                                "gstnType": "B2B",
                                                "billAddress": {
                                                    "name":bill_ship_name,
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'], 
                                                    "city":x['Contact']['Addresses']['Address']['City'],
                                                    "state":state,
                                                    "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    "pan": "",
                                                    "gstin": None,
                                                    "type": "BADR"	
                                                    
                                                },
                                                "shipAddress": {
                                                    "name":bill_ship_name,
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'], 
                                                    "city":x['Contact']['Addresses']['Address']['City'],
                                                    "state":state,
                                                    "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    "pan": "",
                                                    "gstin": None,
                                                    "type": "SADR"
                                                },
                                                    
                                                "amount": 0,
                                                "lineItems": linearray
                                            }
                                        ]
                                    }
                                    
                                else:
                                    # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                    #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                    # else:
                                    #     contactph=None
                                    cus_add_item={
                                        "contactList": [
                                            {
                                                "name": final_con_name,
                                                "accountNumber": final_con_code,
                                                "employee": False,
                                                "vendor": False,
                                                "customer": True,
                                                "primaryType": "customer",
                                                # "contactPerson": [
                                                #     {
                                                #         # "emailAddress": contactemail,
                                                #         "firstName": final_first_name,
                                                #         # "lastName": x['Contact']['LastName'] or "",
                                                #         "primeFlag": 1
                                                #     }
                                                # ],
                                            # "mobile": contactph,
                                            "address": [
                                                {
                                                    "addressGSTIN": x['Contact']['CompanyGstin'],
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city": x['Contact']['Addresses']['Address']['City'],
                                                    "state": state,
                                                    "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    # "telephone": contactph,
                                                    "type": "PADR"
                                                }
                                            ],
                                                "contactGstin":[{
                                                "number": x['Contact']['CompanyGstin'],
                                                "verified": False,
                                                "billingAddress": {
                                                    "addressGSTIN": x['Contact']['CompanyGstin'],
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city": x['Contact']['Addresses']['Address']['City'],
                                                    "state": state,
                                                    "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "BADR"
                                                },
                                                "shippingAddress": {
                                                    "addressGSTIN": x['Contact']['CompanyGstin'],
                                                    "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city": x['Contact']['Addresses']['Address']['City'],
                                                    "state": state,
                                                    "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "SADR"
                                                },
                                                "defaultGstin": True
                                            }],
                                            "status": "COAC",
                                            }
                                        ]
                                    }
                                    inv_add_item={
                                    "creditNoteList": [
                                        {
                                            "contactCode": final_con_code,
                                            "contactName": final_con_name,
                                            "placeSupplyName": state,
                                            "typeCode": "SSCN",
                                            "category": "",
                                            "originalInvoiceNumber": "",
                                            "originalInvoiceDate": "",
                                            "withMaterialFlag": False,
                                            "issueDate": "", 
                                            "number":x['InvoiceNumber'],
                                            "flatDiscountFlag":True,
                                            "roundFlag": False,
                                            "taxRateFlag":True,
                                            "currencyCode": "INR",
                                            "branch": branch,
                                            "date": newdate,
                                            "reference": x['ParentInvoiceNumber'],
                                            "customerGstin": x['Contact']['CompanyGstin'],
                                            "companyGstin":  gstin,
                                            "txnType": "SCN",
                                            "taxType": "ETAX",
                                            "status": "SCNAP",
                                            "gstnType": "B2B",
                                            "billAddress": {
                                                "name":bill_ship_name,
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city":x['Contact']['Addresses']['Address']['City'],
                                                "state":state,
                                                "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                "pan": "",
                                                "gstin":x['Contact']['CompanyGstin'],
                                                "type": "BADR"	
                                                
                                            },
                                            "shipAddress": {
                                                "name":bill_ship_name,
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city":x['Contact']['Addresses']['Address']['City'],
                                                "state":state,
                                                "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                "pan": "",
                                                "gstin": x['Contact']['CompanyGstin'],
                                                "type": "SADR"
                                            },
                                                
                                            "amount": 0,
                                            "lineItems": linearray
                                        }
                                    ]
                                }   
                            else:
                                    print("else cond con name --->",final_con_name)
                                    txntype="INV"
                                    # inv_status="SUCCESS"
                                    # invoice_code=x['InvoiceCode']
                                    # paycode_array=[]
                                    # if "Payments" in x:
                                    #     for pay in x['Payments']:
                                    #         print("kalash in payment")
                                    #         code=pay['PaymentCode']
                                    #         paycode_array.append(code)
                                    # update_inv_status(invoice_code,paycode_array,hotelid,token,inv_status)
                                    # inputdate=x['Date']
                                    dataarr=inputdate.split("-")
                                    newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                    print(newdate)
                                    inputduedate=x['DueDate']
                                    dataarr=inputduedate.split("-")
                                    newduedate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                    print(newduedate)
                                    cus_add_item={}
                                    inv_add_item={}
                                    linearray=[]
                                    transcode_arr=[]
                                    for y in x['LineItems']:
                                        accode=y['AccountCode']
                                        for row in ledger_settings:
                                            accode=y['AccountCode']
                                            acc_code=row['ledgerCode']
                                            if acc_code == accode:
                                                accode=row['Acc_Code']
                                                break
                                            else:
                                                accode="Not Found"
                                        if accode == "Not Found":
                                            return Response (f"{y['AccountCode']} is missing in ledger settings")
                                        else:
                                            pass
                                        # if accode == y['AccountCode']:
                                        #     accode="Not Found"
                                        if y['ParentTransCode'] == "" or y['ParentTransCode'] == None:
                                            if y['TransCode'] not in transcode_arr:
                                                obj={}
                                                if "Taxes" in y:
                                                    for m in y['Taxes']:
                                                        # if m['TaxCode'] != "SERVICECHARGE" or m['TaxCode'] != "SERVICECHARGER" or m['TaxCode'] != "SGST1" or m['TaxCode'] != "CGSTP":
                                                        print(m['TaxCode'].lower())
                                                        if "vat" in ((m['TaxCode']).lower()):
                                                            # # code for discount making
                                                            # vat_dis=0
                                                            # for line in x['LineItems']:
                                                            #     if float(line['UnitAmount']) < 0:
                                                            #         if "Taxes" in line:
                                                            #             for tax in line['Taxes']:
                                                            #                 if (float(tax['UnitAmount']) < 0) and ("vat" in ((tax['TaxCode']).lower())):
                                                            #                     vat_dis+=-(float(line['UnitAmount']))
                                                            # # code for discount making ends
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": y['Quantity'],
                                                                "unitPrice": abs(float(y['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": y['Description'],
                                                                "taxRateName": m['TaxRate'],
                                                                "gstRate":None,
                                                                "billOfSupplyGst":"Non-GST",
                                                                "hsnSac": y['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":y['TransCode']
                                                            }
                                                            linearray.append(obj)
                                                        
                                                        if "service" in ((m['TaxCode']).lower()):
                                                            # code for discount making
                                                            # serv_dis=0
                                                            # for line in x['LineItems']:
                                                            #     if float(line['UnitAmount']) < 0:
                                                            #         if "Taxes" in line:
                                                            #             for tax in line['Taxes']:
                                                            #                 if (float(tax['UnitAmount']) < 0) and ("service" in ((tax['TaxCode']).lower())):
                                                            #                     serv_dis+=-(float(tax['UnitAmount']))
                                                            # code for discount making ends
                                                            cess=0
                                                            for t in y['Taxes']:
                                                                if (("cess" in ((t['TaxCode']).lower())) and ((t['ParentTaxCode'] == ((m['TaxCode']).lower())) or (t['ParentTaxCode'] == ((m['TaxCode']).lower())))):
                                                                    cess+=float(t['UnitAmount'])
                                                            print("kalash in first cond")
                                                            taxrate=0
                                                            for c in y['Taxes']:
                                                                if ((c['ParentTaxCode'] == ((m['TaxCode']).lower())) or (c['ParentTaxCode'] == ((m['TaxCode']).lower()))):
                                                                    taxrate+=float(c['TaxRate'])
                                                            print(taxrate)
                                                            if taxrate == 0 and cess == 0:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": m['Description'],
                                                                    "taxRateName": m['TaxRate'],
                                                                    "gstRate":None,
                                                                    "billOfSupplyGst":"Non-GST",
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                }
                                                            elif taxrate == 0 and cess != 0:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": m['Description'],
                                                                    "taxRateName": m['TaxRate'],
                                                                    "gstRate":None,
                                                                    "cess":cess,
                                                                    "flatCessFlag":True,
                                                                    "billOfSupplyGst":"Non-GST",
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                }
                                                            elif taxrate != 0 and cess == 0:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": m['Quantity'],
                                                                    "unitPrice": abs(float(m['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": m['Description'],
                                                                    "taxRateName":"0",
                                                                    "gstRate":taxrate,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                }
                                                            else:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": m['Quantity'],
                                                                    "unitPrice": abs(float(m['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": m['Description'],
                                                                    "taxRateName": "0",
                                                                    "gstRate":taxrate,
                                                                    "cess":cess,
                                                                    "flatCessFlag":True,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                }
                                                            linearray.append(obj)
                                                        
                                                        if ("sgst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                            print("second cond")
                                                            # code for discount making
                                                            # sgst_dis=0
                                                            # for line in x['LineItems']:
                                                            #     if float(line['UnitAmount']) < 0:
                                                            #         if "Taxes" in line:
                                                            #             for tax in line['Taxes']:
                                                            #                 if ("sgst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                            #                     sgst_dis+=-(float(line['UnitAmount']))
                                                            # code for discount making ends
                                                            taxpercentage =float(m['TaxRate'])*2
                                                            cess=0
                                                            for t in y['Taxes']:
                                                                if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                    cess+=float(t['UnitAmount'])
                                                            if cess == 0:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": y['Description'],
                                                                    "taxRateName": "0",
                                                                    "gstRate":taxpercentage,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                            }
                                                            else:
                                                                obj={
                                                                    "saleType": "Normal",
                                                                    "quantity": y['Quantity'],
                                                                    "unitPrice": abs(float(y['UnitAmount'])),
                                                                    "amount": 0,
                                                                    "description": y['Description'],
                                                                    "taxRateName": "0",
                                                                    "gstRate":taxpercentage,
                                                                    "cess":cess,
                                                                    "flatCessFlag":True,
                                                                    "hsnSac": y['hsncode'],
                                                                    "type": "Goods",
                                                                    "unitName": "Units",
                                                                    "accountCode": accode,
                                                                    "Transcode":y['TransCode']
                                                                            }
                                                            linearray.append(obj)
                                                        if ("igst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                                print("second cond")
                                                                # code for discount making
                                                                # igst_dis=0
                                                                # for line in x['LineItems']:
                                                                #     if float(line['UnitAmount']) < 0:
                                                                #         if "Taxes" in line:
                                                                #             for tax in line['Taxes']:
                                                                #                 if ("igst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                                #                     igst_dis+=-(float(line['UnitAmount']))
                                                                # code for discount making ends
                                                                taxpercentage =float(m['TaxRate'])
                                                                cess=0
                                                                for t in y['Taxes']:
                                                                    if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                        cess+=float(t['UnitAmount'])
                                                                if cess == 0:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": y['Quantity'],
                                                                        "unitPrice": abs(float(y['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": y['Description'],
                                                                        "taxRateName": "0",
                                                                        "gstRate":taxpercentage,
                                                                        "hsnSac": y['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":y['TransCode']
                                                                                }
                                                                else:
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": y['Quantity'],
                                                                        "unitPrice": abs(float(y['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": y['Description'],
                                                                        "taxRateName": "0",
                                                                        "gstRate":taxpercentage,
                                                                        "cess":cess,
                                                                        "flatCessFlag":True,
                                                                        "hsnSac": y['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":y['TransCode']
                                                                                }
                                                                linearray.append(obj)
                                                else:
                                                    # code for discount making
                                                    # main_dis=0
                                                    # for line in x['LineItems']:
                                                    #     if float(line['UnitAmount']) < 0:
                                                    #         if "Taxes" not in line:
                                                    #             main_dis+=-(float(line['UnitAmount']))
                                                    # code for discount making ends
                                                    obj={
                                                        "saleType": "Normal",
                                                        "quantity": y['Quantity'],
                                                        "unitPrice": abs(float(y['UnitAmount'])),
                                                        "amount": 0,
                                                        "description": y['Description'],
                                                        "taxRateName": "0",
                                                        "gstRate":0,#change from None to 0
                                                        "discount":y['DiscAmount'] if "DiscAmount" in y else 0,# if condition by Amarpal
                                                        # "billOfSupplyGst":"Non-GST",
                                                        "hsnSac": y['hsncode'],
                                                        "type": "Goods",
                                                        "unitName": "Units",
                                                        "accountCode": accode,
                                                        "Transcode":y['TransCode']
                                                        }
                                                    linearray.append(obj)
                                            else:
                                                pass
                                            transcode_arr.append(y['TransCode'])
                                        else:
                                            for lt in x['LineItems']:
                                                if y['ParentTransCode'] == lt['TransCode']:
                                                    if y['ParentTransCode'] in transcode_arr:
                                                        for ob in linearray:
                                                            if ob['Transcode'] == y['ParentTransCode']:
                                                                ob['discount'] = abs(float(y['UnitAmount']))
                                                            else:
                                                                pass
                                                    else:
                                                        obj={}
                                                        if "Taxes" in lt:
                                                            for m in lt['Taxes']:
                                                                # if m['TaxCode'] != "SERVICECHARGE" or m['TaxCode'] != "SERVICECHARGER" or m['TaxCode'] != "SGST1" or m['TaxCode'] != "CGSTP":
                                                                print(m['TaxCode'].lower())
                                                                if "vat" in ((m['TaxCode']).lower()):
                                                                    # # code for discount making
                                                                    # vat_dis=0
                                                                    # for line in x['LineItems']:
                                                                    #     if float(line['UnitAmount']) < 0:
                                                                    #         if "Taxes" in line:
                                                                    #             for tax in line['Taxes']:
                                                                    #                 if (float(tax['UnitAmount']) < 0) and ("vat" in ((tax['TaxCode']).lower())):
                                                                    #                     vat_dis+=-(float(line['UnitAmount']))
                                                                    # # code for discount making ends
                                                                    obj={
                                                                        "saleType": "Normal",
                                                                        "quantity": lt['Quantity'],
                                                                        "unitPrice": abs(float(lt['UnitAmount'])),
                                                                        "amount": 0,
                                                                        "description": lt['Description'],
                                                                        "taxRateName": m['TaxRate'],
                                                                        "gstRate":None,
                                                                        "billOfSupplyGst":"Non-GST",
                                                                        "hsnSac": lt['hsncode'],
                                                                        "type": "Goods",
                                                                        "unitName": "Units",
                                                                        "accountCode": accode,
                                                                        "Transcode":lt['TransCode'],
                                                                        "discount":abs(float(y['UnitAmount']))
                                                                    }
                                                                    linearray.append(obj)
                                                                
                                                                if "service" in ((m['TaxCode']).lower()):
                                                                    # code for discount making
                                                                    # serv_dis=0
                                                                    # for line in x['LineItems']:
                                                                    #     if float(line['UnitAmount']) < 0:
                                                                    #         if "Taxes" in line:
                                                                    #             for tax in line['Taxes']:
                                                                    #                 if (float(tax['UnitAmount']) < 0) and ("service" in ((tax['TaxCode']).lower())):
                                                                    #                     serv_dis+=-(float(tax['UnitAmount']))
                                                                    # code for discount making ends
                                                                    cess=0
                                                                    for t in lt['Taxes']:
                                                                        if (("cess" in ((t['TaxCode']).lower())) and ((t['ParentTaxCode'] == ((m['TaxCode']).lower())) or (t['ParentTaxCode'] == ((m['TaxCode']).lower())))):
                                                                            cess+=float(t['UnitAmount'])
                                                                    print("kalash in first cond")
                                                                    taxrate=0
                                                                    for c in lt['Taxes']:
                                                                        if ((c['ParentTaxCode'] == ((m['TaxCode']).lower())) or (c['ParentTaxCode'] == ((m['TaxCode']).lower()))):
                                                                            taxrate+=float(c['TaxRate'])
                                                                    print(taxrate)
                                                                    if taxrate == 0 and cess == 0:
                                                                        obj={
                                                                            "saleTltpe": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": m['Description'],
                                                                            "taxRateName": m['TaxRate'],
                                                                            "gstRate":None,
                                                                            "billOfSupplyGst":"Non-GST",
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                        }
                                                                    elif taxrate == 0 and cess != 0:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": m['Description'],
                                                                            "taxRateName": m['TaxRate'],
                                                                            "gstRate":None,
                                                                            "cess":cess,
                                                                            "flatCessFlag":True,
                                                                            "billOfSupplyGst":"Non-GST",
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                        }
                                                                    elif taxrate != 0 and cess == 0:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": m['Quantity'],
                                                                            "unitPrice": abs(float(m['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": m['Description'],
                                                                            "taxRateName":"0",
                                                                            "gstRate":taxrate,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                        }
                                                                    else:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": m['Quantity'],
                                                                            "unitPrice": abs(float(m['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": m['Description'],
                                                                            "taxRateName": "0",
                                                                            "gstRate":taxrate,
                                                                            "cess":cess,
                                                                            "flatCessFlag":True,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                        }
                                                                    linearray.append(obj)
                                                                
                                                                if ("sgst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                                    print("second cond")
                                                                    # code for discount making
                                                                    # sgst_dis=0
                                                                    # for line in x['LineItems']:
                                                                    #     if float(line['UnitAmount']) < 0:
                                                                    #         if "Taxes" in line:
                                                                    #             for tax in line['Taxes']:
                                                                    #                 if ("sgst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                                    #                     sgst_dis+=-(float(line['UnitAmount']))
                                                                    # code for discount making ends
                                                                    taxpercentage =float(m['TaxRate'])*2
                                                                    cess=0
                                                                    for t in lt['Taxes']:
                                                                        if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                            cess+=float(t['UnitAmount'])
                                                                    if cess == 0:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": lt['Description'],
                                                                            "taxRateName": "0",
                                                                            "gstRate":taxpercentage,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                                    }
                                                                    else:
                                                                        obj={
                                                                            "saleType": "Normal",
                                                                            "quantity": lt['Quantity'],
                                                                            "unitPrice": abs(float(lt['UnitAmount'])),
                                                                            "amount": 0,
                                                                            "description": lt['Description'],
                                                                            "taxRateName": "0",
                                                                            "gstRate":taxpercentage,
                                                                            "cess":cess,
                                                                            "flatCessFlag":True,
                                                                            "hsnSac": lt['hsncode'],
                                                                            "type": "Goods",
                                                                            "unitName": "Units",
                                                                            "accountCode": accode,
                                                                            "Transcode":lt['TransCode'],
                                                                            "discount":abs(float(y['UnitAmount']))
                                                                                    }
                                                                    linearray.append(obj)
                                                                if ("igst" in ((m['TaxCode']).lower()) and m['ParentTaxCode'] == None ):
                                                                        print("second cond")
                                                                        # code for discount making
                                                                        # igst_dis=0
                                                                        # for line in x['LineItems']:
                                                                        #     if float(line['UnitAmount']) < 0:
                                                                        #         if "Taxes" in line:
                                                                        #             for tax in line['Taxes']:
                                                                        #                 if ("igst" in ((tax['TaxCode']).lower()) and tax['ParentTaxCode'] == None ):
                                                                        #                     igst_dis+=-(float(line['UnitAmount']))
                                                                        # code for discount making ends
                                                                        taxpercentage =float(m['TaxRate'])
                                                                        cess=0
                                                                        for t in lt['Taxes']:
                                                                            if ("cess" in ((t['TaxCode']).lower()) and t['ParentTaxCode'] == None):
                                                                                cess+=float(t['UnitAmount'])
                                                                        if cess == 0:
                                                                            obj={
                                                                                "saleType": "Normal",
                                                                                "quantity": lt['Quantity'],
                                                                                "unitPrice": abs(float(lt['UnitAmount'])),
                                                                                "amount": 0,
                                                                                "description": lt['Description'],
                                                                                "taxRateName": "0",
                                                                                "gstRate":taxpercentage,
                                                                                "hsnSac": lt['hsncode'],
                                                                                "type": "Goods",
                                                                                "unitName": "Units",
                                                                                "accountCode": accode,
                                                                                "Transcode":lt['TransCode'],
                                                                                "discount":abs(float(y['UnitAmount']))
                                                                                        }
                                                                        else:
                                                                            obj={
                                                                                "saleType": "Normal",
                                                                                "quantity": lt['Quantity'],
                                                                                "unitPrice": (abs(lt['UnitAmount'])),
                                                                                "amount": 0,
                                                                                "description": lt['Description'],
                                                                                "taxRateName": "0",
                                                                                "gstRate":taxpercentage,
                                                                                "cess":cess,
                                                                                "flatCessFlag":True,
                                                                                "hsnSac": lt['hsncode'],
                                                                                "type": "Goods",
                                                                                "unitName": "Units",
                                                                                "accountCode": accode,
                                                                                "Transcode":lt['TransCode'],
                                                                                "discount":abs(float(y['UnitAmount']))
                                                                                        }
                                                                        linearray.append(obj)
                                                        else:
                                                            # code for discount making
                                                            # main_dis=0
                                                            # for line in x['LineItems']:
                                                            #     if float(line['UnitAmount']) < 0:
                                                            #         if "Taxes" not in line:
                                                            #             main_dis+=-(float(line['UnitAmount']))
                                                            # code for discount making ends
                                                            obj={
                                                                "saleType": "Normal",
                                                                "quantity": lt['Quantity'],
                                                                "unitPrice": (abs(lt['UnitAmount'])),
                                                                "amount": 0,
                                                                "description": lt['Description'],
                                                                "taxRateName": "0",
                                                                "gstRate":0,#change from None to 0
                                                                "discount":abs(float(lt['DiscAmount'])) if "DiscAmount" in lt else 0,# if condition by Amarpal
                                                                # "billOfSupplyGst":"Non-GST",
                                                                "hsnSac": lt['hsncode'],
                                                                "type": "Goods",
                                                                "unitName": "Units",
                                                                "accountCode": accode,
                                                                "Transcode":lt['TransCode']
                                                                }
                                                            linearray.append(obj)
                                                        transcode_arr.append(y['TransCode'])
                                                        
                                    for lts in linearray:
                                        del lts['Transcode']
                                    print("in lineitems")
                                    if "Addresses" not in x:
                                        print("kalash in address condition")
                                        # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                        #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                        # else:
                                        #     contactph=None
                                        if (x['Contact']['CompanyGstin'] == None) or (x['Contact']['CompanyGstin'] == ""):
                                            contactgstin=""
                                            cus_add_item={
                                            "contactList": [
                                                {
                                                    "name": final_con_name,
                                                    "accountNumber": final_con_code,
                                                    "employee": False,
                                                    "vendor": False,
                                                    "customer": True,
                                                    "primaryType": "customer",
                                                    # "contactPerson": [
                                                    #     {
                                                    #         # "emailAddress": contactemail,
                                                    #         # "firstName": final_first_name,
                                                    #        # "lastName": x['Contact']['LastName'] or "",
                                                    #         "primeFlag": 1
                                                    #     }
                                                    # ],
                                                # "mobile": contactph,
                                                "status": "COAC",
                                                }
                                            ]
                                        }
                                        else:
                                            contactgstin=x['Contact']['CompanyGstin']
                                            cus_add_item={
                                            "contactList": [
                                                {
                                                    "name": final_con_name,
                                                    "accountNumber": final_con_code,
                                                    "employee": False,
                                                    "vendor": False,
                                                    "customer": True,
                                                    "primaryType": "customer",
                                                    # "contactPerson": [
                                                    #     {
                                                    #         # "emailAddress": contactemail,
                                                    #         # "firstName": final_first_name,
                                                    #        # "lastName": x['Contact']['LastName'] or "",
                                                    #         "primeFlag": 1
                                                    #     }
                                                    # ],
                                                # "mobile": contactph,
                                                    "contactGstin":[{
                                                    "number": contactgstin,
                                                    "verified": False,
                                                    "billingAddress": {
                                                        "addressGSTIN": contactgstin,
                                                        "address1": address1,
                                                        "city": city,
                                                        "state": state,
                                                        "zip": zip,
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        "pan": None,
                                                        "tan": None,
                                                        "gstin": None,
                                                        "cin": None,
                                                        # "telephone": contactph,
                                                        "type": "BADR"
                                                    },
                                                    "shippingAddress": {
                                                        "addressGSTIN": contactgstin,
                                                        "address1": address1,
                                                        "city": city,
                                                        "state": state,
                                                        "zip": zip,
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        "pan": None,
                                                        "tan": None,
                                                        "gstin": None,
                                                        "cin": None,
                                                        # "telephone": contactph,
                                                        "type": "SADR"
                                                    },
                                                    "defaultGstin": True
                                                }],
                                                "status": "COAC",
                                                }
                                            ]
                                        }
                                        
                                        inv_add_item={
                                            "invoiceList": [
                                                {
                                                    "taxType": "ETAX",
                                                    "currencyCode": "INR",
                                                    "priceGroupName": None,
                                                    "companyGstin": gstin,
                                                    "branch": branch,
                                                    "category": "", 
                                                    "countrySupply": None,
                                                    "invoiceType":"R",
                                                    "date":newdate,
                                                    "dueDate": newduedate, 
                                                    "contactCode": final_con_code,
                                                    "contactName": final_con_name,
                                                    "customerGstin": contactgstin,
                                                    "placeSupplyName": state,
                                                    "billAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": address1,
                                                        "city":city,
                                                        "state":state,
                                                        "zip":zip,
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": None,
                                                        "type": "BADR"	
                                                    },
                                                "shipAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": address1,
                                                        "city":city,
                                                        "state":state,
                                                        "zip":zip,
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": None,
                                                        "type": "SADR"
                                                    },
                                                    "termCondition": None,
                                                    "customersNotes": None,
                                                    "otherReference": None,
                                                    "termsOfPayment": None,
                                                    "amount": 0,
                                                    "roundingAmount": 0,
                                                    "number": x['InvoiceNumber'],
                                                    "flatDiscountFlag":True,
                                                    "roundFlag": False,
                                                    "taxRateFlag":True,
                                                    "lineItems": linearray,
                                                    "typeCode": "SINV",
                                                    "status": saveas,
                                                    "gstnType": "B2B"
                                                }
                                            ]
                                        }                
                                    elif x['Contact']['CompanyGstin'] == "null":
                                        print("kalassh in elif condition in customer")
                                        # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                        #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                        # else:
                                        #     contactph=None
                                        cus_add_item={
                                            "contactList": [
                                                {
                                                    "name": final_con_name,
                                                    "accountNumber": final_con_code,
                                                    "employee": False,
                                                    "vendor": False,
                                                    "customer": True,
                                                    "primaryType": "customer",
                                                    # "contactPerson": [
                                                    #     {
                                                    #         # "emailAddress": contactemail,
                                                    #         # "firstName": final_first_name,
                                                    #       #  "lastName": x['Contact']['LastName'] or "",
                                                    #         "primeFlag": 1
                                                    #     }
                                                    # ],
                                                # "mobile": contactph,
                                                    "address": [
                                                    {
                                                        "addressGSTIN": None,
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city": x['Contact']['Addresses']['Address']['City'],
                                                        "state": None,
                                                        "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        # "telephone": contactph,
                                                        "type": "PADR"
                                                    }
                                                ],
                                                "status": "COAC",
                                                }
                                            ]
                                        }
                                        inv_add_item={
                                            "invoiceList": [
                                                {
                                                    "taxType": "ETAX",
                                                    "currencyCode": "INR",
                                                    "priceGroupName": None,
                                                    "companyGstin": gstin,
                                                    "branch": branch,
                                                    "category": "", 
                                                    "countrySupply": None,
                                                    "invoiceType":"NA",
                                                    "date":newdate,
                                                    "dueDate": newduedate, 
                                                    "contactCode": final_con_code,
                                                    "contactName": final_con_name,
                                                    "customerGstin": None,
                                                    "placeSupplyName": state,
                                                    "billAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city":x['Contact']['Addresses']['Address']['City'],
                                                        "state":state,
                                                        "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": None,
                                                        "type": "BADR"	
                                                    },
                                                "shipAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city":x['Contact']['Addresses']['Address']['City'],
                                                        "state":state,
                                                        "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": None,
                                                        "type": "SADR"
                                                    },
                                                    "termCondition": None,
                                                    "customersNotes": None,
                                                    "otherReference": None,
                                                "termsOfPayment": None,
                                                "amount": 0,
                                                    "roundingAmount": 0,
                                                    "number": x['InvoiceNumber'],
                                                    "flatDiscountFlag":True,
                                                    "roundFlag": False,
                                                    "taxRateFlag":True,
                                                    "lineItems": linearray,
                                                    "typeCode": "SINV",
                                                    "status": saveas,
                                                    "gstnType": "B2C"
                                                }
                                            ]
                                        }
                                    else:
                                        # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                        #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                        # else:
                                        #     contactph=None
                                        cus_add_item={
                                            "contactList": [
                                                {
                                                    "name": final_con_name,
                                                    "accountNumber": final_con_code,
                                                    "employee": False,
                                                    "vendor": False,
                                                    "customer": True,
                                                    "primaryType": "customer",
                                                    # "contactPerson": [
                                                    #     {
                                                    #         # "emailAddress": contactemail,
                                                    #         # "firstName": final_first_name,
                                                    #       #  "lastName": x['Contact']['LastName'] or "",
                                                    #         "primeFlag": 1
                                                    #     }
                                                    # ],
                                                # "mobile": contactph,
                                                "address": [
                                                    {
                                                        "addressGSTIN": x['Contact']['CompanyGstin'],
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city": x['Contact']['Addresses']['Address']['City'],
                                                        "state": state,
                                                        "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        # "telephone": contactph,
                                                        "type": "PADR"
                                                    }
                                                ],
                                                    "contactGstin":[{
                                                    "number": x['Contact']['CompanyGstin'],
                                                    "verified": False,
                                                    "billingAddress": {
                                                        "addressGSTIN": x['Contact']['CompanyGstin'],
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city": x['Contact']['Addresses']['Address']['City'],
                                                        "state": state,
                                                        "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        "pan": None,
                                                        "tan": None,
                                                        "gstin": None,
                                                        "cin": None,
                                                        # "telephone": contactph,
                                                        "type": "BADR"
                                                    },
                                                    "shippingAddress": {
                                                        "addressGSTIN": x['Contact']['CompanyGstin'],
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city": x['Contact']['Addresses']['Address']['City'],
                                                        "state": state,
                                                        "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        # "mobile": contactph,
                                                        "pan": None,
                                                        "tan": None,
                                                        "gstin": None,
                                                        "cin": None,
                                                        # "telephone": contactph,
                                                        "type": "SADR"
                                                    },
                                                    "defaultGstin": True
                                                }],
                                                "status": "COAC",
                                                }
                                            ]
                                        }
                                        inv_add_item={
                                            "invoiceList": [
                                                {
                                                    "taxType": "ETAX",
                                                    "currencyCode": "INR",
                                                    "priceGroupName": None,
                                                    "companyGstin": gstin,
                                                    "branch": branch,
                                                    "category": "", 
                                                    "countrySupply": None,
                                                    "invoiceType":"R",
                                                    "date":newdate,
                                                    "dueDate": newduedate, 
                                                    "contactCode": final_con_code,
                                                    "contactName": final_con_name,
                                                    "customerGstin": x['Contact']['CompanyGstin'],
                                                    "placeSupplyName": state,
                                                    "billAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city":x['Contact']['Addresses']['Address']['City'],
                                                        "state":state,
                                                        "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": x['Contact']['CompanyGstin'],
                                                        "type": "BADR"	
                                                    },
                                                "shipAddress": {
                                                        "name":bill_ship_name,
                                                        "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                        "city":x['Contact']['Addresses']['Address']['City'],
                                                        "state":state,
                                                        "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                        "country": "INDIA",
                                                        "pan": "",
                                                        "gstin": x['Contact']['CompanyGstin'],
                                                        "type": "SADR"
                                                    },
                                                    "termCondition": None,
                                                    "customersNotes": None,
                                                    "otherReference": None,
                                                "termsOfPayment": None,
                                                "amount": 0,
                                                    "roundingAmount": 0,
                                                    "number": x['InvoiceNumber'],
                                                    "flatDiscountFlag":True,
                                                    "roundFlag": False,
                                                    "taxRateFlag":True,
                                                    "lineItems": linearray,
                                                    "typeCode": "SINV",
                                                    "status": saveas,
                                                    "gstnType": "B2B"
                                                }
                                            ]
                                        }

                            noMatchCode=0
                            for j in linearray:
                                print("kalash in loop")
                                if j['accountCode'] == "Not Found":
                                    noMatchCode+=1
                            if noMatchCode == 0:
                                print("kalash is in if cond")
                                # sync of contacts starts
                                customerurl=acc_mas_url
                                headers={
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }
                                add_item=cus_add_item
                                r=requests.post(customerurl, headers=headers,json=add_item)
                                res_cus=r.json()
                                print(res_cus)
                                print("customers accounting response")
                                print(add_item)
                                if res_cus['message'] == "Batch Data Added successfully":
                                    print("if condition")
                                    message=res_cus['message']
                                    status="SUCCESS"
                                    # ErrorFileJson[x['InvoiceNumber']]['Customers']=message
                                    ErrorFileJson[x['InvoiceNumber']]={
                                        "Customers":message
                                    }
                                elif res_cus['message'] == "Some Data is not valid and other batch data added successfully":
                                    print("elif condition")
                                    if res_cus['fieldErrors'] != None:
                                        fielderror=res_cus['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
                                    else:
                                        message=res_cus['errorList'].values()
                                    status="FAILED"
                                    print("error log list -->",ErrorFileJson)
                                    # ErrorFileJson[x['InvoiceNumber']]['Customers']=message
                                    ErrorFileJson[x['InvoiceNumber']]={
                                        "Customers":message
                                    }
                                    print("saved successfully")
                                else:
                                    print("else condition")
                                    message=res_cus['message']
                                    status="FAILED"
                                    # ErrorFileJson[x['InvoiceNumber']]['Customers']=message
                                    ErrorFileJson[x['InvoiceNumber']]={
                                        "Customers":message
                                    }
                                # syncing of customers ends and syncing of invoices starts here 
                                inv_pay_url=acc_txn_url
                                headers={
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }
                                add_item=inv_add_item
                                r_inv=requests.post(inv_pay_url, headers=headers ,json=add_item)
                                res_inv=r_inv.json()
                                print(res_inv)
                                print("invoice accounting response")
                                print(add_item)

                                # syncing of payments starts here
                                if "Payments" in x:
                                    payment_array=[]
                                    payment_amount=0
                                    for n in x['Payments']:
                                        print("kalash in payment")
                                        Acc_pay_code=n['Account']['Code']
                                        for row in ledger_settings:
                                            Acc_pay_code=n['Account']['Code']
                                            acc_code=row['ledgerCode']
                                            if acc_code == Acc_pay_code:
                                                Acc_pay_code=row['Acc_Code']
                                                break
                                            else:
                                                Acc_pay_code="Not Found"
                                        # if Acc_pay_code == n['Account']['Code']:
                                        #     Acc_pay_code="Not Found"
                                        payment_amount+=round(float(n['Amount']),2)
                                        inputdate=n['Date']

                                        if "PaymentCode" in n:
                                            pay_code=n['PaymentCode']
                                            auto_series=False
                                        else:
                                            auto_series=True
                                            pay_code=""

                                        dataarr=inputdate.split("-")
                                        newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                        print(newdate) 
                                        obj={}
                                        obj={
                                                "relatedTxnNumber": n['Invoice']['InvoiceNumber'],
                                                "txnType": txntype,
                                                "amount": n['Amount'],
                                                "date": newdate,
                                                "autoSeries":auto_series,
                                                "relatedTxnDate":newdate,
                                                "accountCode":Acc_pay_code,
                                                "accountName": "", 
                                                "reference": n['description'],
                                                "number": pay_code
                                            }
                                        payment_array.append(obj)
                                        
                                    noMatchCode_pay=0
                                    for p in payment_array:
                                        print("kalash in loop")
                                        if p['accountCode'] == "Not Found":
                                            noMatchCode_pay+=1
                                    if noMatchCode_pay == 0:
                                        pay_add_item={
                                            "txnPaymentReceiptList": payment_array
                                        }
                                        r_pay=requests.post(inv_pay_url, headers=headers, json=pay_add_item)
                                        res_pay=r_pay.json()
                                        print(res_pay)
                                        print("payment accounting response ")
                                        print(pay_add_item)
                                        if res_pay['message'] == "Batch Data Added successfully":
                                            print("if condition")
                                            message=res_pay['message']
                                            status="SUCCESS"
                                            ErrorFileJson[x['InvoiceNumber']]['Payments']=message
                                        elif res_pay['message'] == "Some Data is not valid and other batch data added successfully":
                                            print("elif condition")
                                            if res_pay['fieldErrors'] != None:
                                                fielderror=res_pay['fieldErrors']
                                                message=""
                                                for l in fielderror:
                                                    message+=l['message']
                                            else:
                                                message=res_pay['errorList']
                                            status="FAILED"
                                            ErrorFileJson[x['InvoiceNumber']]['Payments']=message
                                            print("saved successfully")
                                        else:
                                            print("else condition")
                                            message=res_pay['message']
                                            status="FAILED"
                                            ErrorFileJson[x['InvoiceNumber']]['Payments']=message
                                    else:
                                        message="Account Code did not match please add in your Ledger settings"
                                        ErrorFileJson[x['InvoiceNumber']]['Payments']=message
                                # save data into records after all sync 
                                if res_inv['message'] == "Batch Data Added successfully":
                                    print("if condition")
                                    # message=""
                                    success_invs+=1
                                    status="SUCCESS"
                                    invoicenumber=x['InvoiceNumber']
                                    invoice_code=x['InvoiceCode']
                                    cus_name=final_con_name
                                    amount=0
                                    for dict in linearray:
                                        amount+=round(float(dict['unitPrice']),2)
                                    resultant_amount=str(abs(amount))
                                    ErrorFileJson[invoicenumber]['Invoices']=res_inv['message']
                                    a=invoicerecord(Number=invoicenumber,Date=newdate,Customer_Name=cus_name,Invoice_Amount=resultant_amount,Remark=ErrorFileJson,Status=status,companyid=compid,Requested_json=inv_add_item,Response_json=x,branchid=branchid,invoicecode=invoice_code)
                                    a.save(using="hotel")
                                elif res_inv['message'] == "Some Data is not valid and other batch data added successfully":
                                    print("elif condition")
                                    if res_inv['fieldErrors'] != None:
                                        fielderror=res_inv['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message=l['message']
                                    else:
                                        message=res_inv['errorList'].values()
                                    failed_invs+=1
                                    status="FAILED"
                                    invoice_code=x['InvoiceCode']
                                    invoicenumber=x['InvoiceNumber']
                                    cus_name=final_con_name
                                    amount=0
                                    for dict in linearray:
                                        amount+=round(float(dict['unitPrice']),2)
                                    resultant_amount=str(abs(amount))
                                    ErrorFileJson[invoicenumber]['Invoices']=message
                                    a=invoicerecordfailed(Number=invoicenumber,Date=newdate,Customer_Name=cus_name,Invoice_Amount=resultant_amount,Remark=ErrorFileJson,Status=status,companyid=compid,invoicecode=invoice_code,Requested_json=inv_add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                                    print("saved successfully")
                                else:
                                    print("else condition")
                                    message=res_inv['message']
                                    failed_invs+=1
                                    status="FAILED"
                                    inv_status="FAILED"
                                    invoicenumber=x['InvoiceNumber']
                                    invoice_code=x['InvoiceCode']
                                    cus_name=final_con_name
                                    amount=0
                                    for dict in linearray:
                                        amount+=round(float(dict['unitPrice']),2)
                                    resultant_amount=str(abs(amount))
                                    ErrorFileJson[invoicenumber]['Invoices']=message
                                    a=invoicerecordfailed(Number=invoicenumber,Date=newdate,Customer_Name=cus_name,Invoice_Amount=resultant_amount,Remark=ErrorFileJson,Status=status,companyid=compid,invoicecode=invoice_code,Requested_json=inv_add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                            else:
                                    print("kalash is in else cond")
                                    message="Account Code did not match please add in your Ledger settings"
                                    status="FAILED"
                                    failed_invs+=1
                                    invoice_code=x['InvoiceCode']
                                    invoicenumber=x['InvoiceNumber']
                                    cus_name=final_con_name
                                    amount=0
                                    if len(linearray) != 0:
                                        for dict in linearray:
                                            amount+=round(float(dict['unitPrice']),2)
                                        resultant_amount=str(abs(amount))
                                    else:
                                        resultant_amount="Null"
                                    ErrorFileJson[invoicenumber]=message
                                    print("kalash before save ")
                                    a=invoicerecordfailed(Number=invoicenumber,Date=newdate,Customer_Name=cus_name,Invoice_Amount=resultant_amount,Remark=ErrorFileJson,Status=status,companyid=compid,invoicecode=invoice_code,Requested_json=inv_add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                                    print("kalash after save")
                        except Exception as e:
                            print("error is --------",e)
                            import traceback; traceback.print_exc();
                            message=f"{e} is missing in Hotelogix JSON"
                            status="FAILED"
                            failed_invs+=1
                            inv_status="FAILED"
                            invoicenumber=x['InvoiceNumber']
                            invoice_code=x['InvoiceCode']
                            cus_name=final_con_name
                            dataarr=inputdate.split("-")
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            amount=0
                            if len(linearray) != 0:
                                for dict in linearray:
                                    amount+=round(float(dict['unitPrice']),2)
                                resultant_amount=str(abs(amount))
                            else:
                                resultant_amount="Null"
                            inv_add_item={"Error":f"Please review your Hotelogix JSON for this  {invoicenumber} Invoice Number",
                            "TagName":str(e)
                            }
                            ErrorFileJson[invoicenumber]=message
                            a=invoicerecordfailed(Number=invoicenumber,Date=newdate,Customer_Name=cus_name,Invoice_Amount=resultant_amount,Remark=ErrorFileJson,Status=status,companyid=compid,invoicecode=invoice_code,Requested_json=inv_add_item,Response_json=x,branchid=branchid)
                            a.save(using="hotel")
                # save data for invoice records finally
                
            return Response({
                "message":"SYNC CUSTOMERS & INVOICES SUCCESSFULLY",
                "Total_Invoices":total_invs,
                "Success_Invoices":success_invs,
                "Failed_Invoices":failed_invs
            })

        except Exception as e:
            return Response({
                            "message":"SYNC CUSTOMERS & INVOICES FAILED"
                        })
            # return Response('SYNC CUSTOMERS & INVOICES FAILED')

    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=invoicerecord.objects.using("hotel").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed !!!")

# API for sync Commission
@api_view(['GET', 'POST'])
def syncCommission(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=commrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Amount","Remark","Status","companyid","branchid","invoicecode").order_by('-id')
            return Response(data)
        except:
            return Response("syncCommission get request in except")


    if request.method == "POST":
        try:
            # Accounting login starts 
            compid,preserve=request.data['compid'],request.data['preservekey']
            login=Accounting.Accounting_login(preserve,compid)
            compid,preserve,valuetoken=login['compid'],login['preservekey'],login['token']
            # Accounting Login ends
            hotelid=request.data['hotelid']
            token=request.data['token']
            gstin=request.data['gstin']
            branch=request.data['branch']
            state=request.data['state']
            saveas=request.data['saveas']
            city=request.data['city']
            zip=request.data['zip']
            address1=request.data['address1']
            ledger_settings=request.data['ledger_settings']
            fromdate=request.data['fromdate']
            todate=request.data['todate']
            branchid=request.data['branch_id']
            print("Start Date ----->",fromdate)
            print("End Date ----->",todate)
            for page in range(1,1000):
                hlurl=hotelogix_url+"v/accountingledger/ledgers/actype/tpa/dtype/comm"
                headers={
                    "RQ-HOTELID":hotelid,
                    "RQ-AUTH-TOKEN":token
                }
                payload={
                    "fromDate": fromdate,
                    "toDate": todate
                }
                r=requests.post(hlurl, headers=headers ,json=payload)
                res=r.json()
                print(res)
                print("json response")
                if "Invoices" not in res:
                    print("data over")
                    if page > 1:
                        return Response("SYNC COMMISSION SUCCESSFULLY")
                    else:
                        return Response("No Records Found !!!")
                else:
                    for x in res['Invoices']:
                        try:
                            inv_code=x['InvoiceCode']
                            print("before updatation")
                            update_comm_status(inv_code,hotelid,token)
                            print("after updatation")
                            inputdate=x['Date']
                            if "CompanyName" in x:
                                con_name=x['CompanyName']
                            else:
                                con_name=x['Contact']['Name']
                            dataarr=inputdate.split("-")
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            print(newdate)
                            inputduedate=x['DueDate']
                            dataarr=inputduedate.split("-")
                            newduedate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            print(newduedate)
                            # loop for line items
                            linearr=[]
                            for y in x['LineItems']:
                                if y['hsncode'] == "null":
                                    hsn=""
                                else:
                                    hsn=y['hsncode']
                                obj={}
                                if "TaxRate" in y:
                                    gst=y['TaxRate']
                                else:
                                    gst=0
                                accode=y['AccountCode']
                                for row in ledger_settings:
                                    accode=y['AccountCode']
                                    acc_code=row['ledgerCode']
                                    if acc_code == accode:
                                        accode=row['Acc_Code']
                                        break
                                    else:
                                        accode="Not Found"
                                # if accode == y['AccountCode']:
                                #     accode="Not Found"
                                if y['Description'] != None:
                                    desci=y['Description']
                                else:
                                    desci="Commission"
                                obj={
                                            "saleType":"Normal",
                                            "quantity":y['Quantity'],
                                            "unitPrice":y['UnitAmount'],
                                            "amount":0,
                                            "freightUnit":0,
                                            "discount":0,
                                            # "inventoryType":"INVTP",
                                            # "itemCode":"ACC-27",
                                            # "itemName":"BLACK",
                                            "description":desci,
                                            # "gstRate":gst,
                                            "billOfSupplyGst":"Non-GST",
                                            "hsnSac":hsn,
                                            "type":"Goods",
                                            "unitName":"PCS",
                                            # "itcClaim":100,
                                            # "itcEligibility":"INGD",
                                            "accountCode":accode
                                    }
                                linearr.append(obj)
                            if "Addresses" not in x:
                                # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                # else:
                                #     contactph=None
                                if (x['Contact']['CompanyGstin'] == "null") or (x['Contact']['CompanyGstin'] == ""):
                                    contactgstin=None
                                    cus_add_item={
                                    "contactList": [
                                        {
                                            "name": con_name,
                                            "accountNumber": x['Contact']['ContactNumber'],
                                            "employee": False,
                                            "vendor": True,
                                            "customer": False,
                                            "primaryType": "vendor",
                                            "contactPerson": [
                                                {
                                                    # "emailAddress": contactemail,
                                                    "firstName": x['Contact']['FirstName'],
                                                    #"lastName": x['Contact']['LastName'],
                                                    "primeFlag": 1
                                                }
                                            ],
                                        # "mobile": contactph,
                                        "status": "COAC",
                                        }
                                    ]
                                }
                                else:
                                    contactgstin=x['Contact']['CompanyGstin']
                                    cus_add_item={
                                        "contactList": [
                                            {
                                                "name": con_name,
                                                "accountNumber": x['Contact']['ContactNumber'],
                                                "employee": False,
                                                "vendor": True,
                                                "customer": False,
                                                "primaryType": "vendor",
                                                "contactPerson": [
                                                    {
                                                        # "emailAddress": contactemail,
                                                        "firstName": x['Contact']['FirstName'],
                                                        #"lastName": x['Contact']['LastName'],
                                                        "primeFlag": 1
                                                    }
                                                ],
                                            # "mobile": contactph,
                                                "contactGstin":[{
                                                "number": contactgstin,
                                                "verified": False,
                                                "billingAddress": {
                                                    "addressGSTIN": contactgstin,
                                                    "address1": address1,
                                                    "city": city,
                                                    "state": state,
                                                    "zip": zip,
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "BADR"
                                                },
                                                "shippingAddress": {
                                                    "addressGSTIN": contactgstin,
                                                    "address1": address1,
                                                    "city": city,
                                                    "state": state,
                                                    "zip": zip,
                                                    "country": "INDIA",
                                                    # "mobile": contactph,
                                                    "pan": None,
                                                    "tan": None,
                                                    "gstin": None,
                                                    "cin": None,
                                                    # "telephone": contactph,
                                                    "type": "SADR"
                                                },
                                                "defaultGstin": True
                                            }],
                                            "status": "COAC",
                                            }
                                        ]
                                    }
                            if (x['Contact']['CompanyGstin'] == "") or (x['Contact']['CompanyGstin'] == "null"):
                                print("kalash in elif condition")
                                # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                # else:
                                #     contactph=None
                                cus_add_item={
                                    "contactList": [
                                        {
                                            "name": con_name,
                                            "accountNumber": x['Contact']['ContactNumber'],
                                            "employee": False,
                                            "vendor": True,
                                            "customer": False,
                                            "primaryType": "vendor",
                                            "contactPerson": [
                                                {
                                                    # "emailAddress": contactemail,
                                                    "firstName": x['Contact']['FirstName'],
                                                    # "lastName": x['Contact']['LastName'],
                                                    "primeFlag": 1
                                                }
                                            ],
                                        # "mobile": contactph,
                                            "address": [
                                            {
                                                "addressGSTIN": None,
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city": x['Contact']['Addresses']['Address']['City'],
                                                "state": None,
                                                "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                # "mobile": contactph,
                                                # "telephone": contactph,
                                                "type": "PADR"
                                            }
                                        ],
                                        "status": "COAC",
                                        }
                                    ]
                                }
                            
                            else:
                                # if (x['Contact']['Phones']['Phone']['PhoneType'] == "MOBILE") or (x['Contact']['Phones']['Phone']['PhoneType'] == "DEFAULT"):
                                #     contactph=x['Contact']['Phones']['Phone']['PhoneNumber']
                                # else:
                                #     contactph=None
                                cus_add_item={
                                    "contactList": [
                                        {
                                            "name": con_name,
                                            "accountNumber": x['Contact']['ContactNumber'],
                                            "employee": False,
                                            "vendor": True,
                                            "customer": False,
                                            "primaryType": "vendor",
                                            "contactPerson": [
                                                {
                                                    # "emailAddress": contactemail,
                                                    "firstName": x['Contact']['FirstName'],
                                                    # "lastName": x['Contact']['LastName'],
                                                    "primeFlag": 1
                                                }
                                            ],
                                        # "mobile": contactph,
                                        "address": [
                                            {
                                                "addressGSTIN": x['Contact']['CompanyGstin'],
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city": x['Contact']['Addresses']['Address']['City'],
                                                "state": state,
                                                "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                # "mobile": contactph,
                                                # "telephone": contactph,
                                                "type": "PADR"
                                            }
                                        ],
                                            "contactGstin":[{
                                            "number": x['Contact']['CompanyGstin'],
                                            "verified": False,
                                            "billingAddress": {
                                                "addressGSTIN": x['Contact']['CompanyGstin'],
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city": x['Contact']['Addresses']['Address']['City'],
                                                "state": state,
                                                "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                # "mobile": contactph,
                                                "pan": None,
                                                "tan": None,
                                                "gstin": None,
                                                "cin": None,
                                                # "telephone": contactph,
                                                "type": "BADR"
                                            },
                                            "shippingAddress": {
                                                "addressGSTIN": x['Contact']['CompanyGstin'],
                                                "address1": x['Contact']['Addresses']['Address']['AddressLine1'],
                                                "city": x['Contact']['Addresses']['Address']['City'],
                                                "state": state,
                                                "zip": x['Contact']['Addresses']['Address']['PostalCode'],
                                                "country": "INDIA",
                                                # "mobile": contactph,
                                                "pan": None,
                                                "tan": None,
                                                "gstin": None,
                                                "cin": None,
                                                # "telephone": contactph,
                                                "type": "SADR"
                                            },
                                            "defaultGstin": True
                                        }],
                                        "status": "COAC",
                                        }
                                    ]
                                }
                            noMatchCode=0
                            for j in linearr:
                                print("kalash in loop")
                                if j['accountCode'] == "Not Found":
                                    noMatchCode+=1
                            if noMatchCode == 0:
                                customerurl=acc_mas_url
                                headers={
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }
                                add_item=cus_add_item
                                r=requests.post(customerurl, headers=headers,json=add_item)
                                res=r.json()
                                print(res)
                                print("customers accounting response")
                                # syncing of commission starts here 
                                if x['Contact']['CompanyName'] == "":
                                    comapnyname=x['Contact']['Name']
                                else:
                                    comapnyname=x['Contact']['CompanyName']
                                add_item={
                                        "billList":[
                                            {
                                                "taxType":"ETAX",
                                                "typeCode":"PBILL",
                                                "currencyCode":"INR",
                                                "companyGstin":gstin,
                                                "category":"",
                                                "branch":branch,
                                                "billType":"R",
                                                "date":newdate,
                                                "billDate":newdate,
                                                "custBillDate":"",
                                                "dueDate":newduedate,
                                                "contactCode":x['Contact']['ContactNumber'],
                                                "contactName":comapnyname, 
                                                "customerGstin":x['Contact']['CompanyGstin'],
                                                # "placeSupplyName":x['Contact']['PlaceOfSupply'],
                                                "placeSupplyName":state,
                                                "shipAddress":{
                                                    "address1":x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city":x['Contact']['Addresses']['Address']['City'],
                                                    "state":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country":"INDIA",
                                                    "pan":"",
                                                    "gstin":x['Contact']['CompanyGstin'],
                                                    "type":"BADR"
                                                },
                                                "vendorAddress":{
                                                "address1":x['Contact']['Addresses']['Address']['AddressLine1'],
                                                    "city":x['Contact']['Addresses']['Address']['City'],
                                                    "state":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "zip":x['Contact']['Addresses']['Address']['PostalCode'],
                                                    "country":"INDIA",
                                                    "pan":"",
                                                    "gstin":x['Contact']['CompanyGstin'],
                                                    "type":"SADR"
                                                },
                                                
                                                "itcClaimCheckFlag":True,
                                                "amount":0,
                                                "roundingAmount":0,
                                                "number":x['InvoiceNumber'],
                                                "custBillNumber":"",  
                                                "lineItems":linearr,
                                                "status":"BAPP",
                                                "gstnType":"B2B"
                                            }
                                        ]
                                        }
                                commissionurl = acc_txn_url

                                headers = {
                                        "x-auth-token": valuetoken,
                                        "x-preserveKey":  preserve,
                                        "x-company":  compid,
                                        "Content-Type": "application/json"
                                }

                                response = requests.post( commissionurl, headers=headers ,json=add_item)
                                res=response.json()
                                print(res)
                                print("Commission accounting response")
                                print(add_item)
                                if res['message'] == "Batch Data Added successfully":
                                        print("if condition")
                                        message=res['message']
                                        status="SUCCESS"
                                        invoicenumber=x['InvoiceNumber']
                                        inv_code=x['InvoiceCode']
                                        amount=0
                                        for dict in linearr:
                                            amount+=round(float(dict['unitPrice']),2)
                                        resultant_amount=str(amount)
                                        a=commrecord(Number=invoicenumber,Date=newdate,Amount=resultant_amount,Remark=message,Status=status,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid,invoicecode=inv_code)
                                        a.save(using="hotel")
                                elif res['message'] == "Some Data is not valid and other batch data added successfully":
                                    print("elif condition")
                                    if res['fieldErrors'] != None:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
                                    else:
                                        message=str(res['errorList'].values())
                                    status="FAILED"
                                    invoicenumber=x['InvoiceNumber']
                                    inv_code=x['InvoiceCode']
                                    amount=0
                                    for dict in linearr:
                                        amount+=round(float(dict['unitPrice']),2)
                                    resultant_amount=str(amount)
                                    a=commfailedrecord(Number=invoicenumber,Date=newdate,Amount=resultant_amount,Remark=message,Status=status,invoicecode=inv_code,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                                else:
                                    print("else condition")
                                    message+=res['message']
                                    status="FAILED"
                                    invoicenumber=x['InvoiceNumber']
                                    inv_code=x['InvoiceCode']
                                    amount=0
                                    for dict in linearr:
                                        amount+=round(float(dict['unitPrice']),2)
                                    resultant_amount=str(amount)
                                    a=commfailedrecord(Number=invoicenumber,Date=newdate,Amount=resultant_amount,Remark=message,Status=status,invoicecode=inv_code,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                                # syncing of payments starts here
                                if "Payments" in x:
                                    payment_array=[]
                                    payment_amount=0
                                    for n in x['Payments']:
                                        print("kalash in payment")
                                        Acc_pay_code=n['Account']['Code']
                                        for row in ledger_settings:
                                            Acc_pay_code=n['Account']['Code']
                                            acc_code=row['ledgerCode']
                                            if acc_code == Acc_pay_code:
                                                Acc_pay_code=row['Acc_Code']
                                                break
                                            else:
                                                Acc_pay_code="Not Found"
                                        # if Acc_pay_code == n['Account']['Code']:
                                        #     Acc_pay_code="Not Found"
                                        payment_amount+=round(float(n['Amount']),2)
                                        inputdate=n['Date']
                                        pay_code=n['PaymentCode']
                                        dataarr=inputdate.split("-")
                                        newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                                        print(newdate) 
                                        if n['description'] != None:
                                            desc_pay=n['description']
                                        else:
                                            desc_pay="Commission"
                                        obj={}
                                        obj={
                                                "relatedTxnNumber": n['Invoice']['InvoiceNumber'],
                                                "txnType": "BILL",
                                                "amount": n['Amount'],
                                                "date": newdate,
                                                "autoSeries":True,
                                                "relatedTxnDate":newdate,
                                                "accountCode":Acc_pay_code,
                                                "accountName": "", 
                                                "reference": desc_pay
                                            }
                                        payment_array.append(obj)
                                    noMatchCode_pay=0
                                    for p in payment_array:
                                        print("kalash in loop")
                                        if p['accountCode'] == "Not Found":
                                            noMatchCode_pay+=1
                                    if noMatchCode_pay == 0:
                                        pay_add_item={
                                            "txnPaymentReceiptList": payment_array
                                        }
                                        r_pay=requests.post(commissionurl, headers=headers, json=pay_add_item)
                                        res_pay=r_pay.json()
                                        print(res_pay)
                                        print("payment accounting response ")
                                        print(pay_add_item)
                                    else:
                                        pass
                            else:
                                message="Account code did not match so please add in your Ledger settings"
                                status="FAILED"
                                invoicenumber=x['InvoiceNumber']
                                inv_code=x['InvoiceCode']
                                amount=0
                                for dict in linearr:
                                    amount+=round(float(dict['unitPrice']),2)
                                resultant_amount=str(amount)
                                a=commfailedrecord(Number=invoicenumber,Date=newdate,Amount=resultant_amount,Remark=message,Status=status,invoicecode=inv_code,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                a.save(using="hotel")
                        except Exception as e:
                            print("error is -------",e)
                            inputdate=x['Date']
                            dataarr=inputdate.split("-")
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            message=f"{e} is missing in Hotelogix JSON"
                            status="FAILED"
                            invoicenumber=x['InvoiceNumber']
                            inv_code=x['InvoiceCode']
                            amount=0
                            if len(linearr) != 0:
                                for dict in linearr:
                                    amount+=round(float(dict['unitPrice']),2)
                                resultant_amount=str(amount)
                            else:
                                resultant_amount="None"
                            add_item={"Error":f"Please review your Hotelogix JSON for this  {invoicenumber} Invoice Number",
                            "TagName":str(e)
                            }
                            a=commfailedrecord(Number=invoicenumber,Date=newdate,Amount=resultant_amount,Remark=message,Status=status,invoicecode=inv_code,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                            a.save(using="hotel")
            return Response("SYNC COMMISSION SUCCESSFULLY")

        except:
            return Response("SYNC COMMISSION FAILED !!!!")


# API for sync remaining payments 
@api_view(['GET', 'POST'])
def syncPayment(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=paymentrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Amount","Remark","Status","companyid","branchid","paymentcode").order_by('-id')
            return Response(data)
        except:
            return Response("syncPayment get request in except")


    if request.method == "POST":
        try:
            # Accounting login starts 
            compid,preserve=request.data['compid'],request.data['preservekey']
            login=Accounting.Accounting_login(preserve,compid)
            compid,preserve,valuetoken=login['compid'],login['preservekey'],login['token']
            # Accounting Login ends
            hotelid=request.data['hotelid']
            token=request.data['token']
            ledger_settings=request.data['ledger_settings']
            fromdate=request.data['fromdate']
            todate=request.data['todate']
            branchid=request.data['branch_id']
            print("Start Date ----->",fromdate)
            print("End Date ----->",todate)
            for page in range(1,1000):
                hlurl=hotelogix_url+"v/accountingledger/ledgers/actype/tpa/dtype/payments"
                headers={
                    "RQ-HOTELID":hotelid,
                    "RQ-AUTH-TOKEN":token,
                    "RQ-PAGE":"1"
                }
                payload={
                    "fromDate": fromdate,
                    "toDate": todate
                }
                r=requests.post(hlurl, headers=headers ,json=payload)
                res=r.json()
                print(res)
                print("json response")
                if "Payments" not in res:
                    print("data over")
                    if page > 1:
                        return Response("SYNC REMAINING PAYMENTS SUCCESSFULLY")
                    else:
                        return Response("No Records Found !!!")
                else:
                    for x in res['Payments']:
                        try:
                            paycode=x['PaymentCode']
                            print("before updatation")
                            update_pay_status(paycode,hotelid,token)
                            print("after updatation")
                            inputdate=x['Date']
                            dataarr=inputdate.split("-")
                            invoiceno=x['Invoice']['InvoiceNumber']
                            amount=x['Amount']
                            accountcode=x['Account']['Code']
                            for row in ledger_settings:
                                accountcode=x['Account']['Code']
                                acc_code=row['ledgerCode']
                                if acc_code == accountcode:
                                    accountcode=row['Acc_Code']
                                    break
                                else:
                                    accountcode="Not Found"
                            # if accountcode == x['Account']['Code']:
                            #     accountcode="Not Found"
                            if x['description'] != None:
                                desc=x['description']
                            else:
                                desc="Remaining Payment"
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            invoicetype=x['Invoice']['InvoiceType']
                            if invoicetype == "COMM":
                                txntype="BILL"
                            if invoicetype == "HOTEL":
                                txntype="INV"
                            add_item= {
                                            "txnPaymentReceiptList": [
                                    {
                                        "relatedTxnNumber": invoiceno,
                                        "autoSeries":True,
                                        "relatedTxnDate":newdate,
                                        "txnType": txntype,
                                        "amount":amount,
                                        "date": newdate,
                                        "accountCode": accountcode,
                                    
                                        "reference": desc
                                    }
                                ]
                            }
                            noMatchCode_pay=0
                            for p in add_item['txnPaymentReceiptList']:
                                print("kalash in loop")
                                if p['accountCode'] == "Not Found":
                                    noMatchCode_pay+=1
                            if noMatchCode_pay == 0:
                                paymenturl = acc_txn_url

                                headers = {
                                        "x-auth-token": valuetoken,
                                        "x-preserveKey":  preserve,
                                        "x-company":  compid,
                                        "Content-Type": "application/json"
                                }

                                response = requests.post( paymenturl, headers=headers ,json=add_item)
                                res=response.json()
                                print(res)
                                print("Remaining payments accounting response")
                                print(add_item)
                                if res['message'] == "Batch Data Added successfully":
                                    print("if condition")
                                    a=paymentrecord(Number=invoiceno,Date=newdate,Amount=amount,Remark=res['message'],Status="SUCCESS",companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid,                       paymentcode=paycode)
                                    a.save(using="hotel")
                                elif res['message'] == "Some Data is not valid and other batch data added successfully":
                                    print("elif condition")
                                    if res['fieldErrors'] != None:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for x in fielderror:
                                            message+=x['message']
                                    else:
                                        message=res['errorList'].values()
                                    a=paymentfailedrecord(Number=invoiceno,Date=newdate,Amount=amount,Remark=message,Status="FAILED",
                                    paymentcode=paycode,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                                else:
                                    print("else condition")
                                    a=paymentfailedrecord(Number=invoiceno,Date=newdate,Amount=amount,Remark=message,Status="FAILED",
                                    paymentcode=paycode,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                    a.save(using="hotel")
                            else:
                                message="Account code did not match so please add in your Ledger settings"
                                a=paymentfailedrecord(Number=invoiceno,Date=newdate,Amount=amount,Remark=message,Status="FAILED",
                                paymentcode=paycode,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                                a.save(using="hotel")
                        except Exception as e:
                            print("error is ----",e)
                            message=f"{e} is missing in Hotelogix JSON"
                            inputdate=x['Date']
                            dataarr=inputdate.split("-")
                            invoiceno=x['Invoice']['InvoiceNumber']
                            paycode=x['PaymentCode']
                            amount=x['Amount']
                            newdate=dataarr[2]+"-"+dataarr[1]+"-"+dataarr[0]
                            add_item={"Error":f"Please review your Hotelogix JSON for this  {invoiceno} Invoice Number",
                            "TagName":str(e)
                            }
                            a=paymentfailedrecord(Number=invoiceno,Date=newdate,Amount=amount,Remark=message,Status="FAILED",paymentcode=paycode,companyid=compid,Requested_json=add_item,Response_json=x,branchid=branchid)
                            a.save(using="hotel")

            return Response("SYNC REMAINING PAYMENTS SUCCESSFULLY")

        except:
            return Response("SYNC REMAINING PAYMENTS FAILED !!!")


# API for sending status for failed invoice 
@api_view(['GET', 'POST','DELETE'])
def failedinv(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=invoicerecordfailed.objects.usin("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Customer_Name","Invoice_Amount","invoicecode","Remark","Status","companyid","branchid").order_by('-id')
            return Response(data)
        except Exception as e:
            print("Except ------->",e)
            return Response("failedinv get request in except")


    if request.method == "POST":
        try:
            if request.data != []:
                for x in request.data:
                    try:
                        print("hotelid --->",x['hotelid'])
                        inv_code=x['invoicecode']
                        tab=x['tab']
                        hotelid=x['hotelid']
                        password=x['password']
                        user=x['username']
                        url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/hotel"
                        headers={
                                    "RQ-HOTELID":hotelid,
                                    "RQ-AUTH-TOKEN":user+":"+password
                                }
                        payload={
                                "Invoices": {
                                    inv_code:"UNSYNC"
                                },
                                "Payments": {}
                        }
                        r=requests.post(url, headers=headers , json=payload)
                        res=r.json()
                        print(res)
                        if "ErrorMessage" not in res:
                            if tab == "Success":
                                a=invoicerecord.objects.using("hotel").filter(invoicecode=inv_code)
                                a.delete()
                            else:
                                a=invoicerecordfailed.objects.using("hotel").filter(invoicecode=inv_code)
                                a.delete()
                            print("delete successfully")
                        else:
                            print(res['ErrorMessage'])

                    except Exception as e:
                        print(e)
                        print("Invoice before Unsync Functionality")
            else:
                return Response("Please select Invoice for Unsync request")

            return Response("Unsync request successful")

        except:
            return Response("something went wrong")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=invoicerecordfailed.objects.using("hotel").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed !!!")


# API for sending status for failed deposit
@api_view(['GET', 'POST','DELETE'])
def faileddep(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=depositfailedrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Narration","Credit_Amount","Debit_Amount","depcode","Remark","Status","companyid","branchid").order_by('-id')
            return Response(data)

        except:
            return Response("faileddep get request in except")


    if request.method == "POST":
        try:
            print("Request data --------->",request.data)
            if request.data != []:	
                for x in request.data:
                    try:
                        dep_code=x['depcode']
                        tab=x['tab']
                        hotelid=x['hotelid']
                        password=x['password']
                        user=x['username']
                        url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/dep"
                        headers={
                                    "RQ-HOTELID":hotelid,
                                    "RQ-AUTH-TOKEN":user+":"+password
                                }
                        payload={
                                "Invoices": {
                                    dep_code:"UNSYNC"
                                },
                                "Payments": {}
                        }
                        r=requests.post(url, headers=headers , json=payload)
                        res=r.json()
                        print(res)
                        if "ErrorMessage" not in res:
                            if tab == "Success":
                                a=depositrecord.objects.using("hotel").filter(depcode=dep_code)
                                a.delete()
                            else:
                                a=depositfailedrecord.objects.using("hotel").filter(depcode=dep_code)
                                a.delete()
                            print("delete successfully")
                        else:
                            print(res['ErrorMessage'])

                    except Exception as e:
                        print(e)
                        print("Deposit before Unsync Funtionality ")
            else:
                return Response("Please select Deposit for Unsync request")

            return Response("Unsync request successful")

        except:
            return Response("something went wrong")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=depositfailedrecord.objects.using("hotel").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed !!!")



# API for sending status for failed remaining payments
@api_view(['GET', 'POST'])
def failedpay(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=paymentfailedrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("id","Number","Date","Amount","Remark","Status","paymentcode","companyid","branchid").order_by('-id')
            return Response(data)

        except:
            return Response("failedpay get request in except")


    if request.method == "POST":
        try:
            if request.data != []:
                for x in request.data:
                    try:
                        pay_code=x['paymentcode']
                        hotelid=x['hotelid']
                        password=x['password']
                        user=x['username']
                        tab=x['tab']
                        url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/payments"
                        headers={
                                    "RQ-HOTELID":hotelid,
                                    "RQ-AUTH-TOKEN":user+":"+password
                                }
                        payload={
                                "Invoices": {},
                                "Payments": {
                                    pay_code:"UNSYNC"
                                }
                        }
                        r=requests.post(url, headers=headers , json=payload)
                        res=r.json()
                        print(res)
                        if "ErrorMessage" not in res:
                            if tab == "Success":
                                a=paymentrecord.objects.using("hotel").filter(paymentcode=pay_code)
                                a.delete()
                            else:
                                a=paymentfailedrecord.objects.using("hotel").filter(paymentcode=pay_code)
                                a.delete()
                            print("delete successfully")
                        else:
                            print(res['ErrorMessage'])

                    except Exception as e:
                        print(e)
                        print("Payment before Unsync Functionality")
            else:
                return Response("Please select Payment for Unsync request")

            return Response("Unsync request successful")

        except:
            return Response("something went wrong")


# API for sending status for failed commissions
@api_view(['GET', 'POST'])
def failedcomm(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branchid=request.GET.get('branchid')
            data=commfailedrecord.objects.using("hotel").filter(companyid=compid,branchid=branchid).values("Number","Date","Amount","Remark","Status","invoicecode","companyid","branchid").order_by('-id')
            return Response(data)

        except:
            return Response("failedcomm get request in except")


    if request.method == "POST":
        try:
            if request.data != []:
                for x in request.data:
                    try:
                        inv_code=x['invoicecode']
                        hotelid=x['hotelid']
                        password=x['password']
                        user=x['username']
                        tab=x['tab']
                        url=hotelogix_url+"v/accountingledger/notifystatus/actype/tpa/dtype/comm"
                        headers={
                                    "RQ-HOTELID":hotelid,
                                    "RQ-AUTH-TOKEN":user+":"+password
                                }
                        payload={
                                "Invoices": {
                                    inv_code:"UNSYNC"
                                },
                                "Payments": {}
                        }
                        r=requests.post(url, headers=headers , json=payload)
                        res=r.json()
                        print(res)
                        if "ErrorMessage" not in res:
                            if tab == "Success":
                                a=commrecord.objects.using("hotel").filter(invoicecode=inv_code)
                                a.delete()
                            else:
                                a=commfailedrecord.objects.using("hotel").filter(invoicecode=inv_code)
                                a.delete()
                            print("delete successfully")
                        else:
                            print(res['ErrorMessage'])
                            
                    except Exception as e:
                        print(e)
                        print("Commission before Unsync Functionality")
            else:
                return Response("Please select Commission for Unsync request")

            return Response("Unsync request successful")

        except:
            return Response("something went wrong")


# ---------------- AccountCode Search ----------------------
@api_view(['GET', 'POST'])
def search_acc_code(request, **kwargs):
    if request.method == "POST":
        try:
            print("\n this is seach value------------------",request.data['value'])
            acode=[]
            header3={
                    "x-preserveKey": preserve,
                    "x-company": compid,
                    "Content-Type": "application/json",
                    'x-auth-token':valuetoken
            }
            body2={    
                    "entityType":"ACCT",
                    "searchFor":request.data['value'],
                    "page":1,
                    "limit":500
                }
            acresponse = requests.post(branch, headers=header3, json=body2)
            acode=acresponse.json()

            print("\n this is total acc code -----------",len(acode))
            return Response({"accountcode":acode['data']['master']['list']})
            
        except Exception as e:
            print("\nin exception ---------",e)
            return Response("Error")

# ------------------- AccountCode Search -------------------

# ----------- Get Json API --------------------

@api_view(['GET', 'POST'])
def getjsonrecord(request, **kwargs):
    if request.method == "GET":
        id=request.GET.get('id')
        print(id)
        jsontype=request.GET.get('jsontype')
        print(jsontype)
        tabletype=request.GET.get('tabletype')
        print(tabletype)
        synctype=request.GET.get('synctype')
        print(tabletype)

        if synctype == "invoice":
            if "success"==tabletype:
                data=invoicerecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
            else:
                data=invoicerecordfailed.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
        
        if synctype == "deposit":
            if "success"==tabletype:
                data=depositrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
            else:
                data=depositfailedrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
        
        if synctype == "payment":
            if "success"==tabletype:
                data=paymentrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
            else:
                data=paymentfailedrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
        
        if synctype == "commission":
            if "success"==tabletype:
                data=commrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
            else:
                data=commfailedrecord.objects.using("hotel").filter(id=id).values(jsontype)
                return Response(data)
        
# ----------- Get Json API --------------------



# ------------ Searching -------------------------
@api_view(['GET', 'POST'])
def filtertable(request,*args ,**kwargs):
    if request.method=="POST":
        synctype=request.data["synctype"]
        print("Deposit------->",synctype)
        tabletype=request.data["tabletype"]
        print("synctype------->",tabletype)
        searchby=request.data["searchby"]
        print("searchby------->",searchby)
        compid=request.data["compid"]
        print("compid------->",compid)
        branch=request.data["branch"]
        print("branch------->",branch)

        # ----------- Deposit Filter ---------------------
        if synctype=="deposit":
            if tabletype=="success":
                if "number" in searchby and searchby["number"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositrecord.objects.using("hotel").filter(Q(Number__icontains=searchby["number"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "credit" in searchby and searchby["credit"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositrecord.objects.using("hotel").filter(Q(Credit_Amount__icontains=searchby["credit"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "debit" in searchby and searchby["debit"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositrecord.objects.using("hotel").filter(Q(Credit_Amount__icontains=searchby["debit"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "startdate" in searchby and searchby["startdate"]!="":
                    stdate = searchby['startdate'].split("T")[0].split('-')
                    endate = searchby['enddate'].split("T")[0].split('-')
                    stdate1=datetime(int(stdate[0]),int(stdate[1]),int(stdate[2]))
                    endate1=datetime(int(endate[0]),int(endate[1]),int(endate[2]))
                    num_days=(endate1-stdate1).days
                    print(num_days)
                    data1=[]
                    for day in range(num_days+1):
                        curren_date = stdate1+ timedelta(days=day+1)
                        date=curren_date.strftime('%d-%m-%Y')
                        print("\n current--------------",date)
                        fields_to_exclude = ['Requested_json', 'Response_json']
                        all_fields = depositrecord._meta.fields
                        fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                        data=depositrecord.objects.using("hotel").filter(Q(Date__exact=date)).filter(companyid=compid,branchid=branch).defer('Requested_json','Response_json').values(*fields_to_include)
                        for da in data:
                            data1.append(da)
                    return Response(data1)
        
            else:
                if "number" in searchby and searchby["number"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositfailedrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositfailedrecord.objects.using("hotel").filter(Q(Number__icontains=searchby["number"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "credit" in searchby and searchby["credit"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositfailedrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositfailedrecord.objects.using("hotel").filter(Q(Credit_Amount__icontains=searchby["credit"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "debit" in searchby and searchby["debit"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = depositfailedrecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=depositfailedrecord.objects.using("hotel").filter(Q(Credit_Amount__icontains=searchby["debit"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "startdate" in searchby and searchby["startdate"]!="":
                    stdate = searchby['startdate'].split("T")[0].split('-')
                    endate = searchby['enddate'].split("T")[0].split('-')
                    stdate1=datetime(int(stdate[0]),int(stdate[1]),int(stdate[2]))
                    endate1=datetime(int(endate[0]),int(endate[1]),int(endate[2]))
                    num_days=(endate1-stdate1).days
                    print(num_days)
                    data1=[]
                    for day in range(num_days+1):
                        curren_date = stdate1+ timedelta(days=day+1)
                        date=curren_date.strftime('%d-%m-%Y')
                        print("\n current--------------",date)
                        fields_to_exclude = ['Requested_json', 'Response_json']
                        all_fields = depositfailedrecord._meta.fields
                        fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                        data=depositfailedrecord.objects.using("hotel").filter(Q(Date__exact=date)).defer('Requested_json','Response_json').filter(companyid=compid,branchid=branch).values(*fields_to_include)
                        for da in data:
                            data1.append(da)
                    return Response(data1)
                
        #  ---------------- Invoice Filter --------------------
        if synctype=="invoice":
            if tabletype=="success":
                if "number" in searchby and searchby["number"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecord.objects.fusing("hotel").filter(Q(Number__icontains=searchby["number"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "name" in searchby and searchby["name"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecord.objects.using("hotel").filter(Q(Customer_Name__icontains=searchby["name"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "amount" in searchby and searchby["amount"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecord._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecord.objects.using("hotel").filter(Q(Invoice_Amount__icontains=searchby["amount"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "startdate" in searchby and searchby["startdate"]!="":
                    stdate = searchby['startdate'].split("T")[0].split('-')
                    endate = searchby['enddate'].split("T")[0].split('-')
                    stdate1=datetime(int(stdate[0]),int(stdate[1]),int(stdate[2]))
                    endate1=datetime(int(endate[0]),int(endate[1]),int(endate[2]))
                    num_days=(endate1-stdate1).days
                    print(num_days)
                    data1=[]
                    for day in range(num_days+1):
                        curren_date = stdate1+ timedelta(days=day+1)
                        date=curren_date.strftime('%d-%m-%Y')
                        print("\n current--------------",date)
                        fields_to_exclude = ['Requested_json', 'Response_json']
                        all_fields = invoicerecord._meta.fields
                        fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                        data=invoicerecord.objects.using("hotel").filter(Q(Date__exact=date)).filter(companyid=compid,branchid=branch).defer('Requested_json','Response_json').values(*fields_to_include)
                        for da in data:
                            data1.append(da)
                    return Response(data1)

            else:
                if "number" in searchby and searchby["number"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecordfailed._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecordfailed.objects.using("hotel").filter(Q(Number__icontains=searchby["number"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "name" in searchby and searchby["name"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecordfailed._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecordfailed.objects.using("hotel").filter(Q(Customer_Name__icontains=searchby["name"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "amount" in searchby and searchby["amount"]!="":
                    fields_to_exclude = ['Requested_json', 'Response_json']
                    all_fields = invoicerecordfailed._meta.fields
                    fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                    data=invoicerecordfailed.objects.using("hotel").filter(Q(Invoice_Amount__icontains=searchby["amount"])).filter(companyid=compid,branchid=branch).values(*fields_to_include)
                    return Response(data)
                
                if "startdate" in searchby and searchby["startdate"]!="":
                    stdate = searchby['startdate'].split("T")[0].split('-')
                    endate = searchby['enddate'].split("T")[0].split('-')
                    stdate1=datetime(int(stdate[0]),int(stdate[1]),int(stdate[2]))
                    endate1=datetime(int(endate[0]),int(endate[1]),int(endate[2]))
                    num_days=(endate1-stdate1).days
                    print(num_days)
                    data1=[]
                    for day in range(num_days+1):
                        curren_date = stdate1+ timedelta(days=day+1)
                        date=curren_date.strftime('%d-%m-%Y')
                        print("\n current--------------",date)
                        fields_to_exclude = ['Requested_json', 'Response_json']
                        all_fields = invoicerecordfailed._meta.fields
                        fields_to_include = [field.name for field in all_fields if field.name not in fields_to_exclude]
                        data=invoicerecordfailed.objects.using("hotel").filter(Q(Date__exact=date)).filter(companyid=compid,branchid=branch).defer('Requested_json','Response_json').values(*fields_to_include)
                        for da in data:
                            data1.append(da)
                    return Response(data1)
                


# ------------ Searching -------------------------