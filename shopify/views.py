from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Shopify, Customer, Sales, Sync, Sales_order
from django.http import HttpResponse
from datetime import date
from datetime import datetime
from django.core import serializers
from rest_framework.parsers import JSONParser
import requests
import datetime as dt
import time
from datetime import timedelta
from . import Accounting
# ---------------------- Live Accounting Urls ---------------------------
# url4 = "https://in2accounts.hostbooks.com/api/transaction/add"
# url3 = "https://inapiaccounts.hostbooks.com/user/validateUserLogin"
# branchurl = "https://in2accounts.hostbooks.com/api/master/list"
# ---------------------- Live Accounting Urls ---------------------------

# Accouting Urls
branchurl = "https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url = "https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url = "https://booksapi.hostbooks.in/hostbook/api/master/add"




# --------------------- Branch API POST ------------------------------------
@api_view(['GET', 'POST'])
def branchlist(request, **kwargs):
    try:
        if request.method == "POST":
            start_time = time.time()
            global compid, preservekey, valuetoken
            compid, preservekey = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preservekey, compid)
            compid, preservekey, valuetoken = (login["compid"], login["preservekey"],login["token"])
            
            print("total data............", request.data)
            headers1 = {
                "Content-Type": "application/json",
                "x-preserveKey": preservekey,
                "x-company":  compid,
                'x-auth-token': valuetoken,
            }
            add_item = {
                "page": 1,
                "limit": 20,
                "entityType": "BRANCH"
            }
            data = []
            r3 = requests.post(branchurl, headers=headers1, json=add_item)
            token4 = r3.json()
            blist = token4['data']['master']['list']
            for x in blist:
                branchdata = {}
                branchdata['branch'] = x['name']
                branchdata['gst'] = x['gstin']
                data.append(branchdata)
            print("--- %s seconds ---" % (time.time() - start_time))
            return Response(data)
        else:
            return Response("LOGIN FAILED......")
    except:
        return Response("LOGIN FAILED......")

# -------------------- Branch API POST END----------------------------------

# --------------- Shopify Login and Get Data from Shopify-------------------

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def shopifylogin(request, **kwargs):
    if request.method == "GET":
        try:
            Id = request.GET.get("id")
            compid = request.GET.get("compid")
            if Id is not None:
                data = Shopify.objects.using('shopifytb').filter(id=Id).values()
                return Response(data)
            else:
                data5 = Shopify.objects.using('shopifytb').filter(compid=compid).values()
                return Response(data5)
        except:
            return Response("UNAUTHORIZED ACCESS...")

    if request.method == 'POST':
        try:
            token = request.data['token']
            storename = request.data['storename']
            compid = request.data['compid']
            suspense = request.data['suspense']
            url1 = 'https://%s.myshopify.com/admin/api/2022-10/shop.json' % (
                storename)
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': token
            }
            r = requests.get(url1, headers=headers)
            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            if r.ok:
                nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                lastsync = nowc.strftime("%Y"+"-"+"%m"+"-"+"%d"+"T"+"%H"+":"+"%M"+":"+"%S")
                dc = Shopify(compid=compid, token=token, storename=storename, gstin=request.data['gstin'], branch=request.data['branch'], transaction1=request.data['transaction1'], storecode=request.data["storecode"], lastsync=lastsync, datetime1=request.data["datetime1"], ccode=request.data['ccode'], ccodepre=request.data['ccodepre'], stage=request.data['stage'],gst_rates=request.data["gst_rates"],manage_attribute=request.data["manage_attribute"],gst_param=request.data["gst_param"],suspense=suspense)
                dc.save(using="shopifytb")
                return Response('LOGIN SUCCESSFULLY...')
            else:
                return Response("UNAUTHORIZED ACCESS...")
        except Exception as e:
            print("i am in except....................",e)
            return Response("UNAUTHORIZED ACCESS...")

    if request.method == "PUT":
        queryset = Shopify.objects.using('shopifytb').filter(id=request.data['id']).update(storecode=request.data['storecode'], token=request.data['token'], storename=request.data['storename'], gstin=request.data['gstin'],branch=request.data['branch'], transaction1=request.data['transaction1'], ccode=request.data['ccode'], ccodepre=request.data['ccodepre'], stage=request.data['stage'],gst_rates=request.data["gst_rates"],manage_attribute=request.data["manage_attribute"],gst_param=request.data["gst_param"],suspense=suspense)
        return Response(queryset)

    if request.method == "PATCH":
        nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        lastsync1 = nowc.strftime("%Y"+"-"+"%m"+"-"+"%d"+"T"+"%H"+":"+"%M"+":"+"%S")
        print(lastsync1)
        query1 = Shopify.objects.using("shopifytb").get(id=request.data['id'])
        query1.lastsync = lastsync1
        query1.save(using="shopifytb")
        return Response("UPDATE SUCCESSFULLY...")

# ----------- Shopify Login and Get Data from Shopify End ------------------

