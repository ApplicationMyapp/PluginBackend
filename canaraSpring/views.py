from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import userSettings, Sale_Invoice_records, Customer_records,Product_records,CreditNote_records,Receipt_records,CustomerSyncUpdate,InvoiceSyncUpdate,ProductSyncUpdate,CreditNoteSyncUpdate,Expenses_records,ExpenseSyncUpdate,ReceiptSyncUpdate,InventoryDateSyncUpdate
from . import Accounting
import traceback 
import requests
import json
import urllib
from datetime import datetime
import datetime as dt
from django.db.models import Q
from datetime import datetime, timedelta

# Accouting Urls
branch = "https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url = "https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url = "https://booksapi.hostbooks.in/hostbook/api/master/add"


# Canara Spring Urls
# # Live 
# userloginurl = "https://canarasprings-erp-staging.azurewebsites.net/api/User" 
# customerurl = "https://canarasprings-erp-staging.azurewebsites.net/api/Party/GetAllParties"
# product = "https://canarasprings-erp-staging.azurewebsites.net/api/Rate/GetAllProducts"
# invoice = "https://canarasprings-erp-staging.azurewebsites.net/api/Invoice/GetAllInvoices"
# creditNote = "https://canarasprings-erp-staging.azurewebsites.net/api/CreditNote/GetAllCreditNote"
# reciept = "https://canarasprings-erp-staging.azurewebsites.net/api/Receipts/Getall"

urls=f"http://20.244.96.22/api"

userloginurl = f"{urls}/User" 
customerurl = f"{urls}/Party/GetAllParties"
product = f"{urls}/Rate/GetAllProducts"
invoice = f"{urls}/Invoice/GetAllInvoices"
creditNote = f"{urls}/CreditNote/GetAllCreditNote"
reciept = f"{urls}/Receipts/Getall"
switchdivisionurl=f"{urls}/User/SwitchDivision"


# Testing Local
# userloginurl = "https://canarasprings-erp-test.azurewebsites.net/api/User"
# customerurl = "https://canarasprings-erp-test.azurewebsites.net/api/Party/GetAllParties"
# product = "https://canarasprings-erp-test.azurewebsites.net/api/Rate/GetAllProducts"
# invoice = "https://canarasprings-erp-test.azurewebsites.net/api/Invoice/GetAllInvoices"
# creditNote = "https://canarasprings-erp-test.azurewebsites.net/api/CreditNote/GetAllCreditNote"
# reciept = "https://canarasprings-erp-test.azurewebsites.net/api/Receipts/Getall"

    
# --------- Customer Login ---------------------
@api_view(["GET", "POST"])
def customerLogin(request, *args, **kwargs):
    if request.method == "GET":
        return Response("Customer Login GET API")

    if request.method == "POST":
        try:
            print("Request data ----->",request.data)
            username = request.data["username"]
            password = request.data["password"]
            add_item = {"username": username, "password": password}
            r = requests.post(userloginurl, json=add_item)
            res = r.json()
            # print("res ------>",res)
            # JWTToken,division=loginCanaraSpring(username,password)
            # print("\nJWT Token ---------->", JWTToken)
            JWTToken = res["token"]
            division=res["divisions"]   
            # print("\n Division ---------->", division)
            userdata={}
            userdata["userId"]=res["userId"]
            x=[]
            for data in division:
                obj={}
                obj["divisionid"] = data["id"]
                obj["branch"]=data["divisionInitial"]
                obj["division"]=data["name"]
                x.append(obj)
            userdata["division"]=x

            return Response({"JWTToken":JWTToken,"userdata":userdata})

        except Exception as e:
            print(" In exception error is -----------------", e)
            return Response("Login Failed")

# --------- Customer Login ---------------------


# ---------------- AccountCode Search ----------------------
@api_view(["GET", "POST"])
def search_acc_code(request, **kwargs):
    if request.method == "POST":
        try:
            print("\n this is seach value------------------", request.data["value"])
            acode = []
            header3 = {
                "x-preserveKey": preserve,
                "x-company": compid,
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
            }
            body2 = {
                "entityType": "ACCT",
                "searchFor": request.data["value"],
                "page": 1,
                "limit": 500,
            }
            acresponse = requests.post(branch, headers=header3, json=body2)
            acode = acresponse.json()

            print("\n this is total acc code -----------", len(acode))
            return Response({"accountcode": acode["data"]["master"]["list"]})

        except Exception as e:
            print("\nin exception ---------", e)
            return Response("Error")

# ------------------- AccountCode Search -------------------


