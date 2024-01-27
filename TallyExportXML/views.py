from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import requests
from . import Accounting
import json
from  . models import Contact,TransactionList
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import xmltodict
import datetime as dt


# --------------------- Accounting log in Live/Sandbox -------------------------------

# All New urls for sandbox and local use
branch = "https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url = "https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url = "https://booksapi.hostbooks.in/hostbook/api/master/add"

# All urls for live server
# branch = "https://in2accounts.hostbooks.com/api/master/list"
# acc_txn_url = "https://in2accounts.hostbooks.com/api/transaction/add"
# acc_mas_url = "https://in2accounts.hostbooks.com/api/master/add"


# ----------- Branch API ------------
@api_view(["GET", "POST"])
def branchlist(request, **kwargs):
    if request.method == "GET":
        try:
            return Response("branchapi get request in try")
        except:
            return HttpResponse("branchapi get request in except")

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
            print("Branches---->", res_branch)

            payload = json.dumps({"page": 1, "limit": 500, "entityType": "CATEGORY"})
            headers = {
                "x-auth-token": valuetoken,
                "x-preserveKey": preserve,
                "x-company": compid,
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, data=payload)
            res_cat = response.json()

            # print("Categories---->", res_cat)

            data_branch = []
            for x in res_branch["data"]["master"]["list"]:
                print("\nbranch is--------------------------------", x)
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
            print("CostCenter code ----", len(costcode))

            return Response(
                {
                    "Branch": data_branch,
                    "Category": data_cat,
                    "costCenter": costcode["data"]["master"]["list"],
                }
            )
        except:
            return Response(
                "please fill all the required fields in your Branches and Categories"
            )

# ----------- Branch API ------------


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


# ------------- Sync Ledger HB Accounting  to Tally ------------
@api_view(["GET", "POST"])
def SyncLedgerHBtotally(request, **kwargs):
    if request.method == "GET":
        # data=tallyXMLdata(xmldata=xml_string).values()
        return Response("GET")
    if request.method == "POST":
        print("request data ----------->", request.data)
        compid, preserve = request.data["compid"], request.data["preservekey"]
        login = Accounting.Accounting_login(preserve, compid)
        print(login)
        compid, preserve, valuetoken = (
            login["compid"],
            login["preservekey"],
            login["token"],
        )
        acode = []
        header3 = {
            "x-preserveKey": preserve,
            "x-company": compid,
            "Content-Type": "application/json",
            "x-auth-token": valuetoken,
        }
        body2 = {"entityType": "ACCT", "page": 1, "limit": 500}
        acresponse = requests.post(branch, headers=header3, json=body2)
        acode = acresponse.json()
        # print("Accounting data ------->",acode['data']['master']['list'])

        # Create the root element
        root = ET.Element("ENVELOPE")
        # Create the HEADER element
        header = ET.SubElement(root, "HEADER")
        # Create and add elements inside HEADER
        tally_request = ET.SubElement(header, "TALLYREQUEST")
        tally_request.text = "IMPORT DATA"
        type_element = ET.SubElement(header, "TYPE")
        type_element.text = "Collection"
        id_element = ET.SubElement(header, "ID")
        id_element.text = "Ledgers"
        # Create the BODY element
        body = ET.SubElement(root, "BODY")
        # Create the IMPORTDATA element
        import_data = ET.SubElement(body, "IMPORTDATA")
        # Create the REQUESTDESC element
        request_desc = ET.SubElement(import_data, "REQUESTDESC")
        # Create and add elements inside REQUESTDESC
        report_name = ET.SubElement(request_desc, "REPORTNAME")
        report_name.text = "All Masters"
        # Create the REQUESTDATA element
        request_data = ET.SubElement(import_data, "REQUESTDATA")

        # Create and add TALLYMESSAGE elements
        def create_tally_message(name, parent):
            # print('Name-------->',name)
            # print('\nparent-------->',parent)
            tally_message = ET.Element("TALLYMESSAGE", xmlns="TallyUDF")
            group = ET.SubElement(tally_message, "LEDGER")
            group_name = ET.SubElement(group, "NAME")
            group_name.text = name
            group_parent = ET.SubElement(group, "PARENT")
            group_parent.text = parent
            return tally_message

        tally_messages = []
        for i in acode["data"]["master"]["list"]:
            # print("data coming------>",i["name"],i["parentGroup"]['name'])
            tally_messages.append(
                create_tally_message(i["name"], i["parentGroup"]["name"])
            )

        # Add TALLYMESSAGE elements to REQUESTDATA
        for tally_message in tally_messages:
            # print("tally message ------>",tally_message)
            request_data.append(tally_message)
        xml_data = ET.tostring(root, encoding="unicode")
        print("Xml_Data------------->", xml_data)
        return Response(xml_data)