# -----------------------Sync SalesOrder------------------------------------
@api_view(['GET', 'POST', 'PUT'])
def syncsalesorder(request, **kwargs):
    sucord = 0
    failord = 0
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            print("comid in Sales -----------", compid)
            storecod = request.GET.get("storecode")
            syncso1 = Sales_order.objects.using("shopifytb").filter(compid=compid, storecode=storecod).all()
            rec_json = serializers.serialize('json', syncso1)
            return HttpResponse(rec_json, content_type='application/json')
        except:
            return HttpResponse("COULDN'T FETCH RECORDS !!!!")

    if request.method == "POST":
        try:
            global preservekey, valuetoken
            toke = request.data['token']
            storename1 = request.data['storename']
            gstin = request.data['gstin']
            branch = request.data['branch']
            ccode = request.data["ccode"]
            ccodepre = request.data["ccodepre"]
            stage = request.data["stage"]
            storecode = request.data['storecode']
            # preservekey = request.data['preservekey']
            storecode = request.data['storecode']
            manage_attribute = request.data['manage_attribute']
            gst_rates = request.data['gst_rates']
            gst_param = request.data['gst_param']
            suspense =request.data['suspense']
            compid, preservekey = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preservekey, compid)
            compid, preservekey, valuetoken = (login["compid"], login["preservekey"],login["token"])


            if (request.data['salestime'] == "firsttime"):
                lastsyncorder = request.data['datetime1']
            else:
                lastsyncorder = request.data['salestime']
            
            print("last sync date rahul............", lastsyncorder)
            lstsales = "2014-04-25T16:15:47-04:07"


             # Stage ----------------------
            if stage == "Draft":
                statusord = "SODT"
            elif stage == "Approve":
                statusord = "SOAP"
            else:
                statusord = "SOPD"

            start_time = time.time()

            url2 = "https://%s.myshopify.com/admin/api/2022-07/orders.json?status=any&created_at_min=%s&limit=250" % (
                storename1, lstsales)
            print(url2)
            headers = {"Content-Type": "application/json",
                       "X-Shopify-Access-Token": toke
                       }
            r = requests.get(url2, headers=headers)
            invoice = r.json()
            print("Invoices is ----------->",invoice)
            # ---------------------------------- Post Data On Accounting-----------------------------------
            url_header = {
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey":  preservekey,
                "x-company": compid
            }
            ord = invoice["orders"]
            tot = len(ord)
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            batch = ('HB/'+now.strftime("%d""%m""%y""%H""%M""%S"))
            invoicedata = {}
            
            for val in ord:
                try:
                    print("\n ----------------------------------Loop Start again--------------------------------------------")
                    currency1 = val["current_subtotal_price_set"]['shop_money']['currency_code']
                    odnum = val['order_number']
                    print("\norder_number--------------------", val['id'])

                    cdate = val['created_at']
                    if (val['payment_terms'] != None):
                        dueDate = val['payment_terms']['payment_schedules'][0]['due_at']
                    else:
                        dueDate = None
                    category = val["financial_status"]

                    # New Conditions Error---------------------

                    if val["financial_status"] == "paid" :
                        if(val['gateway']=="manual" and val['tags']==""):
                            contactCode=suspense
                        elif(val['gateway']=="manual" and val['tags']!=""):
                            contactCode=val['tags']
                        else:
                            contactCode=ccodepre
                    else:
                        if(val['gateway']=="manual" and val['tags']==""):
                            contactCode=suspense
                        elif(val['gateway']=="manual" and val['tags']!=""):
                            contactCode=val['tags']
                        else:
                            contactCode=ccode

                    # New Conditions Error---------------------

                    if (val['customer']['note'] != None):
                        gstnote1 = val['customer']['note'][-15:]
                        gstntype = "B2B"
                        invoicetype = "R"
                    else:
                        gstnote1 = None
                        gstntype = "B2C"
                        invoicetype = "NA"

                    if 'billing_address' in val:
                        state = val['billing_address']["province"] or "Null"
                        Zip = val['billing_address']["zip"] or "Null"
                        country1 = val['billing_address']["country"] or "Null"
                        add1 = val['billing_address']['address1'] or "Null"
                        add2 = val['billing_address']['address2'] or "Null"
                        city = val['billing_address']['city'] or "Null"
                        mobileinv = val['billing_address']["phone"].replace(
                            " ", "") or "Null"
                        shipcustomer = val['billing_address']["name"] or "Null"
                        bill_address = (add1+" "+add2)
                    else:
                        state = "Null"
                        Zip = "Null"
                        country1 = "Null"
                        city = "Null"
                        bill_address = "Null"
                        mobileinv = "Null"
                        shipcustomer = "Null"

                    print("\nBill_address, city, state, Zip, country1 -----------------------",
                          bill_address, city, state, Zip, country1)

                    if 'shipping_address' in val:
                        shipadd1 = val['shipping_address']["address1"] or "Null"
                        shipadd2 = val['shipping_address']["address2"] or "Null"
                        shipp_address = shipadd1 + " "+shipadd2
                        mobileship = val['shipping_address']["phone"].replace(
                            " ", "") or "Null"
                        shipp_city = val['shipping_address']["city"] or "Null"
                        shipp_state = val['shipping_address']["province"] or "Null"
                        shipp_zip = val['shipping_address']["zip"] or "Null"
                        shipp_country = val['shipping_address']["country"] or "Null"

                    else:
                        shipp_address = "Null"
                        shipp_city = "Null"
                        shipp_state = "Null"
                        shipp_zip = "Null"
                        shipp_country = "Null"
                        mobileship = "Null"
                        
                    print("\nShiping address, shipp_city, shipp_state, shipp_zip, shipp_country------------------------",
                          shipp_address, shipp_city, shipp_state, shipp_zip, shipp_country)
                    total_price = val['total_price']
                    lineitem_var = val['line_items']
                    line_itemlength = len(lineitem_var)
                    final_item_list = []
                    for ele in lineitem_var:
                        try:
                            item_code = ele['product_id']
                            finaldiscount1 = float(0)
                            finaldiscountadd = float(0)
                            finalqty = float(ele['quantity'])
                            lendis = len(ele['discount_allocations'])
                            if lendis == 2:
                                finaldiscount1 = float(
                                    ele['discount_allocations'][0]['amount'])
                                finaldiscount1 = finaldiscount1/finalqty
                                finaldiscountadd = float(
                                    ele['discount_allocations'][1]['amount'])
                                finaldiscountadd = finaldiscountadd/finalqty
                            elif lendis == 1:
                                finaldiscount1 = float(
                                    ele['discount_allocations'][0]['amount'])
                                finaldiscount1 = finaldiscount1/finalqty
                                finaldiscountadd = float(0)
                            else:
                                finaldiscount1 = 0
                                finaldiscountadd = 0.00


                            # ----------------- First Changes (manage attributes)-----------------------------
                            variant=""
                            attoption=[]
                            attributes=[]
                            if manage_attribute =="Yes":
                                if (ele['variant_title'] != "" or ele['variant_title'] != None):
                                    aatvar = (ele['variant_title'].replace(" ", "")).split('/')
                                    norobj = {"attributeOptionName": aatvar[0]}
                                    attoption.append(norobj)
                                    if (len(aatvar) == 2):
                                        colobj = {"attributeOptionName": aatvar[1]}
                                        attoption.append(colobj)
                                    attributes.append({"quantityAttribute": {"inventoryQuantityAttributeOptionList": attoption},
                                                                "quantity": ele['quantity'],
                                                                "unitPrice":ele['price'],
                                                        })
                                else:
                                    pass
                            else:
                                attributes.append({"quantity": ele['quantity'],"unitPrice":ele['price']})
                                variant=ele['variant_title']
                                
                                print("variant-----------------",variant)
                            #-------------------- changes in attributes--------------------------
                            ref = val["discount_codes"]
                            if len(ref) > 0:
                                print("\n Reference ------------IF-----------", ref)
                                code1 = ref[0]["code"]
                            else:
                                code1 = "Null"
                                print("\n Reference ------------Else-----------", ref)
                              


                            # ---------------------------- Second Changes  (Gst_Rates) ------------------------------------
                            unitprice=float(ele['price'])
                            print("unit price ---------------",unitprice)
                            gstrateper=None
                            if gst_rates =="Custom":
                                for i in gst_param:
                                    if unitprice>=i['from_amount'] and unitprice<=i['to_amount']:
                                        gstrateper=i['gst_rate']
                                        print("Gst_Rates ----------------",gstrateper)

                            else:
                                if len(ele['tax_lines'])!= 0:
                                    gstrateper = (ele['tax_lines'][0]['rate'])*100
                            # ----------------------------  Gst_Rates ------------------------------------


                            freightUnit = val['total_shipping_price_set']['shop_money']['amount']
                            print("Freight Unit -----------------------------------", freightUnit)

                            item_dict = {
                                "saleType": "Normal",
                                "inventoryType": "INVTP",
                                "itemCode":ele['sku'],
                                "itemName": ele['title'],
                                "txnQtyAllocationData": {"txnQtyAllocationList":attributes},
                                "description": variant,
                                "gstRate": gstrateper,
                                "freightUnit": float(freightUnit)/line_itemlength,
                                "discount": finaldiscount1,
                                "addDiscount": round(finaldiscountadd, 0),
                                "hsnSac": None,
                                "type": "Goods",
                                "accountName": "Sale of Goods",
                                "fetchAuto": "True"
                            }
                            final_item_list.append(item_dict)
                            item_code = val['line_items'][0]['product_id']
                            item_title = val['line_items'][0]['title']
                            item_variant = val['line_items'][0]['variant_title']
                            item_quantity = val['line_items'][0]['quantity']
                            item_price = val['line_items'][0]['price']
                            items = val['line_items'][0]['tax_lines']

                        except Exception as e:
                            print("\nMissing in Line items -----------------------------------",e)
                            pass
                        
                    invoicedata = {"currencyCode": currency1, "number": odnum, "date": cdate, "dueDate": dueDate, "contactCode": contactCode, "customerGstin": gstnote1, "placeSupplyName": state, "address1": bill_address, "city": city, "state": state, "zip": Zip, "country": country1, "shipaddress1": shipp_address,"city1": shipp_city, "state1": shipp_state, "zip1": shipp_zip, "country1": shipp_country, "totalamount": total_price, "itemCode": item_code, "itemName": item_title, "attributeOptionName": item_variant, "quantity": item_quantity, "unitPrice": item_price, "taxlines": items, "line_items_list": final_item_list}

                    if (dueDate != None):
                        du = cdate
                        x = du.split('T')[0].split('-')
                        pidate = x[2]+"-"+x[1]+"-"+x[0]
                        print("Pidate =------------", pidate)
                    else:
                        date = cdate
                        date_1 = dt.datetime.strptime(
                            date.split("T")[0], "%Y-%m-%d")
                        end_date = date_1 + timedelta(days=10)
                        date_2 = end_date.strftime("%d-%m-%Y")
                        pidate = date_2
                    ddate = invoicedata['date']
                    y = ddate.split('T')[0].split('-')
                    oidate = y[2]+"-"+y[1]+"-"+y[0]
                    shipOrderTime = cdate.split("T")[1][:8]

                    if (val['customer']['email'] != None):
                        shipemail = val['customer']['email']
                    else:
                        shipemail = "Null"

                    add_item = {
                        "salesOrderList":
                        [
                            {
                                "taxType": "ITAX",
                                "currencyCode": invoicedata['currencyCode'],
                                "companyGstin":gstin,
                                "branch":branch,
                                "Category":category,
                                "invoiceType":invoicetype,
                                "number":invoicedata['number'],
                                "date":oidate,
                                "expiryDate":pidate,
                                "contactCode":invoicedata['contactCode'],
                                "contactName":"",
                                "reference": code1,
                                "customerGstin":invoicedata['customerGstin'],
                                "placeSupplyName":invoicedata['placeSupplyName'],
                                "billAddress":{
                                    "address1": invoicedata['address1'],
                                    "city":invoicedata['city'],
                                    "state":invoicedata['state'],
                                    "zip":invoicedata['zip'],
                                    "country":invoicedata['country'],
                                    "mobile":mobileinv,
                                    "name":shipcustomer,
                                    "email":shipemail,
                                    "pan":"",
                                    "gstin":"",
                                    "type":"BADR"
                                },
                                "shipAddress": {
                                    "name": val['shipping_address']["name"],
                                    "address1": invoicedata['shipaddress1'],
                                    "city":invoicedata['city1'],
                                    "state":invoicedata['state1'],
                                    "zip":invoicedata['zip1'],
                                    "country":invoicedata['country1'],
                                    "mobile":mobileship,
                                    "email":shipemail,
                                    "pan":"",
                                    "gstin":"",
                                    "type":" SADR "
                                },

                                "shipmentDetail": {
                                    "shipDeliveryDate": oidate,
                                    "shipOrderTime": shipOrderTime,
                                    "shipPaymentType": val["financial_status"],
                                    "shipPaymentId":val['token'],
                                    "shipTokenId": val['token'],
                                    "shipOrderSource": "Shopify",
                                },

                                "shipCustomerId": val['customer']['id'],
                                "shipCustomerName":shipcustomer,
                                "billingPersonEmail":shipemail,
                                "billingPersonMobile":mobileship,

                                "warehouseAddress":None,
                                "termCondition":None,
                                "customersNotes":None,
                                "shippingNumber":None,
                                "shippingDate":None,
                                "shippingPortCode":None,
                                "purchaseOrderNumber":None,
                                "purchaseOrderDate":None,
                                "buyerOrderNumber":None,
                                "buyerOrderDate":None,
                                "eWayBillNumber":None,
                                "eWayBillDate":None,
                                "lRNo":None,
                                "otherReference":None,
                                "vendorCode":None,
                                "vehicleNumber":None,
                                "termsOfPayment":None,
                                "cin":None,
                                # "amount":invoicedata['totalamount'],
                                "amount":0,
                                "roundingAmount":0,
                                "reverseChargeFlag":False,
                                "flatDiscountFlag":True,
                                "flatAddDiscountFlag":True,
                                "flatCessFlag":False,
                                "flatSubsidyFlag":False,
                                "txnDiscountList":None,
                                "lineItems": invoicedata['line_items_list'],
                                "typeCode": "SINV",
                                "status": statusord,
                                "gstnType": gstntype,

                            }
                        ]
                    }

                    r = requests.post(acc_txn_url, json=add_item,  headers=url_header)
                    print("\n", add_item)
                    print("\n", r.json(), "\n")

                    # Batch Data Added successfully
                    if (r.json()['fieldErrors'] == None) or (r.json()['message'] == "Batch Data Added successfully"):
                        res2 = "Done"
                    else:
                        res2 = r.json()['fieldErrors'][0]['message']
                    if (r.json()['status'] == 200) or (r.json()['status'] == 201):
                        statusmsg = "SUCCESS"
                        sucord += 1
                    else:
                        statusmsg = "FAILED"
                        failord += 1
                    status = statusmsg
                    remark = res2
                    module_type = "Sales Order"
                    so_no = invoicedata['number']
                    amount = invoicedata['totalamount']
                    date = oidate
                    customer = invoicedata['contactCode']

                    sales1 = Sales_order(compid=compid, so_no=so_no, so_amount=amount, so_date=date, batch=batch,remark=remark, status=status, customer_name=customer, module_type=module_type, storecode=storecode, postjson=add_item)
                    sales1.save(using="shopifytb")

                except Exception as a:
                    print("Jump For loop Excepts---------------",a)
                    failord += 1
                    status = "FAILED"
                    remark = "Some data is missing from Shopify"
                    module_type = "Sales Order"
                    so_no = invoicedata['number']
                    amount = invoicedata['totalamount']
                    add_item1 = {"Order Number": val['order_number']}
                    date = oidate
                    customer = invoicedata['contactCode']
                    sales1 = Sales_order(compid=compid, so_no=so_no, so_amount=amount, so_date=date, batch=batch,remark=remark, status=status, customer_name=customer, module_type=module_type, storecode=storecode, postjson=add_item1)
                    sales1.save(using="shopifytb")


            modulesync = "Sales Order"
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d"+"T"+"%H"+":"+"%M"+":"+"%S")
            totalrecordscus = tot
            successcus = sucord
            failcus = failord
            status1 = ""
            if failcus == 0:
                status1 = "SUCCESS"
            elif successcus == 0:
                status1 = "FAILED"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode, recordjson=ord)
            c.save(using="shopifytb")
            print("Sales Order Time --- %s seconds ---" %(time.time() - start_time))
            res1 = r.json()['message']
            if res1 == "Batch Data Added successfully":
                return Response("SYNC ORDER SUCCESSFULLY...")
            else:
                return Response("SYNC ORDER FAILED !!!")
        except Exception as x:
            print("Outside Except ...............",x)
            modulesync = "Sales Order"
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d" +
                                 "T"+"%H"+":"+"%M"+":"+"%S")
            totalrecordscus = tot
            successcus = sucord
            failcus = failord
            status1 = ""
            if failcus == 0:
                status1 = "FAILED"
            elif successcus != 0:
                status1 = "SUCCESS"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode, recordjson=ord)
            c.save(using="shopifytb")
            return Response("SYNC ORDER FAILED !!!")

    if request.method == "PUT":
        try:
            postdata = request.data['data']
            preservekey = request.data["preservekey"]
            order = request.data['data'][0]['order']
            batch = request.data['data'][0]['batch']
            compid, preservekey = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preservekey, compid)
            compid, preservekey, valuetoken = (login["compid"], login["preservekey"],login["token"])
            url_header = {
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey":  preservekey,
                "x-company": compid
            }
            for i in postdata:
                sales112 = Sales_order.objects.using("shopifytb").filter(
                    batch=batch, so_no=order).values('postjson').get()['postjson']
                r = requests.post(acc_txn_url, json=sales112, headers=url_header)
                print("\n", r.json())
                a = r.json()['status']
                if a == 200 or a == 201:
                    succ = Sync.objects.using("shopifytb").filter(
                        batch=batch).values("success_record").get()
                    singleSuccess = int(succ['success_record'])+1
                    succ1 = Sync.objects.using("shopifytb").filter(
                        batch=batch).values("fail_record").get()
                    singlefail = int(succ1['fail_record'])-1
                    sales1 = Sales_order.objects.using("shopifytb").filter(
                        batch=batch, so_no=order).update(status="SUCCESS", remark="Done")
                    c = Sync.objects.using("shopifytb").filter(batch=batch).update(
                        success_record=singleSuccess, fail_record=singlefail)
                    st = "SYNC ORDER SUCCESSFULLY..."
                else:
                    st = "SYNC ORDER FAILED !!!"
                    sales1 = Sales_order.objects.using("shopifytb").filter(batch=batch, so_no=order).update(
                        remark=r.json()['fieldErrors'][0]['message'])
            return Response(st)
        except Exception as x:
            print("Outside Except ...............",x)
            return Response("SYNC ORDER FAILED !!!")