# ---------------- Branch API ----------------
@api_view(["GET", "POST"])
def branchList(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("branchapi get request in try")

        except:
            return Response("branchapi get request in except")

    if request.method == "POST":
        try:
            # Accounting login starts
            global compid, preserve, valuetoken
            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (
                login["compid"],
                login["preservekey"],
                login["token"],
            )

            # Accounting Login ends
            url = branch
            payload = json.dumps({"page": 1, "limit": 500, "entityType": "BRANCH"})
            headers = {
                "x-auth-token": valuetoken,
                "x-preserveKey": preserve,
                "x-company": compid,
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, data=payload)
            res_branch = response.json()
            # print("Branches---->", res_branch)

            payload = json.dumps({"page": 1, "limit": 500, "entityType": "CATEGORY"})
            headers = {
                "x-auth-token": valuetoken,
                "x-preserveKey": preserve,
                "x-company": compid,
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, data=payload)
            res_cat = response.json()

            data_branch = []
            for x in res_branch["data"]["master"]["list"]:
                obj = {}
                obj["branch"] = x["name"]
                obj["gstin"] = x["gstin"]
                obj["state"] = x["branchAddress"]["state"]
                obj["city"] = x["branchAddress"]["city"]
                obj["zip"] = x["branchAddress"]["zip"]
                obj["address1"] = x["branchAddress"]["address1"]
                data_branch.append(obj)

            data_cat = []
            for y in res_cat["data"]["master"]["list"]:
                obj = {}
                obj["category"] = y["options"]
                data_cat.append(obj)

            costcodeurl = branch
            header2 = {
                "x-auth-token": valuetoken,
                "x-preserveKey": preserve,
                "x-company": compid,
                "Content-Type": "application/json",
            }
            body2 = {
                "entityType": "COST_CENTER",
                "allTxnFlag": 1,
                "webhook": 1,
                "page": 1,
                "limit": 500,
            }
            acresponse = requests.post(costcodeurl, headers=header2, json=body2)
            costcode = acresponse.json()
            return Response(
                {
                    "Branch": data_branch,
                    "Category": data_cat,
                    "costCenter": costcode["data"]["master"]["list"],
                }
            )

        except:
            return Response(
                "Please fill all the required fields in your Branches and Categories"
            )

# ---------------- Branch API ----------------


# --------------- Branch Data ---------------------
@api_view(["GET", "POST", "PUT"])
def branchData(request, *args, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get("compid")
            data = userSettings.objects.using('canaraspring').filter(compid=compid).values().order_by("-id")
            return Response(data)
        except:
            return Response("User Setting Data Not Found")

    if request.method == "POST":
        try:
            print("Request data -------->", request.data)
            data = userSettings(username=request.data["username"],userId=request.data["userId"],divisionid=request.data["divisionid"],password=request.data["password"],branchname=request.data["branchname"],branch=request.data["branch"],branchid=request.data["branchid"],city=request.data["city"],state=request.data["state"],zipcode=request.data["zipcode"],saveas=request.data["saveas"],compid=request.data["compid"],gstin=request.data["gstin"],category=request.data["category"],address1=request.data["address1"],ledgersetting=request.data["ledger_settings"],JWTToken=request.data['JWTToken'])
            data.save(using='canaraspring')
            return Response("User Setting Save Successfully")
        except:
            return Response("User Setting Failed Successfully")

    if request.method == "PUT":
        try:
            print("Resquest data --------->", request.data)
            id = request.data["id"]
            data = userSettings.objects.using('canaraspring').filter(id=id).update(branchname=request.data["branchname"],userId=request.data["userId"],divisionid=request.data["divisionid"], branch=request.data["branch"],branchid=request.data["branchid"],city=request.data["city"],state=request.data["state"],zipcode=request.data["zipcode"],saveas=request.data["saveas"],compid=request.data["compid"],gstin=request.data["gstin"],category=request.data["category"],address1=request.data["address1"],ledgersetting=request.data["ledger_settings"])
            return Response("Updated Successfully")
        
        except Exception as e:
            print("E------------->",e)
            return Response("Updated  Failed")

# --------------- Branch Data ---------------------

# canaraspring
# --------------- Customer Sync -----------------
@api_view(["GET", "POST","DELETE"])
def SyncCustomer(request, *args, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            data = Customer_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values(
                "id", "customer_name", "account_no", "status", "compid","remark"
            ).order_by("-id")
            print("\n\nCustomer ------->", data)
            return Response(data)
        except:
            return Response(" Customer Sync Get API")

    if request.method == "POST":
        try:
            JWTToken=request.data["JWTToken"]
            print("\n------------>",request.data["userId"], request.data["branchid"] )
            siwtchdbody = {
                "userId": request.data["userId"],
                "divisionId": request.data["branchid"]
             }
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }
            sw = requests.post(switchdivisionurl, json=siwtchdbody,headers=headers1)
            re=sw.json()
            siwtchtoken=re["token"]
            print("\nNew token --------->",siwtchtoken,"\n\n")
            branch=request.data["branch"]
            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (login["compid"],login["preservekey"],login["token"])

            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")
            print("\n \n Last date --------->", lastsync)

            body1 = {''
                    "pageNumber": "0",  
                    "sortMember": "Id",
                    "pageSize": "250",  
                    "sortDescending": "false",
                    "filters": [
                        {
                            "value": lastsync, 
                            "property": "UpdatedOn",
                            "operator": "lt", 
                        }
                    ],
            
                    "isInActive": "false",
                    "show": "false",
                }

            headers = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {siwtchtoken}",
            }

            print("hey ----------->",headers)
            r = requests.post(customerurl, json=body1, headers=headers)

            res = r.json()
            print("\n c Total Records ----------->", res["item1"]["totalRecords"])
            totalpages=res["item1"]["totalPages"]
            
            data = CustomerSyncUpdate.objects.using('canaraspring').all().values("lastcustomerdate")
            print("inv data------------->",len(data))
            if len(data)==0:
                up=CustomerSyncUpdate(lastcustomerdate="",compid=compid,branch=branch)
                up.save(using="canaraspring")
            else:
                up=CustomerSyncUpdate.objects.using('canaraspring').filter(compid=compid,branch=branch).values()
                # print("\n\n Lenght up ------------",up)
                if len(up)>0:
                    up=CustomerSyncUpdate.objects.using('canaraspring').filter(compid=compid,branch=branch).update(lastcustomerdate=lastsync)
                else:
                    up=CustomerSyncUpdate(lastcustomerdate="",compid=compid,branch=branch)
                    up.save(using="canaraspring")
            data1 = CustomerSyncUpdate.objects.all().values().order_by("-id")
            # print("----------------",data1)

            for tot in range(totalpages):
                if data1[0]['lastcustomerdate']!="":
                    ltdate=data1[0]['lastcustomerdate']
                    print("\nif-----GT---------->")
                    body1 = {
                        "pageNumber": tot,  
                        "sortMember": "Id",
                        "pageSize": "250",  
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": ltdate, 
                                "property": "UpdatedOn",
                                "operator": "gt", 
                            }
                        ],

                        # Static Code 
                        # "filters": [
                        #     {
                        #         "value": "2023-12-01 23:59:59.999", 
                        #         "property": "UpdatedOn",
                        #         "operator": "lt", 
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }
                else:
                    print("\nelse------LT--------->")
                    body1 = {
                        "pageNumber": tot,  
                        "sortMember": "Id",
                        "pageSize": "250",  
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": lastsync,  
                                "property": "UpdatedOn",
                                "operator": "lt",
                            }
                        ],

                        # Static Code 
                        # "filters": [
                        #     {
                        #         "value": "2023-09-01 23:59:59.999",  
                        #         "property": "UpdatedOn",
                        #         "operator": "lt",
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }
                # print("\nheader body ----------------->",body1)
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/plain",
                    "Authorization": f"Bearer {siwtchtoken}",
                }
                print("Customer header ---------->",headers)
                r = requests.post(customerurl, json=body1, headers=headers)

                res = r.json()

                # print("Res ----------->", res)
                # print("Res ----------->", res["item1"]["totalRecords"])

                resdata1 = res["item1"]["records"] 
                print("\n\n Total ------------>",len(resdata1))         
                # 
                if len(resdata1)>0:
                    for resdata in resdata1: 
                        print("\n Resdata-------->",resdata)
                        if "gstNumber" in resdata or resdata["gstNumber"]!=None:
                            gst=resdata["gstNumber"]
                        else:
                            gst=""
                        try:
                            address = resdata["address1"] + "," + resdata["address2"]
                            add_item = {
                                "contactList": [
                                    {
                                        "name": resdata["name"],
                                        "accountNumber": resdata["customerCode"],
                                        "employee": "false",
                                        "vendor": "false",
                                        "customer": True,
                                        "primaryType": "customer",
                                        "address": [
                                                    {
                                                        "address1":address,
                                                        "street": "Street",
                                                        "city": resdata["city"],
                                                        "state": resdata["state"],
                                                        "zip": resdata["pin"],
                                                        "country": "India",
                                                        "type": "PADR"
                                                    }],
                                        "contactGstin": [
                                            {
                                                # "number": resdata["gstNumber"] if "gstNumber" in resdata  else "",
                                                "number": gst,
                                                "verified": "false",
                                                "defaultGstin": True,
                                            }
                                        ],
                                        "status": "COAC",
                                    }
                                ]
                            }
                            print("\n \n Payload for Customer----------->", add_item)

                            headers = {
                                "x-auth-token": valuetoken,
                                "x-preserveKey": preserve,
                                "x-company": compid,
                                "Content-Type": "application/json",
                            }
                            print("\nsend payload to url ------->",acc_mas_url)
                            r = requests.post(acc_mas_url, json=add_item, headers=headers)
                            res = r.json()
                            print("\n\n Accounting Response ------->", res,"\n\n")
                            
                            if res["message"] == "Batch Data Added successfully":
                                message = "Done"
                                a = Customer_records(customer_name=resdata["name"],lastsyncdate=lastsync,account_no=resdata["customerCode"],branch=request.data["branch"],status="SUCCESS",compid=compid,responsejson=add_item,requestjson=resdata,remark=message)
                                a.save(using="canaraspring")

                            else:
                                if "fieldErrors" in res and res["fieldErrors"]!=None:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
            
                                else:
                                    # message=res['errorList']["contactList[0]"]
                                    message=str(res['errorList'].values())
                                    print("\n Error msg ----->",message)
                                a = Customer_records(customer_name=resdata["name"],lastsyncdate=lastsync,account_no=resdata["customerCode"],branch=request.data["branch"],status="FAILED",compid=compid,responsejson=add_item,requestjson=resdata,remark=message)
                                a.save(using="canaraspring")
                                # a.save()
                        except Exception as e:
                            # print("\nthis is res------->",resdata)
                            print("\nthis is error in exception ----->",e,"\n")
                            traceback.print_exc()
                else:
                    return Response("Data Not Found ")

            if res["message"] == "Batch Data Added successfully": return Response("Sync Customer Successfully")
            else: return Response("Sync Customer Failed")

        except Exception as e:
            print(e)
            return Response(f"Missing is {e}")
        
    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=Customer_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed")
        