# ------------- Sync Ledger HB Accounting  to Tally ------------

# ------------- Sync Transaction HB Accounting  to Tally ------------
@api_view(["GET", "POST"])
def SyncTransactionHBtotally(request, **kwargs):
    if request.method == "GET":
        # data=tallyXMLdata(xmldata=xml_string).values()
        return Response("GET")

    if request.method == "POST":
        print("request data ----------->", request.data)
        stdate1 = request.data["startdate"].split("-")[::-1]
        endate1 = request.data["enddate"].split("-")[::-1]
        sd = "-".join(stdate1)
        ed = "-".join(endate1)
        compid, preserve = request.data["compid"], request.data["preservekey"]
        login = Accounting.Accounting_login(preserve, compid)
        print(login)
        compid, preserve, valuetoken = (
            login["compid"],
            login["preservekey"],
            login["token"],
        )
        jv = "https://booksapi.hostbooks.in/hostbook/api/reports"
        header3 = {
            "x-preserveKey": preserve,
            "x-company": compid,
            "Content-Type": "application/json",
            "x-auth-token": valuetoken,
        }
        jvheader = {
            "reportName": "JOURNAL_REPORT",
            "startDate": sd,
            "endDate": ed,
            "page": 1,
            "limit": 500,
        }
        # response = requests.post(transurl, headers=header3, json=body2)
        response = requests.post(jv, headers=header3, json=jvheader)
        jvresponse = response.json()
        print(
            "\n \nAccounting data ------->", len(jvresponse["data"]["report"]["list"])
        )
        if len(jvresponse["data"]["report"]["list"]) > 0:
            print("\n if-------------------------------")
            jvtrans = jvresponse["data"]["report"]["list"]
            timestamp_ms = jvresponse["data"]["report"]["list"][0]["date"]
            timestamp_sec = timestamp_ms / 1000
            date_obj = datetime.datetime.fromtimestamp(timestamp_sec)
            formate_date = date_obj.strftime("%Y%m%d")
            print("\n date ------>", formate_date)
        else:
            print("\n Data not Found-------------------------------")
            return Response("Data not Found")
        root = ET.Element("ENVELOPE")
        header = ET.SubElement(root, "HEADER")
        tally_request = ET.SubElement(header, "TALLYREQUEST")
        tally_request.text = "Import Data"
        body = ET.SubElement(root, "BODY")
        import_data = ET.SubElement(body, "IMPORTDATA")
        request_desc = ET.SubElement(import_data, "REQUESTDESC")
        report_name = ET.SubElement(request_desc, "REPORTNAME")
        report_name.text = "All Masters"
        request_data = ET.SubElement(import_data, "REQUESTDATA")
        tally_message = ET.SubElement(
            request_data, "TALLYMESSAGE", attrib={"xmlns:UDF": "TallyUDF"}
        )
        for item in jvtrans:
            print("voucher number---------------", item["txnNumber"])
            voucher = ET.SubElement(tally_message, "VOUCHER")
            date = ET.SubElement(voucher, "DATE")
            date.text = str(formate_date)
            narration = ET.SubElement(voucher, "NARRATION")
            narration.text = item["txnAccountPostings"][0]["description"]
            voucher_type_name = ET.SubElement(voucher, "VOUCHERTYPENAME")
            voucher_type_name.text = "Journal"
            voucher_number = ET.SubElement(voucher, "VOUCHERNUMBER")
            voucher_number.text = item["txnNumber"]
            persisted_view = ET.SubElement(voucher, "PERSISTEDVIEW")
            persisted_view.text = "Accounting Voucher View"
            print(
                "\nitem txnAccountPostings-----------------------------------",
                item["txnAccountPostings"],
            )
            vouchers = []
            for i in item["txnAccountPostings"]:
                # print("\nin for loop--------",i)
                if float(i["creditAmount"]) > 0:
                    print("\nin credit", i["creditAmount"])
                    dem = "No"
                    amount = float(i["creditAmount"])
                    ledger_entry1 = ET.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
                    ledger_name1 = ET.SubElement(ledger_entry1, "LEDGERNAME")
                    ledger_name1.text = i["accounts"]["name"]
                    is_deemed_positive1 = ET.SubElement(
                        ledger_entry1, "ISDEEMEDPOSITIVE"
                    )
                    is_deemed_positive1.text = dem
                    amount1 = ET.SubElement(ledger_entry1, "AMOUNT")
                    amount1.text = str(amount)
                    vat_exp_amount1 = ET.SubElement(ledger_entry1, "VATEXPAMOUNT")
                    vat_exp_amount1.text = str(amount)
                    vouchers.append(ledger_entry1)
                if float(i["debitAmount"]) > 0:
                    print("\nin debit", i["debitAmount"])
                    dem = "Yes"
                    amount = -float(i["debitAmount"])
                    ledger_entry1 = ET.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
                    ledger_name1 = ET.SubElement(ledger_entry1, "LEDGERNAME")
                    ledger_name1.text = i["accounts"]["name"]
                    is_deemed_positive1 = ET.SubElement(
                        ledger_entry1, "ISDEEMEDPOSITIVE"
                    )
                    is_deemed_positive1.text = dem
                    amount1 = ET.SubElement(ledger_entry1, "AMOUNT")
                    amount1.text = str(amount)
                    vat_exp_amount1 = ET.SubElement(ledger_entry1, "VATEXPAMOUNT")
                    vat_exp_amount1.text = str(amount)
                    vouchers.append(ledger_entry1)
        xml_data = ET.tostring(root, encoding="unicode")
        print("xml_data--------->", xml_data)
    return Response(xml_data)

