from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import requests
import json
from .models import hotellogixlogin, syncmanualJournal, syncCreditList
from . import Accounting
from django.db.models import Q
from datetime import datetime, timedelta
import datetime



# --------------- All Sandbox and Local URLs. ---------------------
branch = "https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url = "https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url = "https://booksapi.hostbooks.in/hostbook/api/master/add"

# --------------- All Sandbox and Local URLs. ---------------------


# ----------------- All Live URLs. -----------------------
# branch="https://in2accounts.hostbooks.com/api/master/list"
# acc_txn_url="https://in2accounts.hostbooks.com/api/transaction/add"
# acc_mas_url="https://in2accounts.hostbooks.com/api/master/add"

# ----------------- All Live URLs. -----------------------

# --------- Login API -----------------
@api_view(['GET', 'POST', 'PUT'])
def login(request, **kwargs):
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            data = hotellogixlogin.objects.using('hotelogixexcel').filter(companyid=compid).values()
            return Response(data)
        except:
            return Response("hotellogix login get request in except")

    if request.method == "POST":
        try:
            print(request.data)
            branch = request.data['branch']
            mjseries = request.data['mjseries']
            category = request.data['category']
            sundryaccode=request.data['sundryaccode']
            gstin = request.data['gstin']
            state = request.data['state']
            saveas = request.data['saveas']
            city = request.data['city']
            zip = request.data['zip']
            address1 = request.data['address1']
            ledger_settings = request.data['ledger_settings']
            compid = request.data['compid']
            a = hotellogixlogin(branch=branch,mjseries=mjseries,category=category, gstin=gstin, state=state, saveas=saveas,
                                city=city, zip=zip, address1=address1, companyid=compid, ledger_settings=ledger_settings,sundryaccode=sundryaccode)
            a.save(using='hotelogixexcel')
            print("Hello-----")
            return Response("LOGIN SUCCESSFULLY")

        except:
            return Response("UNAUTHORIZED ACCESS")

    if request.method == "PUT":
        try:
            print(request.data)
            id = request.data['id']
            branch = request.data['branch']
            mjseries = request.data['mjseries']
            category = request.data['category']
            gstin = request.data['gstin']
            state = request.data['state']
            saveas = request.data['saveas']
            sundryaccode=request.data['sundryaccode']
            city = request.data['city']
            zip = request.data['zip']
            address1 = request.data['address1']
            ledger_settings = request.data['ledger_settings']
            compid = request.data['compid']

            a = hotellogixlogin.objects.using('hotelogixexcel').filter(id=id).update(branch=branch, mjseries=mjseries,category=category,sundryaccode=sundryaccode, gstin=gstin, state=state,
                                                             saveas=saveas, city=city, zip=zip, address1=address1, companyid=compid, ledger_settings=ledger_settings)

            return Response("Data update successfully")
        except:
            return Response("data update failed please fill data carefully")

# --------- Login API -----------------


# ----------- Branch API ------------
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

            # print("Categories---->", res_cat)

            data_branch = []
            for x in res_branch['data']['master']['list']:
                print("\nbranch is--------------------------------",x)
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
            print("CostCenter code ----", len(costcode))

            return Response({"Branch": data_branch, "Category": data_cat,"costCenter": costcode['data']['master']['list']})
        except:
            return Response("please fill all the required fields in your Branches and Categories")
# ----------- Branch API ------------


# ----------- Filter on AccountCode API -------------
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

# ----------- Filter on AccountCode API -------------