# --------------- Sync Customer-----------------


# --------------- Sync Inventory item Master-----------------
@api_view(["GET", "POST","DELETE"])
def SyncProduct(request, *args, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            print("Compid ------>",compid)
            data = Product_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values("id","product_code","product_name","group_name","status","remark").order_by("-id")
            print("\n\n Sync Product ------->", data)
            return Response(data)
        except:
            return Response("Data Not Found")

    if request.method == "POST":
        try:
            print("\n Request data ------------>", request.data)
            JWTToken=request.data["JWTToken"]

            branch=request.data["branch"]
            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (login["compid"],login["preservekey"],login["token"])
            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")
            print("\n \n Last date --------->", lastsync)

            bodyproduct = {
                "pageNumber": "0",
                "sortMember": "Id",
                "pageSize": "250",
                "sortDescending": "false",
                "filters": [
                    {
                        "value": lastsync,
                        "property": "UpdatedOn",
                        "operator": "lt",
                    }
                ],
                "isInActive": "false",
                "show": "false",
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }

            r = requests.post(product, json=bodyproduct, headers=headers)
            res = r.json()
            print("\ntotal pages ----------->", res["totalPages"])
            totalpages=res["totalPages"]

            print("\n \n Number of Pages -------->",totalpages)

            data = ProductSyncUpdate.objects.all().values("lastproductdate")
            print("inv data------------->",len(data))
            if len(data)==0:
                up=ProductSyncUpdate(lastproductdate="",compid=compid,branch=branch)
                up.save(using='canaraspring')
            else:
                up=ProductSyncUpdate.objects.filter(compid=compid,branch=branch).values()
                print("\n\n Lenght up ------------",up)
                if len(up)>0:
                    up=ProductSyncUpdate.objects.filter(compid=compid,branch=branch).update(lastproductdate=lastsync)
                else:
                    up=ProductSyncUpdate(lastproductdate="",compid=compid,branch=branch)
                    up.save(using='canaraspring')

            data1 = ProductSyncUpdate.objects.all().values().order_by("-id")
            # print("----------------",data1)
            count=0
            for tot in range(totalpages):
                if data1[0]['lastproductdate']!="":
                    ltdate=data1[0]['lastproductdate']
                    print("\nif------GT--------->")
                    bodyproduct = {
                        "pageNumber": tot,
                        "sortMember": "Id",
                        "pageSize": "250",
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": ltdate,
                                "property": "UpdatedOn",
                                "operator": "gt",
                            }
                        ],
                        
                        # Static Code 
                        # "filters": [
                        #     {
                        #         "value": "2023-09-01 23:59:59.999",
                        #         "property": "UpdatedOn",
                        #         "operator": "gt",
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }
                else:
                    print("\nElse-------LT-------->")
                    bodyproduct = {
                        "pageNumber": tot,
                        "sortMember": "Id",
                        "pageSize": "250",
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value":lastsync,
                                "property": "UpdatedOn",
                                "operator": "lt",
                            }
                        ],

                        # Static Code 
                        # "filters": [
                        #     {
                        #        "value": "2023-09-01 23:59:59.999",
                        #         "property": "UpdatedOn",
                        #         "operator": "gt",
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }

                print("\n Product body ----------------->",bodyproduct)

                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/plain",
                    "Authorization": f"Bearer {JWTToken}",
                }

                r = requests.post(product, json=bodyproduct, headers=headers)

                canarajson = r.json()

                totalrecods = canarajson["totalRecords"]
                print("\n \n Total Records ------------>", totalrecods)
                if len(canarajson["records"])>0:
                    print("\n\n Length --------->", len(canarajson["records"]))
                    for i in canarajson["records"]:
                        # print("\n\n  ------------>",i)
                        if i["isDeleted"] != True:
                            if i["partInfo"]!=None:
                                part=i["partInfo"]
                                # print("\npart in if condition-------->",part)
                            else:
                                part=""
                            print("\npart -------->",part)
                            add_item={
                                "proInventoryList": [
                                    {
                                        "maintainQtyFlag": True,
                                        "inventoryType": "GOODS",
                                        "typeCode": "BOUT",
                                        "name": i["description"],
                                        "nickName": i["description"],
                                        "skuUomGstCode": "KGS",
                                        "baseUnitName": "KILOGRAMS",
                                        "valuationMethod": "AVG",
                                        "inventoryCode": i["code"],
                                        # "groupNameList": [
                                        #     {
                                        #     "Finished":i["partType"]["typeName"]
                                        #     }
                                        # ],
                                        "groupNameList": [
                                            i["partType"]["typeName"]
                                        ],
                                        "inventoryGstSale": {
                                            "uomCode": "KGS",
                                            "hsnCode": "",
                                            "taxability": "TAXABLE",
                                            "gstRate": "18",
                                            "description":part
                                        },
                                        
                                        "inventoryGstPurchase": {
                                            "itcClaimType": "NIL",
                                            "uomCode": "KGS",
                                            "hsnCode": "",
                                            "taxability": "TAXABLE",
                                            "gstRate": "18",
                                            "description":part
                                        },
                                        "inventoryAccount": {
                                            "saleAccountSetting": {
                                                "accountCode": "52000",
                                                "accountName": "Sale of Goods",
                                                "mrpValue": 0,
                                                "priceValue": i["listPrice"],
                                                "discountValue": 0,
                                                "frieghtValue": 0,
                                                "deliveryValue": 0,
                                                "taxValue": 0,
                                                "otherCost": 0,
                                                "amount": 0,
                                            },
                                            "purchaseAccountSetting": {
                                                "accountCode": "40021",
                                                "accountName": "Purchase Account",
                                                "mrpValue": 0,
                                                "priceValue": 0,
                                                "discountValue": 0,
                                                "frieghtValue": 0,
                                                "deliveryValue": 0,
                                                "taxValue": 0,
                                                "otherCost": 0,
                                                "amount": 0,
                                            },
                                        },
                                    }
                                ]
                            }
                            count+=1
                            print(count,"\n\n Product payload -------------->",add_item) 
                            headers = {
                                "x-auth-token": valuetoken,
                                "x-preserveKey": preserve,
                                "x-company": compid,
                                "Content-Type": "application/json",
                            }
                            # print("\nUrl --------------->",acc_mas_url)
                            # print("\nHeaders --------------->",headers)

                            r = requests.post(acc_mas_url, json=add_item, headers=headers)
                            res = r.json()
                            print("\nAccounting Response -------------->", res)
                            
                            if res["message"] == "Batch Data Added successfully":
                                message = "Done"
                                data=Product_records(product_code=i["code"],product_name=i["partType"]["typeName"],group_name=i["description"],lastsyncdate=lastsync,status="SUCCESS",compid=compid,branch=branch,requestjson=i,responsejson=add_item,remark=message)
                                data.save(using="canaraspring")
                            else:
                                if "fieldErrors" in res:
                                    fielderror = res["fieldErrors"]
                                    message = ""
                                    for l in fielderror:
                                        message += l["message"]
                                else:
                                    message = str(res["errorList"].values())
                                data=Product_records(product_code=i["code"],product_name=i["partType"]["typeName"],group_name=i["description"],lastsyncdate=lastsync,status="FAILED",compid=compid,branch=branch,requestjson=i,responsejson=add_item,remark=message)
                                data.save(using="canaraspring")
                
                
                else: 
                    return Response("Data Not Found")
                
            if res["message"] == "Batch Data Added successfully": return Response("Sync Product Successfully")
            else: return Response("Sync Product Failed")
        except Exception as e:
            return Response(f"Missing is {e}")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=Product_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed")