# -----------------------Sync End SalesOrder--------------------------------



# ----------------------------- Sync Manage --------------------------------
@api_view(['GET', 'POST'])
def sync(request, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            print("comid in Sync ---------------", compid)
            storecod = request.GET.get("storecode")
            sync = Sync.objects.using("shopifytb").filter(compid=compid, storecode=storecod).all()
            rec_json = serializers.serialize('json', sync)
            return HttpResponse(rec_json, content_type='application/json')

        except:
            return Response("COULDN'T FETCH RECORDS !!!!")
# --------------------------- Sync Manage End ------------------------------


# ----------------SynItem (CustomerSync)------------------------------------
@api_view(['GET', 'POST'])
def syncItem(request, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            print("comid in customer===", compid)
            storecod = request.GET.get("storecode")
            customers = Customer.objects.using("shopifytb").filter(compid=compid, storecode=storecod).all()
            rec_json = serializers.serialize('json', customers)
            return HttpResponse(rec_json, content_type='application/json')
        except:
            return HttpResponse("COULDN'T FETCH RECORDS !!!!")

    if request.method == "POST":
        suc = 0
        fail = 0
        print("comid in customerpost===", request.data)
        compid = request.data['compid']
        compid = request.data['compid']
        preservekey = request.data['preservekey']
        try:
            token = request.data['token']
            storename1 = request.data['storename']
            storecode = request.data['storecode']
            if (request.data['customertime'] == "firsttime"):
                lastsynccustomer = request.data['datetime1']
            else:
                lastsynccustomer = request.data['customertime']
            lstitem = "2014-04-25T16:15:47"

            # lastsyncitem = now.strftime("%Y"+"-"+"%m"+"-"+"%d")  # in future use at created_at_min=2022-10-17 (shopify url updated)

            # url1= "https://gcl-ecommerce.myshopify.com/admin/api/2022-07/customers.json?status=any&created_at_min=2014-04-25T16:15:47-04:07"

            url1 = "https://%s.myshopify.com/admin/api/2022-07/customers.json?status=any&created_at_min=%s" % (
                storename1, lstitem)

            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': token,
            }

            r = requests.get(url1, headers=headers)
            data = r.json()
            compid, preservekey = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preservekey, compid)
            compid, preservekey, valuetoken = (login["compid"], login["preservekey"],login["token"])
            url_header = {
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey": preservekey,
                "x-company": compid,
            }

            start_time = time.time()
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            batch = ('HB/'+now.strftime("%d""%m""%y""%H""%M""%S"))
            company = data['customers']
            for x in company:
                id1 = x['id']
                email = x['email']
                fn = x['first_name']
                ln = x['last_name']
                ph = x['phone']
                note1 = x['note']
                xstate = x['state']
                if (xstate == "enabled"):
                    if (note1 == None):
                        note = ""
                    else:
                        note = note1[-15:].upper()
                    addressss = len(x['addresses'])
                    if not addressss:
                        address1 = "None"
                        address2 = "None"
                        city = "None"
                        province = "None"
                        pzip = "None"
                        cont = "None"
                    else:
                        address1 = x['addresses'][0]['address1']
                        address2 = x['addresses'][0]['address2']
                        city = x['addresses'][0]['city']
                        province = x['addresses'][0]['province']
                        pzip = x['addresses'][0]['zip']
                        cont = x['addresses'][0]['country_name']

                    all_data = {'id': id1, 'email': email, 'fn': fn, 'ln': ln, 'ph': ph, 'note': note, 'address1': address1,
                                'address2': address2, 'city': city, 'province': province, 'zip': pzip, 'cont': cont}

                    add_item2 = {'contactList': [{'name': all_data['fn']+" " + all_data['ln'], 'accountNumber': all_data['id'], 'employee': False, 'vendor': False, 'customer': True, 'primaryType': 'customer', 'contactPerson': [{'emailAddress': all_data['email'], 'firstName': all_data['fn'], 'lastName': all_data['ln'], 'primeFlag': 1}], 'pan': None, 'creditLimit': None, 'email': None, 'phone': None, 'mobile': all_data['ph'], 'skype': None, 'website': None, 'address': [{'addressGSTIN': all_data['note'],
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'note': None, 'address1': all_data['address1'], 'address2': all_data['address2'], 'street': None, 'city': all_data['city'], 'state': all_data['province'], 'zip':  all_data['zip'], 'country':all_data['cont'], 'mobile': all_data['ph'], 'pan': None, 'tan': None, 'gstin': None, 'cin': None, 'telephone': None, 'type': 'PADR'}], 'openingBalance': 0, 'openingDate': None, 'notes': None, 'termsAndCondition': None, 'status': 'COAC', 'cinNumber': None, 'panVerified': False, 'fax': None}]}

                    add_item1 = {'contactList': [{'name': all_data['fn']+" " + all_data['ln'], 'accountNumber': all_data['id'], 'employee': False, 'vendor': False, 'customer': True, 'primaryType': 'customer', 'contactPerson': [{'emailAddress': all_data['email'], 'firstName': all_data['fn'], 'lastName': all_data['ln'], 'primeFlag': 1}], 'pan': None, 'creditLimit': None, 'email': None, 'phone': None, 'mobile': all_data['ph'], 'skype': None, 'website': None, 'address': [{'addressGSTIN': all_data['note'], 'note': None, 'address1': all_data['address1'], 'address2': all_data['address2'], 'street': None, 'city': all_data['city'], 'state': all_data['province'], 'zip':  all_data['zip'], 'country':all_data['cont'], 'mobile': all_data['ph'], 'pan': None, 'tan': None, 'gstin': None, 'cin': None, 'telephone': None, 'type': 'PADR'}], 'contactGstin': [{'number':  all_data['note'], 'note': None, 'verified': False, 'billingAddress': {
                        'addressGSTIN':  all_data['note'], 'note':all_data['note'], 'address1': all_data['address1'], 'address2': all_data['address2'], 'street': None, 'city': all_data['city'], 'state': all_data['province'], 'zip': all_data['zip'], 'country':  all_data['cont'], 'mobile': None, 'pan': None, 'tan': None, 'gstin': None, 'cin': None, 'telephone': None, 'type': 'BADR'}, 'shippingAddress': {'addressGSTIN': all_data['note'], 'note':all_data['note'], 'address1': all_data['address1'], 'address2': all_data['address2'], 'street': None, 'city': all_data['city'], 'state': all_data['province'], 'zip': all_data['zip'], 'country':  all_data['cont'], 'mobile': all_data['ph'], 'pan': None, 'tan': None, 'gstin': None, 'cin': None, 'telephone': None, 'type': 'SADR'}, 'defaultGstin': True}], 'openingBalance': 0, 'openingDate': None, 'notes': None, 'termsAndCondition': None, 'status': 'COAC', 'cinNumber': None, 'panVerified': False, 'fax': None}]}

                    if (note == ""):
                        add_item = add_item2
                    else:
                        add_item = add_item1
                    # ------------------------- Check In GST End  ---------------------------

                    r = requests.post(acc_txn_url, json=add_item,  headers=url_header)
                    print(r.json())
                    print('-----------------')
                    print(add_item)
                    print('-----------------')

                    if (r.json()['fieldErrors'] == None):
                        res2 = "Done"
                    else:
                        res2 = r.json()['fieldErrors'][0]['message']

                    if (r.json()['status'] == 200):
                        statusmsg = "SUCCESS"
                        suc += 1
                    else:
                        statusmsg = "FAILED"
                        fail += 1
                    status = statusmsg
                    remark = res2
                    customer_name = all_data['fn']+" " + all_data['ln']
                    state = all_data['province']
                    mobile = all_data['ph']
                    email = all_data['email']
                    code = all_data['id']
                    module_type = "Customers"
                    b = Customer(compid=compid, customer_name=customer_name, state=state, mobile=mobile, email=email,
                                 status=status, remark=remark, batch=batch, code=code, module_type=module_type, storecode=storecode)
                    b.save(using="shopifytb")
                else:
                    fail += 1
                    status = "FAILED"
                    remark = "State is Disabled"
                    customer_name = "Null"
                    state = "Null"
                    mobile = ph
                    email = email
                    code = id1
                    module_type = "Customers"
                    b = Customer(compid=compid, customer_name=customer_name, state=state, mobile=mobile, email=email,
                                 status=status, remark=remark, batch=batch, code=code, module_type=module_type, storecode=storecode)
                    b.save(using="shopifytb")
                # State check is Disabled or Enabled End
            modulesync = "Customers"
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d" +
                                 "T"+"%H"+":"+"%M"+":"+"%S")
            tot = suc+fail
            totalrecordscus = tot
            successcus = suc
            failcus = fail
            status1 = ""
            if failcus == 0:
                status1 = "SUCCESS"
            elif successcus == 0:
                status1 = "FAILED"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode)
            c.save(using="shopifytb")
            res1 = r.json()['message']
            print("Try --------")
            print("--- %s seconds ---" % (time.time() - start_time))
            if res1 == "Batch Data Added successfully":
                return Response("SYNC CUSTOMERS SUCCESSFULLY......")
            else:
                return Response("SYNC CUSTOMERS FAILED !!!!!!!")
        except:
            modulesync = "Customers"
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d" +
                                 "T"+"%H"+":"+"%M"+":"+"%S")
            tot = suc+fail
            totalrecordscus = tot
            successcus = suc
            failcus = fail
            status1 = ""
            if failcus == 0:
                status1 = "SUCCESS"
            elif successcus == 0:
                status1 = "FAILED"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode)
            c.save(using="shopifytb")
            print("--- %s seconds ---" % (time.time() - start_time))
            return Response("SYNC CUSTOMERS FAILED !!!!!!!")