# ------------- Sync Transaction HB Accounting  to Tally ------------


# ----------- Sync ledger tally to HB Accounting --------------
@api_view(["GET", "POST"])
def SyncLedgerTallytoHB(request, *args, **kwargs):
    if request.method=="GET":
        try: 
            compid=request.GET.get('compid')
            print("Compid is and branch---------------",compid)            
            data=Contact.objects.using('tallyexport').filter(compid=compid).values("name","id","date","status","remark",).order_by('-id')
            return Response(data)
        except:
            return Response("Sync Ledger Failed")

    if request.method == "POST":
        try:
            # print("Request data ------>",request.data)
            data = request.data["xmldata"]
            xmldata1 = xmltodict.parse(data)
            jsondata = json.dumps(xmldata1, indent=2)
            xmldata = json.loads(jsondata)
            nowc = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            date = nowc.strftime("%Y" + "-" + "%m" + "-" + "%d" + " " + "%H" + ":" + "%M" + ":" + "%S.%f")

            compid, preserve = ( request.data["logindata"]["compid"],request.data["logindata"]["preservekey"])
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = ( login["compid"],login["preservekey"],login["token"])
            root = xmldata["ENVELOPE"]["LEDGERLIST"]["LEDGER"]
            count = 0
            for data in root:
                count += 1
                add_item = {
                    "contactList": [
                        {
                            "name": data["LEDNAME"],
                            "accountNumber": data["LEDNAME"],
                            "customer": True,
                            "primaryType": "customer",
                            # "pan": "AATFV1949G", #
                            # "creditLimit": None,
                            # "email": None,
                            # "phone": None,
                            # "mobile": "8888888888",
                            "address": [
                                {
                                    "address1": data["LEDADDRESS"],
                                    "address2": "",
                                    # "street": None,
                                    # "city": "Hyderabad City",
                                    # "state": "TELANGANA",
                                    # "zip": "500081",
                                    "country": "INDIA",
                                    "type": "PADR",
                                }
                            ],
                            "status": "COAC",
                            "panVerified": False,
                        }
                    ]
                }
                headers = {
                    "x-auth-token": valuetoken,
                    "x-preserveKey": preserve,
                    "x-company": compid,
                    "Content-Type": "application/json",
                }
                print("\n \n Count ------>", count, "\n \n Add Items ------->", add_item)

                r = requests.post(acc_mas_url, json=add_item, headers=headers)
                res = r.json()
                print("\n\nAccounting Response ------->", res)
                if (res["message"] == "Batch Data Added successfully" or res["status"] == 200):
                    message = "Done"
                    data = Contact(name=data["LEDNAME"],status="SUCCESS",responsedata=add_item,remark=message,date=date,compid=compid)
                    data.save(using="tallyexport")
                else:
                    if "fieldErrors" in res:
                        fielderror = res["fieldErrors"]
                        message = ""
                        for l in fielderror:
                            message += l["message"]
                    else:
                        message = str(res["errorList"].values())
                    # Data Save
                    data = Contact(name=data["LEDNAME"],status="FAILED",responsedata=add_item,remark=message,date=date,compid=compid)
                    data.save(using="tallyexport")
            if res["message"] == "Batch Data Added successfully":
                return Response("Sync Ledger Successfully")
            else:
                return Response("Sync Ledger  Failed")
        except:
            return Response("Sync Ledger Failed")

# ----------- Sync ledger tally to HB Accounting --------------