# --------------- Sync Inventory item Master -----------------


# --------------- Sync Invoice-----------------
@api_view(["GET", "POST","DELETE"])
def SyncInvoice(request, *args, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            print("Hello baby ",branch,"\n",compid)
            data = (Sale_Invoice_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values("id","inv_no","inv_date","customer_name","amount","status","remark").order_by("-id"))
            print("\n\n Sync Invoice ------->", data)
            return Response(data)
        except:
            return Response(" Invoice Sync Get API")

    if request.method == "POST":
        try:
            print("\n------------>",request.data["userId"], request.data["branchid"] )
            JWTToken=request.data["JWTToken"]
            siwtchdbody = {
                "userId": request.data["userId"],
                "divisionId": request.data["branchid"]
             }
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }
            sw = requests.post(switchdivisionurl, json=siwtchdbody,headers=headers1)
            re=sw.json()
            siwtchtoken=re["token"]
            print("\nNew token --------->",siwtchtoken,"\n\n")
         
            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (
                login["compid"],
                login["preservekey"],
                login["token"],
            )
            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")
            print("\nLast date --------->", lastsync)
            count=0
            branch=request.data["branch"]
            
            bodyinvoice1 = {
                "pageNumber": "0", 
                "sortMember": "Id",
                "pageSize": "250", 
                "sortDescending": "false",
                "filters": [
                    {
                        "value": lastsync,
                        "property": "UpdatedOn",
                        "operator": "lt",
                    }
                ],
                "isInActive": "false",
                "show": "false",
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {siwtchtoken}",
            }
            r = requests.post(invoice, json=bodyinvoice1, headers=headers)

            canarajson1 = r.json()
            totalpages = canarajson1["totalPages"]
            print("\n Totalpages in Invoices-------->", totalpages)

            data = InvoiceSyncUpdate.objects.all().values("lastinvoicedate")
            # print("inv data------------->",len(data))
            if len(data)==0:
                up=InvoiceSyncUpdate(lastinvoicedate="",compid=compid,branch=branch)
                up.save(using="canaraspring")
            else:
                up=InvoiceSyncUpdate.objects.filter(compid=compid,branch=branch).values()
                if len(up)>0:
                    up=InvoiceSyncUpdate.objects.filter(compid=compid,branch=branch).update(lastinvoicedate=lastsync)
                else:
                    up=InvoiceSyncUpdate(lastinvoicedate="",compid=compid,branch=branch)
                    up.save(using="canaraspring")
            data1 = InvoiceSyncUpdate.objects.all().values().order_by("-id")
            print("Last data  save----------------",data1)
            for tot in range(totalpages):
                if data1[0]['lastinvoicedate']!="":
                    ltdate=data1[0]['lastinvoicedate']
                    print("\nif------GT--------->",ltdate)
                    bodyinvoice = {
                        "pageNumber": tot,  
                        "sortMember": "Id",
                        "pageSize": "250",  
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": ltdate, 
                                "property": "UpdatedOn",
                                "operator": "gt",
                            }
                        ],

                        # Static Code
                        # "filters": [
                        #     {
                        #         "value": "2023-12-01",
                        #         # 2023-10-16 23:59:59.999
                        #         "property": "UpdatedOn",
                        #         "operator": "gt",
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }
                else:
                    print("\n\n Else ------LT---------->" ,tot)
                    bodyinvoice = {
                            "pageNumber": tot,  
                            "sortMember": "Id",
                            "pageSize": "250",  
                            "sortDescending": "false",

                            # Dynamic Code 
                            "filters": [
                                {
                                    "value": lastsync,  
                                    "property": "UpdatedOn",
                                    "operator": "lt",
                                }
                            ],

                            # Static Code
                            # "filters": [
                            #     {
                            #         "value": "2023-12-01",
                            #         "property": "UpdatedOn",
                            #         "operator": "gt",
                            #     }
                            # ],
                            "isInActive": "false",
                            "show": "false",
                        }

                print("\n\n Body Invoice ----------->",bodyinvoice)
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/plain",
                    "Authorization": f"Bearer {siwtchtoken}",
                }
                r = requests.post(invoice, json=bodyinvoice, headers=headers)

                canarajson = r.json()
                # print("Response of Canara Spring ----------->", canarajson['totalPages'])
                print("\n Total records -------->", canarajson["totalRecords"])
                print("\n Total records length -------->", len(canarajson["records"]))                
                resdata1 = canarajson["records"]
                # print("\n\n Canara Spring Invoices Records ------------------->",resdata1)
                if len(resdata1)>0:
                    for i in resdata1:
                        lineitems = []
                        try:
                            date_str = i["invoiceDate"]
                            date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                            formatted_date = date_object.strftime("%d-%m-%Y")

                            # Multiple Line itmes
                            for j in json.loads(i["productDetails"]):
                                lineitmedata = {}
                                lineitmedata = {
                                    "itemCode":j["ProductCode"],
                                    "saleType": "Normal",
                                    "quantity": j["Quantity"],  # ---> Always enter
                                    "unitPrice": j["Rate"],  # --> Bill Amount
                                    "amount": 0,
                                    "total_amount": 0,
                                    "accountName": request.data["ledgersetting"][0][
                                        "ledgerName"
                                    ],
                                }
                                lineitems.append(lineitmedata)

                            print("\n \n Lineitmes ----------->",lineitems)

                            add_item = {
                                "invoiceList": [
                                    {
                                        "number": i["invNo"],
                                        "taxType": "NTAX",
                                        "invoiceType": "NA",
                                        "dueDate": formatted_date,
                                        "date": formatted_date,
                                        "amount": 0,
                                        "contactName": i["party"]["name"],
                                        "companyGstin":request.data["gstin"],
                                        "contactCode": i["party"]["customerCode"],
                                        "currencyCode": "INR",
                                        "placeSupplyName": i["party"]["state"].replace(".",""),
                                        "branch": request.data["branch"],
                                        "typeCode": "SINV",
                                        "status": "INAP",
                                        "vehicleNumber": i["vehicleNumber"],
                                        "billAddress": {
                                            "name": "Null",
                                            "type": "BADR",
                                            "address1": i["party"]["address1"],
                                            "city": i["party"]["city"],
                                            "state": i["party"]["state"],
                                            "state": i["party"]["state"].replace(".",""),
                                            "zip": i["party"]["pin"],
                                            "country": "Null",
                                            "mobile": i["party"]["mobileNumber"],
                                            # "telephone": "Null" if  i["party"]["telephone"] == "" else  i["party"]["phoneNumber"]
                                            "telephone": "",
                                        },
                                        "roundFlag": "false",
                                        "lineItems": lineitems,
                                    }
                                ]
                            }
                            count+=1
                            print("\n \n Count ------>",count,"\n \n Add Items ------->", add_item)
                            headers = {
                                "x-auth-token": valuetoken,
                                "x-preserveKey": preserve,
                                "x-company": compid,
                                "Content-Type": "application/json",
                            }

                            r = requests.post(acc_txn_url, json=add_item, headers=headers)
                            res = r.json()
                            print("\n\nAccounting Response ------->", res)
                            if res["message"] == "Batch Data Added successfully" or res["status"] == 200:
                                message = "Done"
                                print("If ",i["totalAmount"])
                                a = Sale_Invoice_records(inv_no=i["invNo"],lastsyncdate=lastsync, inv_date=formatted_date,customer_name=i["party"]["name"],amount=i["totalAmount"],status="SUCCESS",compid=compid,branch=request.data["branch"], responsejson=add_item,requestjson=i,remark=message)
                                a.save(using="canaraspring")
                            else:
                                if "fieldErrors" in res:
                                    fielderror = res["fieldErrors"]
                                    message = ""
                                    for l in fielderror:
                                        message += l["message"]
                                else:
                                    message = str(res["errorList"].values())
                                print("Esle ",i["totalAmount"])
                                a = Sale_Invoice_records(inv_no=i["invNo"],lastsyncdate=lastsync,inv_date=formatted_date,customer_name=i["party"]["name"],amount=i["totalAmount"],status="FAILED",compid=compid,branch=request.data["branch"],responsejson=add_item,requestjson=i,remark=message)
                                a.save(using="canaraspring")
                                # return Response("Sync Invoice Failed")
                        except Exception as e:
                            print("\n \n Except ------->", e)
                else:return Response("Data Not Found")

            if res["message"] == "Batch Data Added successfully":
                return Response("Sync Invoice Successfully")
            else:
                print("\n \n Esle------------- ")
                return Response("Sync Invoice  Failed")
        except:
            return Response("Sync Invoice  Failed")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=Sale_Invoice_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed")