# ----------------SynItem (CustomerSync) End--------------------------------


# ----------------------- Sync invoice -------------------------------------
@api_view(['GET', 'POST'])
def syncInvoice(request, **kwargs):
    sucinv = 0
    failinv = 0
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            print("comid in invoice===", compid)
            storecod = request.GET.get("storecode")
            sales = Sales.objects.using("shopifytb").filter(
                compid=compid, storecode=storecod).all()
            rec_json = serializers.serialize('json', sales)
            return HttpResponse(rec_json, content_type='application/json')

        except:
            return HttpResponse("COULDN'T FETCH RECORDS !!!!")
    if request.method == "POST":
        compid = request.data['compid']
        print("comid in Invoicepost ----------------", compid)
        try:
            token1 = request.data['token']
            storename = request.data['storename']
            stage = request.data["stage"]
            gstin = request.data['gstin']
            branch = request.data['branch']
            storecode = request.data['storecode']
            ccode = request.data["ccode"]
            ccodepre = request.data["ccodepre"]
            if (request.data['invoicetime'] == "firsttime"):
                lastsyncinvoice = request.data['datetime1']
            else:
                lastsyncinvoice = request.data['invoicetime']
            lstinvoice = "2014-04-25T16:15:47-04:07"
            
            compid, preservekey = request.data["compid"], request.data["preservekey"]
            login = Accounting.Accounting_login(preservekey, compid)
            compid, preservekey, valuetoken = (login["compid"], login["preservekey"],login["token"])
            

            # ---------------------- Accounting Login -----------------------------------------
            url = "https://%s.myshopify.com/admin/api/2022-07/orders.json?status=any&created_at_min=%s" % (
                storename, lstinvoice)
            print(url)
            # url = "https://%s.myshopify.com/admin/api/2022-07/orders.json?status=any/" % (storename)
            headers = {
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": token1
            }
            r = requests.get(url, headers=headers)
            invoice = r.json()
            # ---------------------------------- Post Data On Accounting------------------------------------
            url_header = {
                "Content-Type": "application/json",
                "x-auth-token": valuetoken,
                "x-preserveKey": preservekey,
                "x-company": compid,
            }
            start_time = time.time()
            loopvar = invoice["orders"]
            tot1 = len(loopvar)
            now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            batch = ('HB/'+now.strftime("%d""%m""%y""%H""%M""%S"))
            # Stage ----------------------
            if stage == "Draft":
                statusinv = "INDT"
            elif stage == "Approve":
                statusinv = "INAP"
            else:
                statusinv = "INPN"

            invoicedata = {}
            for val in loopvar:
                currency1 = val["current_subtotal_price_set"]['shop_money']['currency_code']
                odnum = val['order_number']
                print("val['order_number'].............", val['id'])

                cdate = val['created_at']

                if (val['payment_terms'] != None):
                    dueDate = val['payment_terms']['payment_schedules'][0]['due_at']
                else:
                    dueDate = None

                # Changes ----------------
                category = val["financial_status"]
                if val["financial_status"] == "paid":
                    contactCode = ccodepre
                else:
                    contactCode = ccode

                gstnote = val['customer']['note']
                if (gstnote != None):
                    gstnote1 = gstnote[-15:]
                    gstntype = "B2B"
                    invoicetype = "R"
                else:
                    gstnote1 = None
                    gstntype = "B2C"
                    invoicetype = "NA"

                if val['billing_address']["province"] != None:
                    state = val['billing_address']["province"]
                elif val["customer"]['default_address']["province"] != None:
                    state = val["customer"]['default_address']["province"]
                else:
                    state = "Null"

                if val['billing_address']["zip"] != None:
                    Zip = val['billing_address']["zip"]
                elif val["customer"]['default_address']["zip"] != None:
                    Zip = val["customer"]['default_address']["zip"]
                else:
                    Zip = "Null"
                print("Zip -----------------------------------------------", Zip)

                if val['billing_address']["country"] != None:
                    country1 = val['billing_address']["country"]
                elif val["customer"]['default_address']["country"] != None:
                    country1 = val["customer"]['default_address']["country"]
                else:
                    country1 = "Null"
                print("country1 ---------------------------------------------", country1)

                if val['billing_address']['address1'] != None:
                    add1 = val['billing_address']['address1']
                elif val["customer"]['default_address']['address1'] != None:
                    add1 = val["customer"]['default_address']['address1']
                else:
                    add1 = "Null"
                print("add1 -----------------------------------------------", add1)

                if val['billing_address']['address2'] != None:
                    add2 = val['billing_address']['address2']
                elif val["customer"]['default_address']['address2'] != None:
                    add2 = val["customer"]['default_address']['address2']
                else:
                    add2 = "Null"
                print("add2 -----------------------------------------------", add2)

                if val['billing_address']['city'] != None:
                    city = val['billing_address']['city']
                elif val["customer"]['default_address']['city'] != None:
                    city = val["customer"]['default_address']['city']
                else:
                    city = "Null"
                print("City -----------------------------------------------", city)

                bill_address = (add1+" "+add2)
                print("Bill_address -----------------------", bill_address)

                if (val['shipping_address']["address1"] == None):
                    shipadd1 = "Null"
                else:
                    shipadd1 = val['shipping_address']["address1"]

                if (val['shipping_address']["address2"] == None):
                    shipadd2 = "Null"
                else:
                    shipadd2 = val['shipping_address']["address2"]

                shipp_address = shipadd1 + " "+shipadd2

                print("Ship address ------------------------", shipp_address)

                if val['shipping_address']["city"] == None:
                    shipp_city = "Null"
                else:
                    shipp_city = val['shipping_address']["city"]

                print("Ship City ------------------------", shipp_city)

                if val['shipping_address']["province"] != None:
                    shipp_state = val['shipping_address']["province"]
                elif val["customer"]['default_address']["province"] != None:
                    shipp_state = val["customer"]['default_address']["province"]
                else:
                    shipp_state = "Null"

                if val['shipping_address']["zip"] != None:
                    shipp_zip = val['shipping_address']["zip"]
                elif val["customer"]['default_address']["zip"] != None:
                    shipp_zip = val["customer"]['default_address']["zip"]
                else:
                    shipp_zip = "Null"

                if val['shipping_address']["country"] != None:
                    shipp_country = val['shipping_address']["country"]
                elif val["customer"]['default_address']["country"] != None:
                    shipp_country = val["customer"]['default_address']["country"]
                else:
                    shipp_country = "Null"

                print("Shipping Country ----------------", shipp_country)

                total_price = val['total_price']
                lineitem_var = val['line_items']

                line_itemlength = len(lineitem_var)
                final_item_list = []
                for ele in lineitem_var:
                    item_code = ele['product_id']
                    finaldiscount1 = float(0)
                    finaldiscountadd = float(0)
                    finalqty = float(ele['quantity'])
                    lendis = len(ele['discount_allocations'])
                    if lendis == 2:
                        finaldiscount1 = float(
                            ele['discount_allocations'][0]['amount'])
                        finaldiscount1 = finaldiscount1/finalqty
                        finaldiscountadd = float(
                            ele['discount_allocations'][1]['amount'])
                        finaldiscountadd = finaldiscountadd/finalqty
                    elif lendis == 1:
                        finaldiscount1 = float(
                            ele['discount_allocations'][0]['amount'])
                        finaldiscount1 = finaldiscount1/finalqty
                        finaldiscountadd = float(0)
                    else:
                        finaldiscount1 = 0
                        finaldiscountadd = 0.00
                    attoption = []

                    print("ele['variant_title']..........",
                          ele['variant_title'])
                    if (ele['variant_title'] != "" or ele['variant_title'] != None):
                        aatvar = (ele['variant_title'].replace(
                            " ", "")).split('/')
                        norobj = {"attributeOptionName": aatvar[0]}
                        attoption.append(norobj)
                        if (len(aatvar) == 2):
                            colobj = {"attributeOptionName": aatvar[1]}
                            attoption.append(colobj)
                    else:
                        pass
                    print("attoption.............", attoption)

                    freightUnit = val['total_shipping_price_set']['shop_money']['amount']
                    item_dict = {
                        "saleType": "Normal",
                        "inventoryType": "INVTP",
                        "itemCode": val['line_items'][0]['sku'],
                        "itemName": ele['title'],
                        "txnQtyAllocationData": {
                            "txnQtyAllocationList": [
                                    {
                                        # "batchNo": None,
                                        "quantityAttribute": {
                                            "inventoryQuantityAttributeOptionList": attoption
                                        },
                                        # "quantitySerial": None,
                                        "quantity": ele['quantity'],
                                        "unitPrice":ele['price'],
                                    }
                            ]
                        },
                        # Changes ------------------
                        "description": "",
                        # "gstRate": gstrate,
                        # Changes -------------------
                        "freightUnit": float(freightUnit)/line_itemlength,
                        "discount": finaldiscount1,
                        "addDiscount": round(finaldiscountadd, 0),
                        "hsnSac": None,
                        "type": "Goods",
                        # "unitName": None,
                        "accountName": "Sale of Goods",
                        "fetchAuto": "True"
                    }
                    final_item_list.append(item_dict)
                    item_code = val['line_items'][0]
                    item_title = val['line_items'][0]['title']
                    item_variant = val['line_items'][0]['variant_title']
                    item_quantity = val['line_items'][0]['quantity']
                    item_price = val['line_items'][0]['price']
                    items = val['line_items'][0]['tax_lines']

                    invoicedata = {"currencyCode": currency1, "number": odnum, "date": cdate, "dueDate": dueDate, "contactCode": contactCode, "customerGstin": gstnote1, "placeSupplyName": state, "address1": bill_address, "city": city, "state": state, "zip": Zip, "country": country1, "shipaddress1": shipp_address,
                                   "city1": shipp_city, "state1": shipp_state, "zip1": shipp_zip, "country1": shipp_country, "totalamount":   total_price, "itemCode": item_code, "itemName": item_title, "attributeOptionName": item_variant, "quantity":  item_quantity, "unitPrice": item_price, "taxlines": items, "line_items_list": final_item_list}

                if (dueDate != None):
                    du = invoicedata['dueDate']
                    x = du.split('T')[0].split('-')
                    pdate = x[2]+"-"+x[1]+"-"+x[0]
                else:
                    date = invoicedata['date']
                    date_1 = dt.datetime.strptime(
                        date.split("T")[0], "%Y-%m-%d")
                    end_date = date_1 + timedelta(days=10)
                    date_2 = end_date.strftime("%d-%m-%Y")
                    pdate = date_2

                ddate = invoicedata['date']
                y = ddate.split('T')[0].split('-')
                odate = y[2]+"-"+y[1]+"-"+y[0]
                shipOrderTime = cdate.split("T")[1][:8]
                add_item = {"invoiceList": [
                    {
                        "taxType": "ITAX",
                        "currencyCode": invoicedata['currencyCode'],
                        "companyGstin":gstin,
                        "branch":branch,
                        "Category":category,
                        "invoiceType":invoicetype,
                        "number":invoicedata['number'],
                        "date":odate,
                        "dueDate":pdate,
                        "contactCode":invoicedata['contactCode'],
                        "contactName":"",
                        # "contactName":"PRIYANKA ENTERPRISES",
                        "customerGstin":invoicedata['customerGstin'],
                        "placeSupplyName":invoicedata['placeSupplyName'],
                        "billAddress":{
                            "address1": invoicedata['address1'],
                            "city":invoicedata['city'],
                            "state":invoicedata['state'],
                            "zip":invoicedata['zip'],
                            "country":invoicedata['country'],
                            "pan":"",
                            "gstin":"",
                            "type":"BADR"
                        },

                        "shipAddress": {
                            "address1": invoicedata['shipaddress1'],
                            "city":invoicedata['city1'],
                            "state":invoicedata['state1'],
                            "zip":invoicedata['zip1'],
                            "country":invoicedata['country1'],
                            "pan":"",
                            "gstin":"",
                            "type":" SADR "
                        },
                        "warehouseAddress":None,
                        "termCondition":None,
                        "customersNotes":None,
                        "shippingNumber":None,
                        "shippingDate":None,
                        "shippingPortCode":None,
                        "purchaseOrderNumber":None,
                        "purchaseOrderDate":None,
                        "buyerOrderNumber":None,
                        "buyerOrderDate":None,
                        "eWayBillNumber":None,
                        "eWayBillDate":None,
                        "lRNo":None,
                        "otherReference":None,
                        "vendorCode":None,
                        "vehicleNumber":None,
                        "termsOfPayment":None,
                        "cin":None,
                        # changes------------------
                        "amount":invoicedata['totalamount'],
                        "roundingAmount":0,
                        "reverseChargeFlag":False,
                        "flatDiscountFlag":True,
                        "flatAddDiscountFlag":True,
                        "flatCessFlag":False,
                        "flatSubsidyFlag":False,
                        "txnDiscountList":None,
                        "lineItems": invoicedata['line_items_list'],
                        "typeCode": "SINV",
                        # apporve case
                        "status": statusinv,
                        "gstnType": gstntype,
                        # Changes---------------------
                        "shipBillingName":val['billing_address']['name'],
                        "shipCustomerId":val['customer']['id'],
                        "shipName":val['shipping_address']['name'],
                        "shipOrderTime":shipOrderTime,
                        "shipPaymentType":contactCode,
                        "shipPaymentId":val['reference'],
                        "shipPgId":val['payment_gateway_names'][0],
                        "shipTokenId":val['token'],
                        "shipOrderSource":"Shopify",
                    }
                ]
                }

                print("-----------------Post Data Started-----------------------")
                r = requests.post(acc_txn_url, json=add_item,  headers=url_header)
                print(r.json(), "\n")
                print(add_item)
                res1 = r.json()['message']
                if (r.json()['fieldErrors'] == None):
                    res2 = "Done"
                else:
                    res2 = r.json()['fieldErrors'][0]['message']
                if (r.json()['status'] == 200):
                    statusmsg = "SUCCESS"
                    sucinv += 1
                else:
                    statusmsg = "FAILED"
                    failinv += 1
                status = statusmsg
                remark = res2
                module_type = "Sales Invoice"
                invoice_no = invoicedata['number']
                amount = invoicedata['totalamount']
                date = odate
                customer = invoicedata['contactCode']
                dc = Sales(compid=compid, invoice_no=invoice_no, amount=amount, date=date, batch=batch,
                           remark=remark, status=status, customer_name=customer, module_type=module_type, storecode=storecode, postjson=add_item)
                dc.save(using="shopifytb")
            modulesync = "Sales Invoice"
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d" +
                                 "T"+"%H"+":"+"%M"+":"+"%S")
            totalrecordscus = tot1
            successcus = sucinv
            failcus = failinv
            status1 = ""
            if failcus == 0:
                status1 = "SUCCESS"
            elif successcus == 0:
                status1 = "FAILED"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode, recordjson=loopvar)
            c.save(using="shopifytb")
            res1 = r.json()['message']
            print("Invoice Time --- %s seconds ---" %
                  (time.time() - start_time))
            if res1 == "Batch Data Added successfully":
                return Response("SYNC INVOICE SUCCESSFULLY...")
            else:
                return Response("SYNC INVOICE FAILED !!!")
        except:
            modulesync = "Sales Invoice"
            cdate = now.strftime("%Y"+"-"+"%m"+"-"+"%d" +
                                 "T"+"%H"+":"+"%M"+":"+"%S")
            totalrecordscus = tot1
            successcus = sucinv
            failcus = failinv
            status1 = ""
            if failcus == 0:
                status1 = "SUCCESS"
            elif successcus == 0:
                status1 = "FAILED"
            else:
                status1 = "PARTIALLY"+" "+"SUCCESS"
            c = Sync(compid=compid, batch=batch, module_type=modulesync, date=cdate, status=status1,
                     total_record=totalrecordscus, success_record=successcus, fail_record=failcus, storecode=storecode, recordjson=loopvar)
            c.save(using="shopifytb")
            return Response("SYNC INVOICE FAILED !!!")

# -----------------------Sync End Sales Invoice ----------------------------