# ------------ Sync Manual Journal API ----------------
@api_view(['GET', 'POST','DELETE'])
def SyncManualJournal(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            branch=request.GET.get('branch')
            print("Compid is and branch---------------",compid,branch)
            data=syncmanualJournal.objects.using('hotelogixexcel').filter(compid=compid).values("id","date","creditAmount","debitAmount","Journalnumber","remark","Status").order_by('-id')
            print("data------",data)
            return Response(data)
        except:
            return Response("SyncManualJournal get request in except")

    if request.method == "POST":
        try:
            compid, preserve = request.data['compid'], request.data['preservekey']
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']
            logindata = request.data['loginData']
            exceldata = request.data['excelData']
            ledger_settings = logindata['ledger_settings']
            item_array = []
            date=exceldata[0]['Date']
            print("\nRequest data --------------",request.data)

            try:
                date_obj = datetime.datetime.strptime(date, "%d-%m-%y")
                formatted_date = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                try:
                    date_obj = datetime.datetime.strptime(date, "%d-%m-%Y")
                    formatted_date = date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    try:
                        date_obj = datetime.datetime.strptime(date, "%d/%m/%y")
                        formatted_date = date_obj.strftime("%d-%m-%Y")
                    except ValueError:
                        try:
                            date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
                            formatted_date = date_obj.strftime("%d-%m-%Y")
                        except ValueError:
                            return Response ("Date format is invalid")

            jv=formatted_date.split("-")
            jv1=jv[0]+jv[1]+jv[2]
            Journalnumber=logindata['branch']+" "+"JV" + str(jv1)
            print("\n jv ---------------------------------------",Journalnumber)

            mjseries=request.data["loginData"]["mjseries"]
            print("\n\n Mj series -------------->",mjseries)
        
            if mjseries=="Auto":
                autonf=True
                auto_no=""
            else:
                autonf=False
                auto_no=Journalnumber
            
            saveas1=logindata["saveas"]
            
            if saveas1=="Draft":
                savesstatus="MJDT"
            else:
                savesstatus="MJPT"
            print("\n Saveas data ------------->",saveas1)
        
            missl=[]
            for voucher in exceldata:
                if float(voucher['Credit Amount']) != 0:
                    for row in ledger_settings:
                        code = voucher['Dept & Revenue code']
                        acc_code = row['ledgerCode']
                        if acc_code == code:
                            code = row['ledgerName']
                            missl.append(voucher['Dept & Revenue code'])
                            break
                        else:
                            code = "Not Found"
                    oneitem = {
                        "description": voucher['Narration'],
                        "accountName": code,
                        "creditAmount": abs(float(voucher['Credit Amount']))
                    }
                    item_array.append(oneitem)
                if float(voucher['Debit Amount']) != 0:
                    for row in ledger_settings:
                        code = voucher['Dept & Revenue code']
                        acc_code = row['ledgerCode']
                        if acc_code == code:
                            code = row['ledgerName']
                            missl.append(voucher['Dept & Revenue code'])
                            break
                        else:
                            code = "Not Found"
                    oneitem = {
                        "description": voucher['Narration'],
                        "accountName": code,
                        "debitAmount": abs(float(voucher['Debit Amount']))
                    }
                    item_array.append(oneitem)

            # print(" ----------- Exit for loop")
            debitAmount=0
            creditAmount=0
            for data in item_array:
                if 'debitAmount' in data:
                    debitAmount+=data["debitAmount"]
                else:
                    creditAmount+=data["creditAmount"]
            print("Debit- and credit -----------------",debitAmount," ",creditAmount)
            add_item = {
                "journalList": [
                    {
                        "taxRateFlag": False,
                        "branch": logindata['branch'],
                        "category": logindata['category'],
                        "number": auto_no,
                        "autoNumberFlag":autonf,
                        "debitAmount": debitAmount,
                        "creditAmount": creditAmount,
                        "companyGstin": logindata['gstin'],
                        "manualJournalDetail":item_array,
                        "narration": exceldata[0]['Narration'],
                        "reportflag": 1,
                        "autoReversingDate": None,
                        "date": formatted_date,
                        "amount": 0,
                        "taxType": "NTAX",
                        "status": savesstatus,
                        "txnStatus": "TRPN",
                        "typeCode":"JMJ",
                    }
                ]
            }
            noMatchCode=0
            for j in item_array:
                if (j['accountName'] == "Not Found"):
                    print("\nthis ledger setting is missing-----------",j)
                    noMatchCode += 1
            if noMatchCode == 0:
                accountingurl = acc_txn_url
                headers = {
                    "x-auth-token": valuetoken,
                    "x-preserveKey":  preserve,
                    "x-company":  compid,
                    "Content-Type": "application/json"
                }
                print("Add itme -----------------",add_item)
                print("Headers -----------------",headers)
                r = requests.post(accountingurl, json=add_item, headers=headers)
                res = r.json()
                print(res)
                if res['message'] == "Batch Data Added successfully":
                    print(" ---------------- Batch Data Added successfully")
                    message="Done"
                    a=syncmanualJournal(Journalnumber=Journalnumber,date=formatted_date,Narration=exceldata[0]['Narration'],creditAmount=creditAmount,debitAmount=debitAmount,remark=message,Status="SUCCESS",compid=compid,Revenuename=exceldata[0]["Dept & Revenue code"],Revenuecode=exceldata[0]["Dept & Revenue Name"],jsondata=add_item)
                    a.save(using='hotelogixexcel')
                else:
                    if "fieldErrors" in res:
                        fielderror=res['fieldErrors']
                        message=""
                        for l in fielderror:
                            message+=l['message']
                    else:
                        message=res['errorList'].values()

                    a=syncmanualJournal(Journalnumber=Journalnumber,date=formatted_date,Narration=exceldata[0]['Narration'],creditAmount=creditAmount,debitAmount=debitAmount,remark=message,Status="FAILED",compid=compid,Revenuename=exceldata[0]["Dept & Revenue code"],Revenuecode=exceldata[0]["Dept & Revenue Name"],jsondata=add_item)
                    a.save(using='hotelogixexcel')
                    return Response(message)
                print("Response ----------------",res)
            else:
                print("/the error in ledger ---------------",missl)
                allledeger=[]
                for l in exceldata:
                    allledeger.append(l['Dept & Revenue code'])
                print("/the all in ledger ---------------",allledeger)
                l_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 
                non_match = l_func(missl,allledeger)

                missingres=f'Missing Ledger Setting in which the is Dept & Revenue code is {non_match}'

                message="Missing in Ledger setting"
                a=syncmanualJournal(Journalnumber=Journalnumber,date=formatted_date,Narration=exceldata[0]['Narration'],creditAmount=creditAmount,debitAmount=debitAmount,remark=missingres,Status="FAILED",compid=compid,Revenuename=exceldata[0]["Dept & Revenue code"],Revenuecode=exceldata[0]["Dept & Revenue Name"],jsondata=add_item)
                a.save(using='hotelogixexcel')

                return Response(missingres)
            
            return Response("SyncManualJournal Successfully !!!")
        except Exception as e:
            print("error is -----------------",e)
            return Response("SyncManualJournal Failed !!!")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=syncmanualJournal.objects.using('hotelogixexcel').filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Delete Failed !!!")
# ------------ Sync Manual Journal API ----------------



# -------------- Sync Credit List API ---------------
@api_view(['GET', 'POST','DELETE'])
def SyncCreditList(request, **kwargs):
    if request.method == "GET":
        try:
            compid=request.GET.get('compid')
            print("Compid is---------------",compid)
            data=syncCreditList.objects.using("hotelogixexcel").filter(compid=compid).values("id","number","date","billAmount","remark","Status").order_by('-id')
            return Response(data)
        except:
            return Response("SyncManualJournal get request in except")

    if request.method == "POST":
        try:
            compid, preserve = request.data['compid'], request.data['preservekey']
            login = Accounting.Accounting_login(preserve, compid)
            compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']
            logindata = request.data['loginData']
            exceldata = request.data['excelData']
            ledger_settings = logindata['ledger_settings']
            print("\n sync invoice start--------------")
            countnum=0
            sendBills=[]

            match1=[]
            nmatch1=[]
            mjseries=request.data["loginData"]["mjseries"]
            print("\n\n Mj series -------------->",mjseries)
            saveas1=logindata["saveas"]
            print("\n \n Saves type -------------------",saveas1)

            if saveas1=="Draft":
                savesstatusInv="INDT"
                savesstatusJv="MJDT"
            else:
                savesstatusInv="INAP"
                savesstatusJv="MJPT"
                
            for excel in exceldata:
                for ledger in ledger_settings:
                    if (excel['Account Code']==ledger['ledgerCode'] and excel['Account Name'] ==ledger['itdLedger']):
                        match1.append(excel['Account Name'])
                    else:
                        nmatch1.append(excel['Account Name'])

            l_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 
            non_match1 = l_func(match1,nmatch1)

            print("\n\n this is missing ledger settings-----",non_match1),

            if (len(non_match1)==0):
                for voucher in exceldata:
                    try:
                        if mjseries=="Auto":
                            autonf=True
                            auto_no=""
                            number=""
                        else:
                            autonf=False
                            auto_no=voucher['Bill No']
                            number=str(voucher['Bill No'])+"-"+ str(logindata["branch"])

                        print("\n\n autonf -->",autonf ,"\n auto_no -->",auto_no,"\n number -->",number)

                        if "zipCode" in voucher:
                            zipCode=voucher['zipCode']
                        else:
                            zipCode=""
                        # this code is for change date format
                        date2=voucher['Bill Date']
                        try:
                            date_obj = datetime.datetime.strptime(date2, "%d-%m-%y")
                            date = date_obj.strftime("%d-%m-%Y")
                        except ValueError:
                            try:
                                date_obj = datetime.datetime.strptime(date2, "%d-%m-%Y")
                                date = date_obj.strftime("%d-%m-%Y")
                            except ValueError:
                                try:
                                    date_obj = datetime.datetime.strptime(date2, "%d/%m/%y")
                                    date = date_obj.strftime("%d-%m-%Y")
                                except ValueError:
                                    try:
                                        date_obj = datetime.datetime.strptime(date2, "%d/%m/%Y")
                                        date = date_obj.strftime("%d-%m-%Y")
                                    except ValueError:
                                        return Response ("Date format is invalid")

                        # this code for send multi line items in invoice sync
                        lineItem=[]
                        totalBills=[]
                        for bill in exceldata:
                            obj={}
                            totalBills.append(bill['Bill No'])
                            if voucher['Bill No'] == bill['Bill No']:
                                obj={
                                        "saleType": "Normal",
                                        "quantity": 1, #---> Always enter 1
                                        "unitPrice": bill['Bill Amount'], #--> Bill Amount
                                        "amount": 0,
                                        "total_amount": 0,
                                        "description": "Hotel Service",
                                        "accountName":logindata['sundryaccode'] #change
                                    }
                                if float(bill['Bill Amount'])>=0:
                                    lineItem.append(obj)
                                else:
                                    pass

                        # this code for send multi line items in invoice sync

                        for con in ledger_settings:
                            if(con['ledgerCode']==voucher['Account Code']):
                                contactCode=con['ledgerName']
                                break
                            else:
                                contactCode="Not Found"

                        add_item={}
                        if contactCode != "Not Found":
                            countnum+=1
                            if float(voucher['Bill Amount']) >= 0:
                                if voucher['Bill No'] not in sendBills:
                                    
                                    add_item={
                                    "invoiceList":[
                                        {
                                            "number":number,
                                            "category": logindata["category"], #// form Settings
                                            "autoNumberFlag":autonf,
                                            "taxType":"NTAX",
                                            "invoiceType":"NA",
                                            "date":date, 
                                            "dueDate":date, 
                                            "amount":0,
                                            "companyGstin":logindata["gstin"], 
                                            # "currencyCode":"INR",
                                            "placeSupplyName":logindata["state"], 
                                            "branch":logindata["branch"],
                                            "contactName":contactCode, 
                                            "typeCode":"SINV",
                                            "status":savesstatusInv,
                                            "reference":voucher['Guest Name'],  
                                            "otherReference":voucher['Bill No'],
                                            "billAddress":{
                                                "name":voucher['Guest Name'], #--> Guest Name
                                                "type":"BADR", 
                                                "address1":"", #--> Address 1+Address 2+Address 3
                                                "city":logindata["state"], # --> Branch state from settings
                                                "state":logindata["state"], # --> Branch state from settings
                                                "zip":zipCode, #--> zipCode
                                                "country":"INDIA",
                                            },
                                            "roundFlag":"false",
                                            "lineItems":lineItem,
                                        }
                                    ]
                                    }
                                    accountingurl = acc_txn_url
                                    headers = {
                                        "x-auth-token": valuetoken,
                                        "x-preserveKey":  preserve,
                                        "x-company":  compid,
                                        "Content-Type": "application/json"
                                    }
                                    print("\n Total ---> ",countnum,"\n Add items -----------------",add_item)
                                    sendBills.append(voucher['Bill No'])
                                    r = requests.post(accountingurl, json=add_item, headers=headers)
                                    res = r.json()
                                    print("\n",res)
                                    if res['message'] == "Batch Data Added successfully":
                                        message="Done"
                                        a=syncCreditList(number=voucher['Bill No'],date=date,billAmount=voucher['Bill Amount'],remark=message,Status="SUCCESS",compid=compid,State=logindata["state"],jsondata=add_item)
                                        a.save(using="hotelogixexcel")
                                    else:
                                        if "fieldErrors" in res:
                                            fielderror=res['fieldErrors']
                                            message=""
                                            for l in fielderror:
                                                message+=l['message']
                                        else:
                                            message=res['errorList'].values()
                                        a=syncCreditList(number=voucher['Bill No'],date=date,billAmount=voucher['Bill Amount'],remark=message,Status="FAILED",compid=compid,State=logindata["state"],jsondata=add_item)
                                        a.save(using="hotelogixexcel")
                            else:
                                add_item = {
                                    "journalList": [
                                        {
                                            "taxRateFlag": False,
                                            "branch": logindata["branch"], # form Settings
                                            "category": logindata["category"], #// form Settings
                                            "number":auto_no, #// Bill No
                                            "autoNumberFlag":autonf,
                                            "debitAmount": abs(float(voucher['Bill Amount'])), #//
                                            "creditAmount": abs(float(voucher['Bill Amount'])), #//
                                            "companyGstin": logindata["gstin"], #// From Settings
                                            "reference": voucher['Bill No'],
                                            "manualJournalDetail": [
                                                {
                                                    "description": voucher['Guest Name'] + voucher['Account Code'] , #// Payment Reversal + Guest Name
                                                    "accountName": logindata['sundryaccode'] , #// SUNDRY DEBTORS CONTROL A/C form settings
                                                    "debitAmount": abs(float(voucher['Bill Amount'])) , #// Bill Amount
                                                },
                                                {
                                                    "description": voucher['Guest Name'] + voucher['Account Code'] , #// Payment Reversal + Guest Name
                                                    "accountName": contactCode , #, // - -> Account Code(search from ledger mapping)
                                                    "creditAmount":abs(float(voucher['Bill Amount'])) , #// Bill Amount
                                                }
                                            ],
                                            "narration": voucher['Guest Name'] + voucher['Account Code'], # // Payment Reversal + Guest Name
                                            "reportflag": 1,
                                            "autoReversingDate":None,
                                            "date": date,# // Bill Date
                                            "amount": 0,
                                            "taxType": "NTAX",
                                            "status": savesstatusJv,
                                            "txnStatus": "TRPN",
                                            "typeCode": "JMJ",
                                        }
                                    ] 
                                }
                                accountingurl = acc_txn_url
                                headers = {
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }
                                print("\n Total Count --------->",countnum,"\n  Add items ----------------->",add_item)
                                sendBills.append(voucher['Bill No'])
                                r = requests.post(accountingurl, json=add_item, headers=headers)
                                res = r.json()
                                # print("\n",res)
                                if res['message'] == "Batch Data Added successfully":
                                    message="Done"
                                    a=syncCreditList(number=voucher['Bill No'],date=date,billAmount=voucher['Bill Amount'],remark=message,Status="SUCCESS",compid=compid,State=logindata["state"],jsondata=add_item)
                                    a.save(using="hotelogixexcel")
                                else:
                                    if "fieldErrors" in res:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
                                    else:
                                        message=res['errorList'].values()
                                    a=syncCreditList(number=voucher['Bill No'],date=date,billAmount=voucher['Bill Amount'],remark=message,Status="FAILED",compid=compid,State=logindata["state"],jsondata=add_item)
                                    a.save(using="hotelogixexcel")
                                
                        elif voucher['Bill No'] not in sendBills:
                            message="Missing in ledger setting"
                            a=syncCreditList(number=voucher['Bill No'],date=date,billAmount=voucher['Bill Amount'],remark=message,Status="FAILED",compid=compid,State=logindata["state"],jsondata=add_item)
                            a.save(using="hotelogixexcel")

                    except Exception as e:
                        print("\nExcept error is--------------------",e)
            else:
                return Response(f"Missing Ledger { non_match1}")

            if res['message'] == "Batch Data Added successfully":
                return Response("Sync Credit List Successfully")
            else:
                return Response("Sync Credit List Failed !!!")

        except Exception as e:
            print("\nExcept error is--------------------",e)
            return Response(f"Sync Credit List Failed {e} !!!")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            for i in str(id).split(","):
                data=syncCreditList.objects.using("hotelogixexcel").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Delete Successfully...")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Not selected  data !!!")