# --------------- Sync Invoice -----------------



# --------------- Sync CreditNote-----------------
@api_view(["GET", "POST","DELETE"])
def SyncCreditNote(request, *args, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            print("Compid ------>",compid,branch)
            data = CreditNote_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values("id","number","debitamount","creditamount","date","status","remark").order_by("-id")
            print("\n\n Sync Data------->", data)
            return Response(data)
        except:
            return Response("Data Not Found")

    if request.method == "POST":
        try:
            print("\n Request data ------------>", request.data)
            JWTToken=request.data["JWTToken"]
            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")
            print("\n \n Last date --------->", lastsync)
            print("\n------------>",request.data["userId"], request.data["branchid"] )
            JWTToken=request.data["JWTToken"]
            siwtchdbody = {
                "userId": request.data["userId"],
                "divisionId": request.data["branchid"]
             }
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }
            sw = requests.post(switchdivisionurl, json=siwtchdbody,headers=headers1)
            re=sw.json()
            siwtchtoken=re["token"]
            print("\nNew token --------->",siwtchtoken,"\n\n")

            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (login["compid"],login["preservekey"],login["token"])

            creditbody = {
            "pageNumber": "0",
            "sortMember": "Id",
            "pageSize": "250",
            "sortDescending": "false",
            "filters": [
                {
                "value": lastsync,
                "property": "UpdatedOn",
                "operator": "lt"
                }
            ],
            "isInActive": "false",
            "show": "false"
            }
             
     
            print("\nHeader body ----------------->",creditbody)
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {siwtchtoken}",
            }
            r = requests.post(creditNote, json=creditbody, headers=headers)
            canarajson = r.json()

            print("hello--------->",canarajson)
            # return 
            creditdata = canarajson["records"]

            print("\n\n creditdata of length ------------>",len(creditdata))
            if len(creditdata)>0:
                for i in creditdata:
                    print("\n\n i ------------>",i)
                    date_str = i["createdOn"]
                    date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                    formatted_date = date_object.strftime("%d-%m-%Y")
                    print("\n Date ----------->",formatted_date)
                    # if "reasonId" in i:
                    if i["reasonId"]=="null":
                        resId=""
                    else:
                        resId=i["reasonId"]

                    print("\n Res ID----------->",resId)
                    
                    # else:
                    #     pass
                    
                    add_item={
                        "journalList": [
                            {
                                "taxRateFlag":False,
                                "autoNumberFlag": False,
                                "companyGstin": request.data['gstin'],
                                "branch": request.data['branch'],	
                                "category": "Goods",
                                "number": i["creditNoteId"],			
                                "debitAmount": i["amount"],		
                                "creditAmount": i["amount"],		
                                # //"customerGstin": "09ASEPQ2345K1Z1",
                                "manualJournalDetail": [
                                    {
                                        "accountName": "Sales Return",	  # After Testing discuss
                                        "debitAmount": i["amount"],	
                                    },
                                    {
                                        "accountName": i["party"]["name"],	
                                        "creditAmount": i["amount"],
                                    }
                                ],
                                "narration": resId,		
                                "reportflag": 1,
                                "date": formatted_date,		
                                "amount": 0,			
                                "taxType": "ETAX",
                                "status": "MJPT",
                                # "txnStatus": "TRPN",
                                # "txnType": "MJ",
                                "typeCode": "JMJ"
                            }
                        ]
                    }
                    
                    print("\n \n Add items ------->", add_item)
                    headers = {
                            "x-auth-token": valuetoken,
                            "x-preserveKey": preserve,
                            "x-company": compid,
                            "Content-Type": "application/json",
                        }

                    r = requests.post(acc_txn_url, json=add_item, headers=headers)
                    res = r.json()
                    print("\n\n Accounting Response ------->", res)
                    
                    if res["message"] == "Batch Data Added successfully":
                        message = "Done"
                        # CreditNote Records Save 
                        data=CreditNote_records(number=i["creditNoteId"],debitamount=i["amount"],creditamount=i["amount"],date=formatted_date,status="SUCCESS",compid=request.data["compid"],branch=request.data["branch"],requestjson=i,responsejson=add_item,remark=message)
                        data.save(using="canaraspring")

                    else:
                        if "fieldErrors" in res:
                            fielderror = res["fieldErrors"]
                            message = ""
                            for l in fielderror:
                                message += l["message"]
                        else:
                            message = str(res["errorList"].values())
                        data=CreditNote_records(number=i["creditNoteId"],debitamount=i["amount"],creditamount=i["amount"],date=formatted_date,status="FAILED",compid=request.data["compid"],branch=request.data["branch"],requestjson=i,responsejson=add_item,remark=message)
                        data.save(using="canaraspring")

                if res["message"] == "Batch Data Added successfully": return Response("Sync Credit Note Successfully")
                else: return Response("Sync Credit Note Failed")

            else:return Response("Data Not Found")

        except Exception as e:
            print("\n\n Except --------------------->",e)
            return Response(f"Missing is {e}")

    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=CreditNote_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed")