# ----------- Sync Transactions tall to HB Accounting --------------
@api_view(["GET", "POST"])
def SyncTransactionTallytoHB(request, *args, **kwargs):
    if request.method=="GET":
        try: 
            compid=request.GET.get('compid')
            print("Compid is and branch---------------",compid)            
            data=TransactionList.objects.using("tallyexport").filter(compid=compid).values("amount","id","date","status","voucherno","remark",).order_by('-id')
            return Response(data)
        except:
            return Response("Sync Transaction Failed")
        
    if request.method == "POST":
        try:
            # Get the token from TALLY
            print("\n \n Request data ------>", request.data)
            data = request.data["xmldata"]
            xmldata1 = xmltodict.parse(data)
            jsondata = json.dumps(xmldata1, indent=2)
            xmldata = json.loads(jsondata)
            compid, preserve = ( request.data["logindata"]["compid"],request.data["logindata"]["preservekey"])
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = ( login["compid"],login["preservekey"],login["token"])
            print("\n \n XML Data is =---------->", xmldata)

            for data1 in xmldata["ENVELOPE"]["VOUCHERLIST"]["VOUCHER"]:
                # print("\n \n Data is  ------->", data1)
                date= data1["DVCHDATE"]
                formatted_date1=datetime.strptime(date, "%d-%b-%Y")
                formatted_date=formatted_date1.strftime("%d-%m-%Y")
                print("\n formatted_date ----->",formatted_date)
                narr=data1["DVCHNARR"]
                ledname=data1["MYLEDNAME"]
                ledamount=data1["MYLEDAMOUNT"]
                ledtype=data1["MYLEDDEMPOS"]
                arr=zip(ledname,ledamount,ledtype)
                mjdata=[]
                debitAmount=0
                creditAmount=0
                for i in arr:
                    # print("\n Arr is ------->",i)
                    if "Yes" in i:
                        oneitem ={
                            "accountName": i[0],
                            "debitAmount": float(i[1].replace(",","")), 
                        }
                        debitAmount += float(i[1].replace(",",""))
                    else:
                        oneitem ={
                            "accountName": i[0],
                            "creditAmount": float(i[1].replace(",",""))
                        }
                        creditAmount += float(i[1].replace(",",""))
                    mjdata.append(oneitem)
                
                # print("\n Mjdata is ------>",mjdata)
                print("\n debitAmount is ------>",debitAmount)
                print("\n creditAmount is ------>",creditAmount)
                add_item = {
                    "journalList": [
                        {
                            "taxRateFlag": False,
                            "branch": "H.O",
                            "category": "Both",
                            "number": data1["DVOUCHERNUMBER"],  
                            # "autoNumberFlag":autonf,
                            "debitAmount": debitAmount, 
                            "creditAmount": creditAmount, 
                            # "companyGstin": request.data["gstin"], 
                            "manualJournalDetail":mjdata,
                            "narration": narr,
                            "reportflag": 1,
                            "autoReversingDate": None,
                            "date": formatted_date,  
                            "amount": 0,
                            "taxType": "NTAX",
                            "status": "MJPT",
                            "txnStatus": "TRPN",
                            "typeCode": "JMJ",
                        }
                    ]
                }
                print("\n Add items ------>",add_item)
                accountingurl = acc_txn_url
                headers = {
                    "x-auth-token": valuetoken,
                    "x-preserveKey":  preserve,
                    "x-company":  compid,
                    "Content-Type": "application/json"
                }
                r = requests.post(accountingurl, json=add_item, headers=headers)
                res = r.json()
                print("\n\nAccounting Response ----------->",res)
                if res['message'] == "Batch Data Added successfully":
                    print("\n-------IF--------- Batch Data Added successfully ",res['message'])
                    message="Done"
                    data=TransactionList(voucherno=data1["DVOUCHERNUMBER"],amount=debitAmount,status="SUCCESS",responsedata=add_item,remark=message,date=formatted_date,compid=compid)
                    data.save(using="tallyexport")
                else:
                    if "fieldErrors" in res:
                        fielderror=res['fieldErrors']
                        message=""
                        for l in fielderror:
                            message+=l['message']
                    else:
                        message=res['errorList'].values()
                    data=TransactionList(voucherno=data1["DVOUCHERNUMBER"],amount=debitAmount,status="FAILED",responsedata=add_item,remark=message,date=formatted_date,compid=compid)
                    data.save(using="tallyexport")

            if res["message"] == "Batch Data Added successfully":
                return Response("Sync Transaction Successfully")
            else:
                return Response("Sync Transaction Failed")    
        except Exception as e:
            return Response(f"Find error is :- {e}")

# ----------- Sync Transactions tally to HB Accounting --------------


@api_view(["GET", "POST"])
def getJsondata(request, *args, **kwargs):
    if request.method == "GET":
        id = request.GET.get("id")
        type1 = request.GET.get("type")
        print(" JSOn data ------------>", id, "\n", type1, "\n", type1)

        if type1 == "ledger":
            print("this is type value ----------->",type1)
            data1 = Contact.objects.using("tallyexport").filter(id=id).values("responsedata")
            print("\n\n json ------->", data1)
            return Response(data1)
        else:
            print("this is type value ----------->",type1)
            data1 = TransactionList.objects.using("tallyexport").filter(id=id).values("responsedata")
            print("\n\n json ------->", data1)
            return Response(data1)