# -------------- Sync Credit List API ---------------



# ----------------- Downloads Response json ----------------------
@api_view(['GET'])
def records(request,*args,**kwargs):
    if request.method=="GET":
        try: 
            print(request.data)
            id = request.GET.get('id')
            type=request.GET.get('type')
            print("\nid------------",id, "\ntype---------------",type)      
            if type == "RV":
                data=syncmanualJournal.objects.using('hotelogixexcel').filter(id=id).values("jsondata")
                print("data------",data[0]["jsondata"])
                return Response(data[0]["jsondata"])
            else:
                data=syncCreditList.objects.using("hotelogixexcel").filter(id=id).values("jsondata")
                print("data------",data)
                return Response(data[0]["jsondata"])
                
        except:
            return Response("SyncManualJournal get request in except")
    
# ----------------- Downloads XML and Accounting Json ----------------------




# ------------ Searching -------------------------
@api_view(['GET', 'POST'])
def filtertable(request,*args ,**kwargs):
    if request.method=="POST":
        synctype=request.data["synctype"]
        print("Sync Type------->",synctype)

        searchby=request.data["searchby"]
        print("searchby------->",searchby)

        compid=request.data["compid"]
        print("compid------->",compid)
        branch=request.data["branch"]
        print("branch------->",branch)

        print("re----------",request.data)

        # ----------- syncmanualJournal Filter ---------------------
        if synctype=="RV":
            if "number" in searchby and searchby["number"]!="":
                data=syncmanualJournal.objects.using("hotelogixexcel").filter(Q(Journalnumber__icontains=searchby["number"])).filter(compid=compid).values()
                # data=syncmanualJournal.objects.filter(Q(Journalnumber__icontains=searchby["number"])).filter(compid=compid,branch=branch).values()
                return Response(data)
                
            if "amount" in searchby and searchby["amount"]!="":
                # data=syncmanualJournal.objects.filter(Q(debitAmount__icontains=searchby["amount"])| Q(creditAmount__icontains=searchby["amount"]) ).filter(compid=compid,branch=branch).values()
                data=syncmanualJournal.objects.using("hotelogixexcel").filter(Q(debitAmount__icontains=searchby["amount"])| Q(creditAmount__icontains=searchby["amount"]) ).filter(compid=compid).values()
                return Response(data)
                
            if "status" in searchby and searchby["status"]!="":
                # data=syncmanualJournal.objects.filter(Q(Status__icontains=searchby["status"])).filter(compid=compid).values()
                data=syncmanualJournal.objects.using("hotelogixexcel").filter(Q(Status__icontains=searchby["status"])).filter(compid=compid,branch=branch).values()
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
                        # data=syncmanualJournal.objects.filter(Q(date__exact=date)).filter(compid=compid,branch=branch).values()
                        data=syncmanualJournal.objects.using("hotelogixexcel").filter(Q(date__exact=date)).filter(compid=compid).values()
                        for da in data:
                            data1.append(da)
                    return Response(data1)
            
        else:
            if "number" in searchby and searchby["number"]!="":
                # data=syncCreditList.objects.filter(Q(number__icontains=searchby["number"])).filter(compid=compid,branch=branch).values()
                data=syncCreditList.objects.using("hotelogixexcel").filter(Q(number__icontains=searchby["number"])).filter(compid=compid).values()
                return Response(data)
                
            if "amount" in searchby and searchby["amount"]!="":
                # data=syncCreditList.objects.filter(Q(billAmount__icontains=searchby["amount"])).filter(compid=compid,branch=branch).values()
                data=syncCreditList.objects.using("hotelogixexcel").filter(Q(billAmount__icontains=searchby["amount"])).filter(compid=compid).values()
                return Response(data)
                
            if "status" in searchby and searchby["status"]!="":
                # data=syncCreditList.objects.filter(Q(Status__icontains=searchby["status"])).filter(compid=compid,branch=branch).values()
                data=syncCreditList.objects.using("hotelogixexcel").filter(Q(Status__icontains=searchby["status"])).filter(compid=compid).values()
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
                        # data=syncCreditList.objects.filter(Q(date__exact=date)).filter(compid=compid,branch=branch).values()
                        data=syncCreditList.objects.using("hotelogixexcel").filter(Q(date__exact=date)).filter(compid=compid).values()
                        for da in data:
                            data1.append(da)
                    return Response(data1)
# ------------ Searching -------------------------