# --------------- Sync CreditNote -----------------

# --------------- Sync Expenses-----------------
@api_view(["GET", "POST","DELETE"])
def SyncExpenses(request, *args, **kwargs):
    if request.method == "GET":
        try:
            print("GET API-----------",request.data)
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            print("Compid ------>",compid,)
            data = Expenses_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values("id","number","debitamount","creditamount","date","status","remark").order_by("-id")
            print("\n\n Sync Data ------->", data)
            return Response(data)
        except:
            return Response("Data Not Found")

    if request.method == "POST":
        try:
            JWTToken=request.data["JWTToken"]
            print("\n------------>",request.data["userId"], request.data["branchid"] )
            siwtchdbody = {
                "userId": request.data["userId"],
                "divisionId": request.data["branchid"]
             }
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }
            sw = requests.post(switchdivisionurl, json=siwtchdbody,headers=headers1)
            re=sw.json()
            siwtchtoken=re["token"]
            print("\nNew token --------->",siwtchtoken,"\n\n")
            

            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")
            print("\n \n Last date --------->", lastsync)

            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (login["compid"],login["preservekey"],login["token"])

            # ------------ Urls GET for Expenses ---------------- 
            date=lastsync.split(" ")[0]
            input_date = datetime.strptime(date, '%Y-%m-%d')
            output_date_str = input_date.strftime('%a %b %d %Y')
            date_value = output_date_str.split(" ")
            print("date_value ----------->",date_value)
            boolean_value = "false"
            endpoint = "Expense/GetAllExpenses" 

            # Construct the URL with encoded spaces
            encoded_date = urllib.parse.quote(output_date_str.encode('utf-8'))
            encoded_boolean = urllib.parse.quote(boolean_value.encode('utf-8'))
            # Construct the final URL.
            expenses = f"{urls}/{endpoint}/{encoded_date}/{encoded_boolean}"
            print("\n\n My urls is --------->",expenses)

            # ------------ Urls GET for Expenses ---------------- 
            expensbody=""
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {siwtchtoken}",
            }

            r = requests.post(expenses, headers=headers1)
            canarajson = r.json()

            print("\n\n Response -------------->",canarajson)
            if len(canarajson["expenses"])==0:
                return Response ("Data Not Found")

            for data in canarajson["expenses"]:
                # print("\n data ------------->",data )
                original_date = data["transactionDate"]
                date_obj = datetime.strptime(original_date, "%Y-%m-%dT%H:%M:%S")
                formatted_date = date_obj.strftime("%d-%m-%Y")
                print("\n \n Formatted dated ----------->",formatted_date)
                add_item = {
                    "journalList": [
                        {
                            "taxRateFlag": False,
                            "branch": request.data['branch'],
                            "category": request.data['category'],
                            "number": data["docNo"],    # save 
                            # "autoNumberFlag":autonf,
                            "debitAmount": data["amount"],  # save 
                            "creditAmount":data["amount"],
                            "companyGstin": request.data['gstin'],
                            "manualJournalDetail":[
                                {
                                "description": data["description"],
                                "accountName": data["expenseType"]["description"],  
                                "debitAmount": data["amount"]
                                },
                                {
                                "description": data["description"],
                                "accountName":data["targetBranch"]["name"], 
                                "creditAmount": data["amount"]
                                }
                            ],
                            "narration": data["description"],
                            "reportflag": 1,
                            "autoReversingDate": None,
                            "date": formatted_date,  # save 
                            "amount": 0,
                            "taxType": "NTAX",
                            "status": "MJPT",
                            "txnStatus": "TRPN",
                            "typeCode":"JMJ",
                        }
                    ]
                }

                print("\n\n add_item ------------>",add_item)
                headers = {
                        "x-auth-token": valuetoken,
                        "x-preserveKey": preserve,
                        "x-company": compid,
                        "Content-Type": "application/json",
                }
                r = requests.post(acc_txn_url, json=add_item, headers=headers)
                res = r.json()
                print("\n Response on Accounting ----------->",res)
                if res['message'] == "Batch Data Added successfully" or res["status"] == 200:
                    print(" ---------------- Batch Data Added successfully")
                    message="Done"
                    data=Expenses_records(number=data["docNo"],debitamount=data["amount"],creditamount=data["amount"],date=formatted_date,status="SUCCESS",compid=request.data["compid"],branch=request.data["branch"],requestjson=data,responsejson=add_item,remark=message)
                    data.save(using="canaraspring")
                else:
                    # if "fieldErrors" in res:
                    #     fielderror=res['fieldErrors']
                    #     message=""
                    #     for l in fielderror:
                    #         l=+l['message']
                    # else:
                    #     message=res['errorList']["contactList[0]"]
                    if "fieldErrors" in res:
                        fielderror = res["fieldErrors"]
                        message = ""
                        for l in fielderror:
                            message += l["message"]
                    else:
                        message = str(res["errorList"].values())

                    print("\n Messages  ----->",message)
                data=Expenses_records(number=data["docNo"],debitamount=data["amount"],creditamount=data["amount"],date=formatted_date,status="FAILED",compid=request.data["compid"],branch=request.data["branch"],requestjson=data,responsejson=add_item,remark=message)
                data.save(using="canaraspring")
            if res["message"] == "Batch Data Added successfully": return Response("Sync Expenses Successfully")
            else: return Response("Sync Expenses Failed")
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response("Except Sync Expenses POST API----------->", e)


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=Expenses_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Deleted Failed")
# --------------- Sync Expenses -----------------

# --------------- Sync Receipt-----------------
@api_view(["GET", "POST","DELETE"])
def SyncReceipt(request, *args, **kwargs):
    if request.method == "GET":
        try:
            print("GET API-----------",request.data)
            compid = request.GET.get("compid")
            branch = request.GET.get("branch")
            print("Compid ------>",compid,)
            data = Receipt_records.objects.using('canaraspring').filter(compid=compid,branch=branch).values("id","number","debitamount","creditamount","date","status","remark").order_by("-id")
            print("\n\n Sync Data ------->", data)
            return Response(data)
        except:
            return Response("Data Not Found")

    if request.method == "POST":
        try:
            print("\n Request data ------------>", request.data)
            JWTToken=request.data["JWTToken"]
            print("\n------------>",request.data["userId"], request.data["branchid"] )
            siwtchdbody = {
                "userId": request.data["userId"],
                "divisionId": request.data["branchid"]
             }
            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {JWTToken}",
            }
            sw = requests.post(switchdivisionurl, json=siwtchdbody,headers=headers1)
            re=sw.json()
            siwtchtoken=re["token"]
            print("\nNew token --------->",siwtchtoken,"\n\n")

            branch=request.data['branch']
            compid, preserve = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = (login["compid"],login["preservekey"],login["token"])

            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            lastsync = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")

            print("\n \n Last date --------->", lastsync)
            recieptbody = {
                    "pageNumber": "0",  
                    "sortMember": "Id",
                    "pageSize": "250",  
                    "sortDescending": "false",
                    "filters": [
                        {
                            "value": lastsync, 
                            # "value": "2023-09-26 23:59:59.999", 
                            "property": "UpdatedOn",
                            "operator": "gt", 
                        }
                    ],
            
                    "isInActive": "false",
                    "show": "false",
                }

            headers1 = {
                "Content-Type": "application/json",
                "Accept": "text/plain",
                "Authorization": f"Bearer {siwtchtoken}",
            }

            # print("hey ----------->",headers1)/
            r = requests.post(reciept, json=recieptbody, headers=headers1)

            res= r.json()
            print("\n --------------- First Test pass----------------")
            # print("Res ----------->", res)
            totalpages=res["totalRecords"]
            # print("total lenght -------------->",len(res["records"]))

            print("\n Totalpages -------------",totalpages)


            data = ReceiptSyncUpdate.objects.using('canaraspring').all().values("lastreceiptdate")
            print("inv data------------->",len(data))
            if len(data)==0:
                up=ReceiptSyncUpdate(lastreceiptdate="",compid=compid,branch=branch)
                up.save(using="canaraspring")
            else:
                up=ReceiptSyncUpdate.objects.using('canaraspring').filter(compid=compid,branch=branch).values()
                print("\n\n Lenght up ------------",up)
                if len(up)>0:
                    up=ReceiptSyncUpdate.objects.using('canaraspring').filter(compid=compid,branch=branch).update(lastreceiptdate=lastsync)
                else:
                    up=ReceiptSyncUpdate(lastreceiptdate="",compid=compid,branch=branch)
                    up.save(using="canaraspring")
            data1 = ReceiptSyncUpdate.objects.all().values().order_by("-id")
            print("\nlastdate----------------",data1[0]['lastreceiptdate'])

            # print("\n Canara Spring data --------->",res)
            for tot in range(totalpages):
                print("tot is ----->",tot)
                if data1[0]['lastreceiptdate']!="":
                    ltdate=data1[0]['lastreceiptdate']
                    print("\nif-----GT---------->")
                    body1 = {
                        "pageNumber": tot,  
                        "sortMember": "Id",
                        "pageSize": "250",  
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": ltdate, 
                                "property": "UpdatedOn",
                                "operator": "gt",
                            }
                        ],

                        # Static Code 
                    #     "filters": [
                    #     {
                    #         "value": "2023-09-26 23:59:59.999", 
                    #         "property": "UpdatedOn",
                    #         "operator": "gt", 
                    #     }
                    #   ],
                        "isInActive": "false",
                        "show": "false",
                    }
                else:
                    print("\nelse------LT--------->")
                    body1 = {
                        "pageNumber": tot,  
                        "sortMember": "Id",
                        "pageSize": "250",  
                        "sortDescending": "false",

                        # Dynamic Code 
                        "filters": [
                            {
                                "value": lastsync,  
                                "property": "UpdatedOn",
                                "operator": "lt",
                            }
                        ],

                        # Static Code 
                        # "filters": [
                        #     {
                        #         "value": "2023-09-26 23:59:59.999",  
                        #         "property": "UpdatedOn",
                        #         "operator": "gt",
                        #     }
                        # ],
                        "isInActive": "false",
                        "show": "false",
                    }
                print("\nheader body ----------------->",body1)
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "text/plain",
                    "Authorization": f"Bearer {siwtchtoken}",

                }
                print("Receipt header ---------->",headers)
                r = requests.post(reciept, json=body1, headers=headers)
                
                resdata=r.json()
                print("\n ------------ Hello -------",resdata)

                resdata1 = resdata["records"] 
                print("\n\n Total ------------>",len(resdata["records"]))  
                if len(resdata["records"])!=0:
                    for data in resdata1:
                        original_date = data["docDate"]
                        date_obj = datetime.strptime(original_date, "%Y-%m-%dT%H:%M:%S")
                        formatted_date = date_obj.strftime("%d-%m-%Y")
                        print("\n \n Formatted dated ----------->",formatted_date)
                        add_item = {
                            "journalList": [
                                {
                                    "taxRateFlag": False,
                                    "branch": request.data['branch'],
                                    "category": request.data['category'],
                                    "number": data["docNo"],    # save 
                                    # "autoNumberFlag":autonf,
                                    "debitAmount": data["docAmt"],  # save 
                                    "creditAmount":data["docAmt"],
                                    "companyGstin": request.data['gstin'],
                                    "manualJournalDetail":[
                                        {
                                        # "description": data["description"],
                                        # "accountName": data["bankId"],   
                                        "accountCode": data["bankId"],   # As per discuss
                                        "debitAmount": data["amount"]
                                        },
                                        {
                                        # "description": data["description"],
                                        "accountName":data["party"]["name"].replace(" ", ""),
                                        "creditAmount": data["amount"]
                                        }
                                    ],
                                    "narration": data["narration"],
                                    "reportflag": 1,
                                    "autoReversingDate": None,
                                    "date": formatted_date,  # save 
                                    "amount": 0,
                                    "taxType": "NTAX",
                                    "status": "MJPT",
                                    "txnStatus": "TRPN",
                                    "typeCode":"JMJ",
                                }
                            ]
                        }
                        print("\n\n add_item ------------>",add_item)
                        headers = {
                                "x-auth-token": valuetoken,
                                "x-preserveKey": preserve,
                                "x-company": compid,
                                "Content-Type": "application/json",
                        }
                        r = requests.post(acc_txn_url, json=add_item, headers=headers)
                        res = r.json()
                        print("\n Response on Accounting ----------->",res)
                        if res['message'] == "Batch Data Added successfully" or res["status"] == 200:
                            print(" ---------------- Batch Data Added successfully")
                            message="Done"
                            a=Receipt_records(number=data["docNo"],debitamount=data["docAmt"],creditamount=data["docAmt"],date=formatted_date,status="SUCCESS",compid=request.data["compid"],branch=request.data["branch"],requestjson=data,responsejson=add_item,remark=message)
                            a.save(using="canaraspring")
                        else:
                            if "fieldErrors" in res:
                                fielderror = res["fieldErrors"]
                                message = ""
                                for l in fielderror:
                                    print("\n error is-------",l)
                                    message += l["message"]
                            else:
                                message = str(res["errorList"].values())
                            print("\n Messages ------->",message)
                            a=Receipt_records(number=data["docNo"],debitamount=data["docAmt"],creditamount=data["docAmt"],date=formatted_date,status="FAILED",compid=request.data["compid"],branch=request.data["branch"],requestjson=data,responsejson=add_item,remark=message)
                            a.save(using="canaraspring") 
                    if res["message"] == "Batch Data Added successfully": return Response("Sync Receipt Successfully")
                    else: return Response("Sync Receipt Failed") 
                else:return Response("Data Not Found ")
            return Response("Data Not Found")
        except Exception as e:
            return Response("Except Sync Receipt POST API ---------->", e)


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=Receipt_records.objects.using('canaraspring').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Deleted Failed")
# --------------- Sync Receipt -----------------


#  -------------- Get Json ---------------
@api_view(["GET", "POST"])
def getJsondata(request, *args, **kwargs):
    if request.method == "GET":
        id = request.GET.get("id")
        type1 = request.GET.get("type")
        tablefrom = request.GET.get("tablefrom")
        print(" JSOn data ------------>", id, "\n", type1, "\n", tablefrom)
        if tablefrom == "Customer":
            print("this is type value ----------->",type1)
            data1 = Customer_records.objects.using('canaraspring').filter(id=id).values(type1)
            # if type1 =="responsejson":
            #     data = data1['responsejson']
            # else:
            #     data = data1
            print("\n\n json ------->", data1)
            return Response(data1)
        elif tablefrom == "Invoice":
            data = Sale_Invoice_records.objects.using('canaraspring').filter(id=id).values(type1)
            print("\n\nInvoice ------->", data)
            return Response(data)
        elif tablefrom == "Product":
            data = Product_records.objects.using('canaraspring').filter(id=id).values(type1)
            print("\n\n Pruduct ------->", data)
            return Response(data)
        elif tablefrom == "Expenses":
            data = Expenses_records.objects.using('canaraspring').filter(id=id).values(type1)
            print("\n\n Expenses ------->", data)
            return Response(data)
        elif tablefrom == "CreditNote":
            data = CreditNote_records.objects.using('canaraspring').filter(id=id).values(type1)
            print("\n\n CreditNote ------->", data)
            return Response(data)
        
        elif tablefrom == "Receipt":
            data = Receipt_records.objects.using('canaraspring').filter(id=id).values(type1)
            print("\n\n Receipt ------->", data)
            return Response(data)
        
        return Response("Get Json API")

#  -------------- Get Json ---------------

# --------------- Sync InventoryGroupMaster-----------------
@api_view(["GET", "POST"])
def SyncInventoryGroupMaster(request, *args, **kwargs):
    if request.method == "GET":
        try:
            return Response(" SyncInventoryGroupMaster Get API")
        except:
            return Response(" SyncInventoryGroupMaster Get API")

    if request.method == "POST":
        try:
            return Response("SyncInventoryGroupMaster POST API")
        except Exception as e:
            return Response("SyncInventoryGroupMaster POST API")

# --------------- Sync InventoryGroupMaster -----------------

# ------------ Searching -------------------------
@api_view(['GET', 'POST'])
def filtertable(request,*args ,**kwargs):
    if request.method=="POST":
        try:
            synctype=request.data["synctype"]
            print("Sync Type------->",synctype)

            searchby=request.data["searchby"]
            print("searchby------->",searchby)

            compid=request.data["compid"]
            print("compid------->",compid)
            branch=request.data["branch"]
            print("branch------->",branch)

            print("re----------",request.data)

            if synctype=="customer":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}

                if "cus_code" in filtered_data:
                    data=Customer_records.objects.using('canaraspring').filter(Q(account_no__icontains=searchby["cus_code"])).filter(compid=compid).values()
                    print("\n Data ---->",data)
                    return Response(data)
                    
                if "cus_name" in filtered_data:
                    data=Customer_records.objects.using('canaraspring').filter(Q(customer_name__icontains=searchby["cus_name"])).filter(compid=compid).values()
                    return Response(data)
                    
                if "status" in filtered_data:
                    data=Customer_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid,branch=branch).values()
                    return Response(data)
                    
            if synctype=="product":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}

                if "product_name" in filtered_data:
                    data=Product_records.objects.using('canaraspring').filter(Q(product_name__icontains=searchby["product_name"])).filter(compid=compid).values()
                    return Response(data)

                if "product_code" in filtered_data:
                    data=Product_records.objects.using('canaraspring').filter(Q(product_code__icontains=searchby["product_code"])).filter(compid=compid).values()
                    return Response(data)
                    
                if "status" in filtered_data:
                    print("Searching ------>",searchby["status"])
                    data=Product_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)
                
            if synctype=="invoice":
                # Filter out items with None values
                filtered_data = {key: value for key, value in searchby.items() if value is not None}

                print("\n Searching for ------->",filtered_data)

                if "number" in filtered_data:
                    data=Sale_Invoice_records.objects.using('canaraspring').filter(Q(inv_no__icontains=searchby["number"])).filter(compid=compid).values()
                    return Response(data)

                if "amount" in filtered_data:
                    data=Sale_Invoice_records.objects.using('canaraspring').filter(Q(amount__icontains=searchby["amount"])).filter(compid=compid).values()
                    return Response(data)
                
                if "status" in filtered_data:
                    print("Searching ------>",searchby["status"])
                    data=Sale_Invoice_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)
                
                if "startdate" in filtered_data:
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
                            data=Sale_Invoice_records.objects.using('canaraspring').filter(Q(inv_date__exact=date)).filter(compid=compid).values()
                            for da in data:
                                data1.append(da)
                        return Response(data1)
                
           
            if synctype=="creditnote":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}

                if "cus_name" in filtered_data:
                    data=CreditNote_records.objects.using('canaraspring').filter(Q(number__icontains=searchby["cus_name"])).filter(compid=compid).values()
                    return Response(data)

                if "acc_name" in filtered_data:
                    data=CreditNote_records.objects.using('canaraspring').filter(Q(creditamount__icontains=searchby["acc_name"])).filter(compid=compid).values()
                    return Response(data)
                
                if "status" in filtered_data:
                    print("Searching ------>",searchby["status"])
                    data=CreditNote_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)
                           
           
            if synctype=="expense":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}

                if "expense_amount" in filtered_data:
                    data=Expenses_records.objects.using('canaraspring').filter(Q(creditamount__icontains=searchby["expense_amount"])).filter(compid=compid).values()
                    return Response(data)

                if "expense_number" in filtered_data:
                    data=Expenses_records.objects.using('canaraspring').filter(Q(number__icontains=searchby["expense_number"])).filter(compid=compid).values()
                    return Response(data)
                
                if "status" in filtered_data:
                    print("Searching ------>",searchby["status"])
                    data=Expenses_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)

            if synctype=="receipt":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}
                if "receipt_amount" in filtered_data:
                    data=Receipt_records.objects.using('canaraspring').filter(Q(creditamount__icontains=searchby["receipt_amount"])).filter(compid=compid).values()
                    return Response(data)

                if "receipt_number" in filtered_data:
                    data=Receipt_records.objects.using('canaraspring').filter(Q(number__icontains=searchby["receipt_number"])).filter(compid=compid).values()
                    return Response(data)
                
                if "status" in filtered_data:
                    print("Searching ------>",searchby["status"])
                    data=Receipt_records.objects.using('canaraspring').filter(Q(status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)
                
            return Response("Data Not Found!")
        except:
            return Response("Data Not Found!")
# ------------ Searching -------------------------  