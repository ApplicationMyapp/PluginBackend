from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import XML_UserData,XML_syncData, syncCreditList, syncmanualJournal,CustomerModelSync,User
from django.http import HttpResponse
import requests
from . import Accounting
import json
import xmltodict
from django.contrib.auth.models import User as DjangoUser
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.db.models import Q
import re

# --------------------- Accounting log in Live/Sandbox -------------------------------

# All New urls for sandbox and local use
branch = "https://booksapi.hostbooks.in/hostbook/api/master/list"
acc_txn_url = "https://booksapi.hostbooks.in/hostbook/api/transaction/add"
acc_mas_url = "https://booksapi.hostbooks.in/hostbook/api/master/add"
# https://booksapi.hostbooks.in/hostbook/api/master/add"
clienturls="https://booksapi.hostbooks.in/securitycenter/client/login"



# All urls for live server
# branch = "https://in2accounts.hostbooks.com/api/master/list"
# acc_txn_url = "https://in2accounts.hostbooks.com/api/transaction/add"
# acc_mas_url = "https://in2accounts.hostbooks.com/api/master/add"


# --------------------- Login ---------------------------- 
@api_view(['GET', 'POST', 'PUT','DELETE'])
def login(request, **kwargs):   
    if request.method == "GET":
        try:
            compid = request.GET.get('compid')
            print("Login API Called --------",compid)
            data = XML_UserData.objects.using('consolidationxml').filter(companyid=compid).values()
            return Response(data)
        except:
            return Response("hotellogix login get request in except")

    if request.method == "POST":
        try:
            print("Login Post API Called ---------->",request.data)

            branch = request.data['branch']
            mjseries = request.data['mjseries']
            category = request.data['category']
            sundryaccode=request.data['sundryaccode']
            if "gstin" in  request.data:
                gstin = request.data['gstin']
            else:
                gstin = ""
            state = request.data['state']
            saveas = request.data['saveas']
            city = request.data['city']
            zip1 = request.data['zip']
            address1 = request.data['address1']
            ledger_settings = request.data['ledger_settings']
            compid = request.data['compid']
            walkingcustomer=request.data["walkingcustomer"]

            token = request.data['token_key']+"-"+request.data['branchCode']
            autoSync=request.data['autoSync']

            # call Accounting login api if auto sync == true
            if autoSync == "True" or autoSync == True:
                clientid=request.data['clientid']
                clientsecret=request.data['clientsecret']

                clientheaders = {
                    "clientId": clientid,
                    "clientSecret": clientsecret
                }
                r = requests.post(clienturls, json=clientheaders)
                res = r.json()  
                if res["status"]==200 or res["status"]==201:
                    valuetoken = res["data"]["client"]["accessToken"]
                    compid = res["data"]["client"]["businessId"]
                    a = XML_UserData(branch=branch,walkingcustomer=walkingcustomer, category=category, gstin=gstin,mjseries=mjseries,state=state, saveas=saveas,
                                city=city, zip=zip1, address1=address1, companyid=compid, ledger_settings=ledger_settings,sundryaccode=sundryaccode,token=token,autoSync=autoSync,clientid=clientid,clientsecret=clientsecret)
                    print(a)    
                    a.save(using="consolidationxml")
                    return Response("LOGIN SUCCESSFULLY")
                else:
                    return Response("Unauthorized Client Id or Client Secret Key")
                
            else:
                a = XML_UserData(branch=branch,walkingcustomer=walkingcustomer, category=category, gstin=gstin,mjseries=mjseries,state=state, saveas=saveas,
                                    city=city, zip=zip1, address1=address1, companyid=compid, ledger_settings=ledger_settings,sundryaccode=sundryaccode,token=token,autoSync=autoSync)
                print(a)
                a.save(using="consolidationxml")
                return Response("LOGIN SUCCESSFULLY")
        except Exception as e:
            return Response(f"Missing is :- {e}")

    if request.method == "PUT":
        try:
            print(request.data)
            id = request.data['id']
            branch = request.data['branch']
            category = request.data['category']
            gstin = request.data['gstin']
            mjseries = request.data['mjseries']
            state = request.data['state']
            saveas = request.data['saveas']
            sundryaccode=request.data['sundryaccode']
            city = request.data['city']
            zip = request.data['zip']
            address1 = request.data['address1']
            ledger_settings = request.data['ledger_settings']
            compid = request.data['compid']
            walkingcustomer=request.data["walkingcustomer"]
            print("Save as ---------->",saveas)
            # token = request.data['token_key']+"-"+request.data['branchCode']
            autoSync=request.data['autoSync']

            if autoSync == "True" or autoSync == True:
                clientid=request.data['clientid']
                clientsecret=request.data['clientsecret']
                a = XML_UserData.objects.using('consolidationxml').filter(id=id).update(branch=branch,clientid=clientid,clientsecret=clientsecret,mjseries=mjseries,walkingcustomer=walkingcustomer, category=category,sundryaccode=sundryaccode, gstin=gstin, state=state, saveas=saveas, city=city, zip=zip, address1=address1, companyid=compid, ledger_settings=ledger_settings,autoSync=autoSync)
                return Response("Updated successfully")
            else:
                a = XML_UserData.objects.using('consolidationxml').filter(id=id).update(branch=branch,mjseries=mjseries,walkingcustomer=walkingcustomer, category=category,sundryaccode=sundryaccode, gstin=gstin, state=state, saveas=saveas, city=city, zip=zip, address1=address1, companyid=compid, ledger_settings=ledger_settings,autoSync=autoSync)
                return Response("Updated successfully")
        except:
            return Response("Update failed please fill data carefully")
# --------------------- Login ----------------------------- 


# ----------------- Branch api -----------------------------
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
            print("\n helooo-----------------------------",request.data)
            # account_id="953"
            account_id=request.data["account_id"]
            global compid,preserve,valuetoken
            compid, preserve = request.data['compid'], request.data['preservekey']
            login = Accounting.Accounting_login(preserve, compid,account_id)
            print("this.is login--------------------",login)
            compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']
            username=login['username']
            print("Username View ---------->",username)

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
                obj['branchCode']=x['code']
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

            # -------------------- Token Generate ----------------

            if not username or not compid:
                return Response({'error': 'Please provide both username and password.'}, status=400)

            # Check if the user are already exists
            try:
                print("\nin try hello-------------------")
                user = DjangoUser.objects.using("consolidationxml").get(username=username)
                user_profile, created = User.objects.using("consolidationxml").get_or_create(django_user=user, defaults={'is_valid': True})
                token, created = Token.objects.using("consolidationxml").get_or_create(user=user_profile.django_user)
                return Response({"Branch": data_branch, "Category": data_cat, "costCenter": costcode['data']['master']['list'], 'token': token.key})
            
            except DjangoUser.DoesNotExist:
                django_user = DjangoUser.objects.using("consolidationxml").create(username=username, password=compid)
                user_profile = User.objects.using("consolidationxml").create(django_user=django_user, is_valid=True)
                token = Token.objects.using("consolidationxml").create(user=user_profile.django_user)
                return Response({"Branch": data_branch, "Category": data_cat, "costCenter": costcode['data']['master']['list'], 'token': token.key})



        except Exception as e:
            print("Exception is --------->",e)
            return Response(f"Error is {e}")

# ---------------- Branch api ------------------------------


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


# --------------- Convert into xml to json ------------------
@api_view(['GET', 'POST','DELETE'])
def xmlToken(request,**kwargs):
    if request.method=="GET":
        getdata=request.headers
        stype1=getdata['Synctype']
        token1= getdata['Token']
        print("getdata--------->",stype1,"\t ",token1)
        data= XML_syncData.objects.using('consolidationxml').filter(token=token1,syncType=stype1).values("id","date","status","filedate").order_by('-id')
        if len(data)!=0:
            return Response (data)
        else:
            return Response ("No Data Found")
    
    if request.method=="POST":
        try:
            postdata=request.headers
            print("postdata ---------->",postdata)
            usertoken=postdata['Token']
            synctype=postdata['Synctype'].upper()

            if "date" in postdata:
                filedate=postdata['date']
            else:
                filedate = datetime.now().strftime("%d-%m-%Y")
            
            print("\n Formatted Current Date: -->", filedate)

            if (synctype == "RV" or synctype == "CL"):
                token1= XML_UserData.objects.using('consolidationxml').filter(token=usertoken).values()
                auto=token1[0]
                token=auto["token"]
                print("\n  Token is Try ---------> ",token,"\n")
                print("\n Auto values -------->",auto)
                xmldata=request.body.decode('utf-8')
                dateError=re.compile(r'\b\d{2}-\d{2}-\d{4}\b')
                match =dateError.search(filedate)
                print("Match --------->",match)

                if not match:
                    return Response({"status_Code":400,"isSuccess":False,"message":'Please provide the correct Date Format : DD-MM-YYYY'})
                else:
                    pass

                
                if(len(auto)!=0):
                    try:
                        status="New"
                        # Data save in database 
                        a=XML_syncData(token=usertoken,syncType=synctype,xmldata=xmldata,status=status,filedate=filedate)
                        a.save(using="consolidationxml")
                        if auto["autoSync"] == "True":
                            a=XML_syncData.objects.using('consolidationxml').filter(token=token,syncType=synctype).values("id").order_by('-id')
                            id =a[0]["id"]
                            print("\n User id is ----------->",a[0]["id"])
                            if synctype == "CL":
                                funres=clautosync(auto,xmldata,id) #  Call cl functions 
                            else:
                                funres=rvautosync(auto,xmldata,id)

                            print("RV response -----------",funres)
                            
                            if (funres =="Sync Successfully"):
                                return Response({"status_Code":200,"isSuccess":True,"message":"Data Add Successfully","synctype":synctype,"autoSync":"Activate","Sync Status":funres})
                            else:
                                return Response({"status_Code":201,"isSuccess":True,"message":"Data Add Successfully","synctype":synctype,"autoSync":"Activate","Sync Status":funres})
                        else:
                            return Response({"status_Code":200,"isSuccess":True,"message":"Data Add Successfully","synctype":synctype,"autoSync":"Deactivate"})

                    except Exception as a:
                        print("a--------->",a)
                        return Response({"status_Code":400,"isSuccess":False,"message":f"Missing are {a}","synctype":synctype})
                else:
                    print("Else token------------------")
                    return Response({"status_Code":400,"isSuccess":False,"message":"Invalid Token","synctype":synctype})

            else:
                print("Else synctype----------------")
                return Response({"status_Code":400,"isSuccess":False,"message":"Invalid Sync Type"})
        except Exception as a:
                print("in expet---------------->",a)
                return Response({"status_Code":400,"isSuccess":False,"message":"Invalid Token","synctype":synctype})
        

    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            if id!="":
                for i in str(id).split(","):
                    data=XML_syncData.objects.using("consolidationxml").filter(id=int(i))
                    data.delete()
                return Response("Deleted Successfully")
        
        except  Exception as e:
            print("Error ------------",e)
            return Response("Not selected data !!!")
        
# -------------- Convert into xml to json -------------------

# # ---------- RV automations --------------
def rvautosync(autovalue,xml,id):
    try:
        print(" \n Rv---------->",autovalue)
        add_itemclient={
            "clientId":autovalue["clientid"],
            "clientSecret":autovalue["clientsecret"],
        }
        r = requests.post(clienturls, json=add_itemclient)
        res = r.json()
        valuetoken=res["data"]["client"]["accessToken"]
        print("\n Value token ------>",valuetoken)
        compid=res["data"]["client"]["businessId"]
        print("\n Company id ------>",compid)
        print("\n Xml data is --------->",xml)
        xmldata1=xmltodict.parse(xml)
        jsondata=json.dumps(xmldata1,indent=2)
        xmldata=json.loads(jsondata)

        print("\n xml json ---------->",xmldata)
        remote = xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['@REMOTEID']

        date=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['DATE']
        formated_date= datetime.strptime(date, "%Y%m%d")
        output_date = formated_date.strftime("%d-%m-%Y")
        print("date ------------->",output_date)

        jv=output_date.split("-")
        jv1=jv[0]+jv[1]+jv[2]

        Journalnumber=autovalue['branch']+"-"+"JV" + str(jv1)
        print("jv ---------------------------------------",Journalnumber)
        mjseries=autovalue["mjseries"]
        print("\n\n Mj series -------------->",mjseries)
        saveas1=autovalue["saveas"]

        if saveas1=="Draft":
            savesstatus="MJDT"
        else:
            savesstatus="MJPT"
        
        if mjseries=="Auto":
            autonf=True
            auto_no=""
        else:
            autonf=False
            auto_no=Journalnumber


        amount=abs(float(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST'][0]["AMOUNT"]))
        print("\n Amount----------->",amount)
        maindata=[]
        creditamount=0
        debitamount=0
        for data in xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']:
            if float(data["AMOUNT"]) !=0:
                if float(data['AMOUNT']) > 0:
                    for row in autovalue['ledger_settings']:
                        code=row['ledgerCode'].strip()
                        acc_code=data['LEDGERNAME']
                        print("\n\n Code in -----------------??",row['ledgerCode'].strip(),acc_code)
                        if code==acc_code:
                            print("in if con credit--------",code,acc_code)
                            code1=row['ledgerName']
                            break
                        else:
                            code1="Not Found"
                    print("\n code 1-------->",code1)
                    if code1 == "Not Found":
                        return f"{data['LEDGERNAME']} is missing in ledger settings"
                    else:
                        pass
                    
                    print("match account name-------",code1)
                    manualJournal={
                        "description":data['USERDESCRIPTION.LIST']['USERDESCRIPTION'],
                        "accountName": code1,
                        "debitAmount": abs(float(data['AMOUNT']))
                        # "creditAmount": abs(float(data['AMOUNT']))
                    }
                    maindata.append(manualJournal)
                else:
                    for row in autovalue['ledger_settings']:
                        code=row['ledgerCode'].strip()
                        acc_code=data['LEDGERNAME']
                        if code==acc_code:
                            code1=row['ledgerName'].strip()
                            break
                        else:
                            code1="Not Found"
                    manualJournal={
                        "description":data['USERDESCRIPTION.LIST']['USERDESCRIPTION'],
                        "accountName": code1,
                        # "debitAmount": abs(float(data['AMOUNT']))
                        "creditAmount": abs(float(data['AMOUNT']))

                    }
                    maindata.append(manualJournal)

        for i in maindata:
            if "debitAmount" in i:
                debitamount+=i["debitAmount"]
            else:
                creditamount+=i["creditAmount"]

        additem= {
            "journalList": [
                {
                    "taxRateFlag": "false",
                    "branch":autovalue['branch'],
                    "category": autovalue['category'],
                    "number": auto_no,
                    "autoNumberFlag":autonf,
                    "debitAmount":debitamount,
                    "creditAmount": creditamount,
                    "companyGstin": autovalue['gstin'], #From Settings
                    "manualJournalDetail": maindata,
                    "narration":xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'] ,#Narrationx	
                    "reportflag": 1,
                    # "autoReversingDate": 'Null',
                    "date": output_date, #Date
                    "amount": 0,
                    "taxType": "NTAX",
                    "status": savesstatus,  
                    "txnStatus": "TRPN",
                    "typeCode":"JMJ",
                }
            ]
        }

        print("\n\nAdd items ---------->",additem)

        accountingurl = acc_txn_url
        headers = {
            "x-auth-token": valuetoken,
            # "x-preserveKey":  preserve,
            "x-company":  compid,
            "Content-Type": "application/json"
        }
        r = requests.post(accountingurl, json=additem, headers=headers)
        res = r.json()
        print("\n\nAccounting Response ----------->",res)
        if res['message'] == "Batch Data Added successfully":
            print("\n-------IF--------- Batch Data Added successfully ",res['message'])
            message="Done"
            a=syncmanualJournal(Journalnumber=remote,date=output_date,Narration=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'],creditAmount=abs(amount),debitAmount=abs(amount),remark=message,Status="SUCCESS",compid=compid,jsondata=additem,branch=autovalue['branch'])
            a.save(using="consolidationxml")
            data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
            return "Sync Successfully"
        else:
            if "fieldErrors" in res:
                fielderror=res['fieldErrors']
                message=""
                for l in fielderror:
                    message+=l['message']
            else:
                message=res['errorList'].values()

            print("\nError is -------->",message)
            a=syncmanualJournal(Journalnumber=remote,date=output_date,Narration=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'],creditAmount=abs(amount),debitAmount=abs(amount),remark=message,Status="FAILED",compid=compid,jsondata=additem,branch=autovalue['branch'])
            a.save(using="consolidationxml")
            data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
            return ("Sync RV Failed !!!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\nExcept error is--------------------",e)
        return f"Error is {e}"

# ---------- RV automations --------------
        
# --------------------- Sync CL Automated-------------------
def clautosync(autovalue,xml,id):
    try:
        add_itemclient={
            "clientId":autovalue["clientid"],
            "clientSecret":autovalue["clientsecret"],
        }
        r = requests.post(clienturls, json=add_itemclient)
        res = r.json()
        valuetoken=res["data"]["client"]["accessToken"]
        print("\n Value token ------>",valuetoken)
        compid=res["data"]["client"]["businessId"]
        xmldata1=xmltodict.parse(xml)
        jsondata=json.dumps(xmldata1,indent=2)
        xmldata=json.loads(jsondata)
        print("\nCompid ------------->",compid)
        countnum=0
        saveas1=autovalue["saveas"]
        if saveas1=="Draft":
            savesstatusInv="INDT"
            savesstatusJv="MJDT"
        else:
            savesstatusInv="INAP"
            savesstatusJv="MJPT"

            
        newdata=[]
        if type(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']) == dict:
            # print("Hey I am dict ")
            newdata.append(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST'])
        else:
            # print("Hey I am list") 
            newdata=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']

        # print("\n\n Data is New dataset   -------------->",newdata)

        # this code is for change date format
        date2=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']["DATE"]
        try:
            date = datetime.strptime(date2, '%Y%m%d').strftime('%d-%m-%Y')
        except ValueError:
            return Response("Date format issue")
        
        for voucher in newdata:
                isInvoicesync=True
                countnum+=1
                # print("\n Voucher is -------->",voucher)
                try:
                    lineItem=[]
                    for bill in newdata:
                        obj={}
                        if float(bill['AMOUNT'])>=0:
                            obj={
                                    "saleType": "Normal",
                                    "quantity": 1, 
                                    "unitPrice": bill['AMOUNT'], 
                                    "amount": 0,
                                    "total_amount": 0,
                                    "description": "Hotel Service",
                                    "accountName":autovalue['sundryaccode'] #change   ## automations problem
                                }
                            lineItem.append(obj)
                        else:
                            pass
                    contactCode=voucher['LEDGER']['#text']
                    print("\ncontact code-----------------------",contactCode)
                    add_item={}
                    print("\n voucher['INVOICE'] -----------",voucher['INVOICE'])
                    if float(voucher['AMOUNT']) > 0:
                        if voucher["LEDGER"]["@TYPE"] == "GUEST" or voucher["LEDGER"]["@TYPE"] == "":
                            contactCode=autovalue["walkingcustomer"]
                        
                        print("\n New Contact name ----------->",contactCode)

                        if voucher['LEDGER']['#text'] is None:
                            references=""
                            name=""
                        else:
                            references=voucher['LEDGER']['#text']
                        print("\n References ---->",references)

                        if voucher['OWNER']['ADDRESS.LIST'] is None:
                            address1= autovalue["address1"]
                            city=autovalue["city"]
                            state=autovalue["state"]
                            zipcode=autovalue["zip"]
                            country="India"

                        else:
                            if voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0]['#text'] is not None:
                                address1=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0] else autovalue["address1"]
                                city=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][3]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][3] else autovalue["city"]
                                state=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][4]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][4] else autovalue["state"]
                                zipcode=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][6]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][6] else autovalue["zip"]
                                country="India"

                        print("\n Address ----->",address1, "\n city ----->",city,"\n state ------->",state,"\n zipcode ------->",zipcode,"\n country ------->",country)
                        acnumber=voucher['LEDGER']['@CODE']
                        gstin=autovalue["gstin"]
                        voucherno=str(voucher['INVOICE'])
                        branch=autovalue["branch"]
                        typeset=voucher["LEDGER"]["@TYPE"]

                        #  ------------------- Customer Sync Conditions---------------------

                        if typeset == "TA" or typeset == "CORP":
                            name=voucher['OWNER']['BILLINGCONTACT.LIST']['BILLINGCONTACT'][0]['#text']

                            add_itemcust= {
                                "contactList": [
                                    {
                                        "name": references, 
                                        "accountNumber": acnumber, 
                                        "employee": False,
                                        "vendor": False, 
                                        "customer": True, 
                                        "primaryType": "customer", 
                                        "address": [
                                            {
                                                "addressGSTIN": gstin, 
                                                "address1":address1 ,
                                                "city": city, 
                                                "state": state, 
                                                "zip": zipcode,
                                                "country": country,
                                                "type": "PADR"
                                            }
                                        ],
                                        "status": "COAC",
                                    }
                                    ]
                                }
                            print("\n \n ContactList Json ------>",add_itemcust)
                            
                            accountingurl = acc_mas_url
                            headers = {
                                "x-auth-token": valuetoken,
                                # "x-preserveKey":  preserve,
                                "x-company":  compid,
                                "Content-Type": "application/json"
                            }

                            r = requests.post(accountingurl, json=add_itemcust, headers=headers)
                            res = r.json()
                            print("\n Accounting Response in Contact Sync  ----------->",res)
                            try:
                                if "batch data added successfully" in res['message'].lower():
                                    message="Done"
                                    print("syncCustomer  is Save if ")
                                    cust=CustomerModelSync(voucher_field=voucherno,date_field=date,compid_field=compid,remark_field=message,status_field="SUCCESS",jsondata_field=add_itemcust,branch_field=branch,synctype_field=typeset)
                                    cust.save(using="consolidationxml")
                                    # print("Sync Customer batch is Save  successfully------->",result)
                                else:
                                    if "fieldErrors" in res:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            message+=l['message']
                                    else:
                                        message=str(res['errorList'].values())
                                    cust=CustomerModelSync(voucher_field=voucherno,date_field=date,compid_field=compid,remark_field=message,status_field="FAILED",jsondata_field=add_itemcust,branch_field=branch,synctype_field=typeset)
                                    cust.save(using="consolidationxml")
                            except Exception as e:
                                print('Exception in syncCustomer ',e,'\n')


                        #  ------------------- Customer Sync Conditions---------------------                                  
                            
                        add_item={
                            "invoiceList":[
                                {
                                    "number":str(voucher['INVOICE']),
                                    "category":autovalue["category"],
                                    "taxType":"NTAX",
                                    "invoiceType":"NA",
                                    "date":date, #--> Bill Date
                                    "dueDate":date, #--> Bill Date
                                    "amount":0,  
                                    "references":references,
                                    "companyGstin":autovalue["gstin"], 
                                    "currencyCode":"INR",
                                    "placeSupplyName":autovalue["state"], 
                                    "branch":autovalue["branch"], 
                                    "contactName":contactCode, 
                                    "typeCode":"SINV",
                                    "status":savesstatusInv,
                                    "billAddress":{
                                        "type":"BADR", 
                                        "name":name,
                                        "address1":address1,
                                        "city":city,
                                        "state":state,
                                        "zip":zipcode,
                                        "country":country

                                    },
                                    "roundFlag":"false",
                                    "lineItems":[
                                            {
                                                "saleType": "Normal",
                                                "quantity": 1,
                                                "unitPrice": voucher['AMOUNT'], 
                                                "amount": 0,
                                                "total_amount": 0,
                                                "description": voucher["REFERENCE"] if "REFERENCE" in voucher else date,
                                                "accountName":autovalue['sundryaccode'] 
                                            }
                                        ],
                                    }
                                ]
                        }
                    
                        print("\n\n isInvoicesync ------------->",isInvoicesync,"\n\n")

                        if isInvoicesync == True:
                            print("\n ",countnum,". Add item -----------------",add_item)
                            accountingurl = acc_txn_url
                            headers = {
                                "x-auth-token": valuetoken,
                                "x-company":  compid,
                                "Content-Type": "application/json"
                            }

                            r = requests.post(accountingurl, json=add_item, headers=headers)
                            res = r.json()

                            print("\nAccount response ----->",res)
                            if res['message'] == "Batch Data Added successfully" or res["status"] == 200:
                                message="Done"
                                cl=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="SUCCESS",compid=compid,State=autovalue["state"],jsondata=add_item,branch=autovalue["branch"],synccl="Invoice")
                                cl.save(using="consolidationxml")
                                a=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
                            else:
                                if "fieldErrors" in res:
                                    fielderror=res['fieldErrors']
                                    message=""
                                    for l in fielderror:
                                        message+=l['message']
                                else:
                                    message=res['errorList'].values()
                                cl=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="FAILED",compid=compid,State=autovalue["state"],jsondata=add_item,branch=autovalue["branch"],synccl="Invoice")
                                cl.save(using="consolidationxml")
                                a=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
                        else:
                            print ("\n isInvoicesync condition is False")
                            pass
        
                    else:
                        add_item = {
                            "journalList": [
                                {
                                    "taxRateFlag": False,
                                    "branch": autovalue["branch"], 
                                    "category":autovalue["category"], 
                                    "number":str(voucher['INVOICE']),
                                    "debitAmount": abs(float(voucher['AMOUNT'])), 
                                    "creditAmount": abs(float(voucher['AMOUNT'])), 
                                    "companyGstin": autovalue["gstin"], 
                                    "reference": voucher['INVOICE'],
                                    "manualJournalDetail": [
                                        {
                                            "description":  "Payment Reversal"+" - " +voucher['INVOICE'], 
                                            "accountName":  autovalue["sundryaccode"], 
                                            "debitAmount": abs(float(voucher['AMOUNT'])) , 
                                        },
                                        {
                                            "description": "Payment Reversal"+" - " +voucher['INVOICE'], 
                                            "accountName": contactCode , 
                                            "creditAmount":abs(float(voucher['AMOUNT'])) ,
                                        }
                                    ],
                                    "narration":  voucher["REFERENCE"] if "REFERENCE" in voucher else date, 
                                    "reportflag": 1,
                                    "autoReversingDate":None,
                                    "date": date,    
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
                            # "x-preserveKey":  preserve,
                            "x-company":  compid,
                            "Content-Type": "application/json"
                        }
                        print("\n ",countnum,". Add item In Else -----------------",add_item)
                        r = requests.post(accountingurl, json=add_item, headers=headers)
                        res = r.json()
                        print("\n Accounting Response ---->",res)
                        if res['message'] == "Batch Data Added successfully":
                            message="Done"
                            cl=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="SUCCESS",compid=compid,State=autovalue["state"],jsondata=add_item,branch=autovalue["branch"], synccl="JV")
                            cl.save(using="consolidationxml")
                            a=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
                            print("\n", countnum, "Sucessfully save IF ")
                        else:
                            if "fieldErrors" in res:
                                fielderror=res['fieldErrors']
                                message=""
                                for l in fielderror:
                                    message+=l['message']
                            else:
                                message=f'res['"errorList"'].values()'
                            cl=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="FAILED",compid=compid,State=autovalue["state"],jsondata=add_item,branch=autovalue["branch"],synccl="JV")
                            cl.save(using="consolidationxml")
                            a=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
                            print("\n hello- 3 -------",a)
                            print("\n", countnum, "Else save ")
                except Exception as e:
                    print("\nExcept error is---- hello----------------",e)
        if res['message'] == "Batch Data Added successfully":
            return "Sync Successfully"
        else:
            return "Sync Credit List Failed"
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\nExcept error is--------------------",e)
        return f"Error is {e}"

# --------------------- Sync CL Automated------------------


# ----------- Sync RV ---------------------
@api_view(['GET', 'POST',"DELETE"])
def syncrv(request,*args,**kwargs):
    if request.method=="GET":
        try: 
            compid=request.GET.get('compid')
            branch=request.GET.get('branch')
            print("Compid is and branch---------------",compid,branch)            
            data=syncmanualJournal.objects.using("consolidationxml").filter(compid=compid,branch=branch).values("Journalnumber","id","date","creditAmount","debitAmount","compid","remark","Status",).order_by('-id')
            # print("data------",data)
            return Response(data)
        except:
            return Response("SyncManualJournal get request in except")
    
    if request.method=="POST":
        ledger_data=json.loads(request.data['ledger_data'])
        print("\nthis is ledeger settings--------------------",ledger_data)
        id=request.data["loginData"]["id"]
        print("\n this is Request data--------------------",request.data)
        account_id=request.data["account_id"]
        compid, preserve = request.data['compid'], request.data['preserveKey']
        login = Accounting.Accounting_login(preserve, compid,account_id)
        compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']

        a=XML_syncData.objects.using("consolidationxml").filter(id=id).values("xmldata")
        xmldata=xmltodict.parse(a[0]['xmldata'])

        remote=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['@REMOTEID']
        
        date=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['DATE']
        formated_date= datetime.strptime(date, "%Y%m%d")
        output_date = formated_date.strftime("%d-%m-%Y")
        print("date ------------->",output_date)

        jv=output_date.split("-")
        jv1=jv[0]+jv[1]+jv[2]

        Journalnumber=ledger_data['branch']+"-"+"JV" + str(jv1)
        print("jv ---------------------------------------",Journalnumber)
        mjseries=ledger_data["mjseries"]
        print("\n\n Mj series -------------->",mjseries)
        saveas1=ledger_data["saveas"]

        if saveas1=="Draft":
            savesstatus="MJDT"
        else:
            savesstatus="MJPT"
        
        if mjseries=="Auto":
            autonf=True
            auto_no=""
        else:
            autonf=False
            auto_no=Journalnumber


        amount=abs(float(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST'][0]["AMOUNT"]))
        print("\n Amount----------->",amount)


        maindata=[]
        creditamount=0
        debitamount=0
        for data in xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']:
           
            if float(data["AMOUNT"]) !=0:
                if float(data['AMOUNT']) > 0:
                    for row in ledger_data['ledger_settings']:
                        code=row['ledgerCode'].strip()
                        acc_code=data['LEDGERNAME']
                        # print("\n\n Code in -----------------??",row['ledgerCode'].strip(),"\n",acc_code)
                        if code==acc_code:
                            # print("in if con credit--------",code,acc_code)
                            code1=row['ledgerName']
                            break
                        else:
                            code1="Not Found"
                    if code1 == "Not Found":
                        return Response (f"{data['LEDGERNAME']} is missing in ledger settings")
                    else:
                        pass
                    
                    # print("match account name-------",code1)
                    manualJournal={
                        "description":data['USERDESCRIPTION.LIST']['USERDESCRIPTION'],
                        "accountName": code1,
                        # "creditAmount": abs(float(data['AMOUNT']))
                        "debitAmount": abs(float(data['AMOUNT']))
                    }
                    maindata.append(manualJournal)
                else:
                    for row in ledger_data['ledger_settings']:
                        code=row['ledgerCode'].strip()
                        acc_code=data['LEDGERNAME']
                        if code==acc_code:
                            code1=row['ledgerName'].strip()
                            break
                        else:
                            code1="Not Found"
                    manualJournal={
                        "description":data['USERDESCRIPTION.LIST']['USERDESCRIPTION'],
                        "accountName": code1,
                        # "debitAmount": abs(float(data['AMOUNT']))
                        "creditAmount": abs(float(data['AMOUNT']))
                    }
                    maindata.append(manualJournal)

        for i in maindata:
            if "debitAmount" in i:
                debitamount+=i["debitAmount"]
            else:
                creditamount+=i["creditAmount"]

        additem= {
            "journalList": [
                {
                    "taxRateFlag": "false",
                    "branch":ledger_data['branch'],
                    "category": ledger_data['category'],
                    "number": auto_no,
                    "autoNumberFlag":autonf,
                    "debitAmount":debitamount,
                    "creditAmount": creditamount,
                    "companyGstin": ledger_data['gstin'], #From Settings
                    "manualJournalDetail": maindata,
                    "narration":xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'] ,#Narrationx	
                    "reportflag": 1,
                    # "autoReversingDate": 'Null',
                    "date": output_date, #Date
                    "amount": 0,
                    "taxType": "NTAX",
                    "status": savesstatus,  
                    "txnStatus": "TRPN",
                    "typeCode":"JMJ",
                }
            ]
        }

        print("\n\nAdd items ---------->",additem)

        accountingurl = acc_txn_url
        headers = {
            "x-auth-token": valuetoken,
            "x-preserveKey":  preserve,
            "x-company":  compid,
            "Content-Type": "application/json"
        }
        r = requests.post(accountingurl, json=additem, headers=headers)
        res = r.json()
        print("\n\nAccounting Response ----------->",res)
        if res['message'] == "Batch Data Added successfully":
            print("\n-------IF--------- Batch Data Added successfully ",res['message'])
            message="Done"
            a=syncmanualJournal(Journalnumber=remote,date=output_date,Narration=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'],creditAmount=abs(amount),debitAmount=abs(amount),remark=message,Status="SUCCESS",compid=compid,jsondata=additem,branch=ledger_data['branch'])
            a.save(using="consolidationxml")
            data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
            return Response("Sync RV Successfully")
        else:
            if "fieldErrors" in res:
                fielderror=res['fieldErrors']
                message=""
                for l in fielderror:
                    message+=l['message']
            else:
                message=res['errorList'].values()

            print("\nError is -------->",message)
            a=syncmanualJournal(Journalnumber=remote,date=output_date,Narration=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['NARRATION'],creditAmount=abs(amount),debitAmount=abs(amount),remark=message,Status="FAILED",compid=compid,jsondata=additem,branch=ledger_data['branch'])
            a.save(using="consolidationxml")
            data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
            return Response("Sync RV Failed !!!")
    
    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            print("Deleted id -------------",id)
            for i in str(id).split(","):
                data=syncmanualJournal.objects.using("consolidationxml").filter(id=int(i))
                data.delete()
                print(f"data : {i} -->",data)
            return Response("Deleted Successfully")
        except  Exception as e:
            print("Error ------------",e)
            return Response("Not selected data !!!")

# ----------- Sync RV ---------------------


#  ---------------- Sync CL------------------
@api_view(['GET', 'POST','DELETE'])
def synccl(request,*args,**kwargs):
    if request.method=="GET":
        try: 
            compid=request.GET.get('compid')
            branch=request.GET.get('branch')
            if request.GET.get('getType')=="CL":
                print("CL Compid is and branch---------------",compid,branch)            
                data=syncCreditList.objects.using("consolidationxml").filter(compid=compid,branch=branch).values("number","synccl","date","billAmount","compid","remark","Status","id","jsondata").order_by('-id')
                return Response(data)
            else:
                # cust=CustomerModelSync.objects.filter(compid=compid,branch=branch).values("voucher_field","date_field","remark_field","status_field","synctype_field").order_by("-id")
                cust=CustomerModelSync.objects.using("consolidationxml").filter(compid_field=compid,branch_field=branch).values("id","voucher_field","date_field","remark_field","status_field","synctype_field").order_by("-id")
                return Response(cust)
        except:
            return Response("Sync Invoice Get Request Faild")
    
    if request.method=="POST":
        try:
            print("\n Request data ----------->",request.data)
            account_id=request.data["account_id"]
            print("\n Request data ----------->",account_id)
            compid, preserve = request.data['compid'], request.data['preserveKey']
            login = Accounting.Accounting_login(preserve, compid,account_id)
            compid, preserve, valuetoken = login['compid'], login['preservekey'], login['token']
            id=request.data["loginData"]["id"]

            # XML to Convert into json
            a=XML_syncData.objects.using("consolidationxml").filter(id=id).values("xmldata")
            b=a[0]["xmldata"]
            xmldata1=xmltodict.parse(b)
            jsondata=json.dumps(xmldata1,indent=2)
            xmldata=json.loads(jsondata)
            ledger_settings = request.data['ledger_data']
            print("\nCompid ------------->",compid)
            countnum=0
            saveas1=ledger_settings["saveas"]
            if saveas1=="Draft":
                savesstatusInv="INDT"
                savesstatusJv="MJDT"
            else:
                savesstatusInv="INAP"
                savesstatusJv="MJPT"

                
            newdata=[]
            if type(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']) == dict:
                # print("Hey I am dict ")
                newdata.append(xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST'])
            else:
                # print("Hey I am list") 
                newdata=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']['LEDGERENTRIES.LIST']

            # print("\n\n Data is New dataset   -------------->",newdata)

            # this code is for change date format
            date2=xmldata['ENVELOPE']['BODY']['DATA']['VOUCHER']["DATE"]
            try:
                date = datetime.strptime(date2, '%Y%m%d').strftime('%d-%m-%Y')
            except ValueError:
                return Response("date format issue")
            res=""
            for voucher in newdata:
                    isInvoicesync=True
                    countnum+=1
                    # print("\n Voucher is -------->",voucher)
                    try:
                        lineItem=[]
                        for bill in newdata:
                            obj={}
                            if float(bill['AMOUNT'])>=0:
                                obj={
                                        "saleType": "Normal",
                                        "quantity": 1, 
                                        "unitPrice": bill['AMOUNT'], 
                                        "amount": 0,
                                        "total_amount": 0,
                                        "description": "Hotel Service",
                                        "accountName":ledger_settings['sundryaccode'] #change
                                    }
                                lineItem.append(obj)
                            else:
                                pass
                        contactCode=voucher['LEDGER']['#text']
                        print("\ncontact code-----------------------",contactCode)
                        add_item={}
                        print("\n voucher['INVOICE'] -----------",voucher['INVOICE'])
                        if float(voucher['AMOUNT']) > 0:
                            if voucher["LEDGER"]["@TYPE"] == "GUEST" or voucher["LEDGER"]["@TYPE"] == " ":
                                contactCode=request.data["ledger_data"]["walkingcustomer"]
                            
                            print("\n New Contact name ----------->",contactCode)

                            if voucher['LEDGER']['#text'] is None:
                                references=""
                                name=""
                            else:
                                references=voucher['LEDGER']['#text']
                                # name=voucher['OWNER']['BILLINGCONTACT.LIST']['BILLINGCONTACT'][0]['#text']
                            print("\n References ---->",references)
                            print("name --------->",name)

                            if voucher['OWNER']['ADDRESS.LIST'] is None:
                                # print("\n If ADDRESS.LIST")
                                address1= request.data["ledger_data"]["address1"]
                                city=request.data["ledger_data"]["city"]
                                state=request.data["ledger_data"]["state"]
                                zipcode=request.data["ledger_data"]["zip"]
                                country="India"

                            else:
                                if voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0]['#text'] is not None:
                                    address1=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][0] else request.data["ledger_data"]["address1"]
                                    city=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][3]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][3] else request.data["ledger_data"]["city"]
                                    state=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][4]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][4] else request.data["ledger_data"]["state"]
                                    zipcode=voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][6]['#text'] if "#text" in voucher['OWNER']['ADDRESS.LIST']['ADDRESS'][6] else request.data["ledger_data"]["zip"]
                                    country="India"

                            print("\n Address ----->",address1, "\n city ----->",city,"\n state ------->",state,"\n zipcode ------->",zipcode,"\n country ------->",country)
                            acnumber=voucher['LEDGER']['@CODE']
                            gstin=ledger_settings["gstin"]
                            voucherno=str(voucher['INVOICE'])
                            branch=ledger_settings["branch"]
                            typeset=voucher['LEDGER']['@TYPE']

                            #  ------------------- Customer Sync Conditions---------------------

                            if typeset == "TA" or typeset == "CORP":
                                name=voucher['OWNER']['BILLINGCONTACT.LIST']['BILLINGCONTACT'][0]['#text']
                                print("\n\n Name ------->",name)
                                cust=syncCustomer(compid,preserve,valuetoken,references,acnumber,gstin,address1,city,state,zipcode,country,voucherno,date,branch,typeset)   
                                print("\n Customer Function Retruns------------>",cust)
                                isInvoicesync=cust                                 
                                # isInvoicesync=False                                

                            #  ------------------- Customer Sync Conditions---------------------                                  
                                
                            add_item={
                                "invoiceList":[
                                    {
                                        "number":str(voucher['INVOICE']),
                                        "category":ledger_settings["category"],
                                        "taxType":"NTAX",
                                        "invoiceType":"NA",
                                        "date":date, #--> Bill Date
                                        "dueDate":date, #--> Bill Date
                                        "amount":0,  
                                        "references":references,
                                        "companyGstin":ledger_settings["gstin"], 
                                        "currencyCode":"INR",
                                        "placeSupplyName":ledger_settings["state"], 
                                        "branch":ledger_settings["branch"], 
                                        "contactName":contactCode, 
                                        "typeCode":"SINV",
                                        "status":savesstatusInv,
                                        "billAddress":{
                                            "type":"BADR", 
                                            "name":name,
                                            "address1":address1,
                                            "city":city,
                                            "state":state,
                                            "zip":zipcode,
                                            "country":country

                                        },
                                        "roundFlag":"false",
                                        "lineItems":[
                                                {
                                                    "saleType": "Normal",
                                                    "quantity": 1,
                                                    "unitPrice": voucher['AMOUNT'], 
                                                    "amount": 0,
                                                    "total_amount": 0,
                                                    "description": voucher["REFERENCE"] if "REFERENCE" in voucher else date,
                                                    "accountName":ledger_settings['sundryaccode'] 
                                                }
                                            ],
                                        }
                                    ]
                            }
                        
                            print("\n\n isInvoicesync ------------->",isInvoicesync,"\n\n")

                            if isInvoicesync == True:
                                print("\n ",countnum,". Add item -----------------",add_item)
                                accountingurl = acc_txn_url
                                headers = {
                                    "x-auth-token": valuetoken,
                                    "x-preserveKey":  preserve,
                                    "x-company":  compid,
                                    "Content-Type": "application/json"
                                }

                                r = requests.post(accountingurl, json=add_item, headers=headers)
                                res = r.json()

                                print("\nAccount response ----->",res)
                                if res['message'] == "Batch Data Added successfully" or res["status"] == 200:
                                    message="Done"
                                    a=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="SUCCESS",compid=compid,State=ledger_settings["state"],jsondata=add_item,branch=ledger_settings["branch"],synccl="Invoice")
                                    # print("helllll- 1 -------",a)
                                    a.save(using="consolidationxml")
                                    data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
                                else:
                                    if "fieldErrors" in res:
                                        fielderror=res['fieldErrors']
                                        message=""
                                        for l in fielderror:
                                            # print("Loloo ----------",l)
                                            message+=l['message']
                                    else:
                                        message=res['errorList'].values()
                                    # print("\n Messages ---------->",message)
                                    a=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="FAILED",compid=compid,State=ledger_settings["state"],jsondata=add_item,branch=ledger_settings["branch"],synccl="Invoice")
                                    a.save(using="consolidationxml")
                                    # print("helllll- 2 -------",a)
                                    data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
                            else:
                                print ("\n isInvoicesync condition is False")
                                pass
            
                        else:
                            add_item = {
                                "journalList": [
                                    {
                                        "taxRateFlag": False,
                                        "branch": ledger_settings["branch"], # form Settings
                                        "category":ledger_settings["category"], #// form Settings
                                        "number":str(voucher['INVOICE']),
                                        "debitAmount": abs(float(voucher['AMOUNT'])), #//
                                        "creditAmount": abs(float(voucher['AMOUNT'])), #//
                                        "companyGstin": ledger_settings["gstin"], #// From Settings
                                        "reference": voucher['INVOICE'],
                                        "manualJournalDetail": [
                                            {
                                                "description":  "Payment Reversal"+" - " +voucher['INVOICE'], #// Payment Reversal + Guest Name
                                                "accountName":  ledger_settings["sundryaccode"], #// SUNDRY DEBTORS CONTROL A/C form settings
                                                "debitAmount": abs(float(voucher['AMOUNT'])) , #// Bill Amount
                                            },
                                            {
                                                "description": "Payment Reversal"+" - " +voucher['INVOICE'], #// Payment Reversal + Guest Name
                                                "accountName": contactCode , #, // - -> Account Code(search from ledger mapping)
                                                "creditAmount":abs(float(voucher['AMOUNT'])) , #// Bill Amount
                                            }
                                        ],
                                        # "narration":  voucher["REFERENCE"], # // Payment Reversal + Guest Name
                                        "narration":  voucher["REFERENCE"] if "REFERENCE" in voucher else date, # // Payment Reversal + Guest Name
                                        "reportflag": 1,
                                        "autoReversingDate":None,
                                        "date": date,     # // Bill Date
                                        "amount": 0,  
                                        "taxType": "NTAX",
                                        "status": savesstatusJv,
                                        "txnStatus": "TRPN",
                                        "typeCode": "JMJ",
                                    }
                                ]
                            }
                            # print("\n Reference -----------",voucher['INVOICE'])

                            accountingurl = acc_txn_url
                            headers = {
                                "x-auth-token": valuetoken,
                                "x-preserveKey":  preserve,
                                "x-company":  compid,
                                "Content-Type": "application/json"
                            }
                            print("\n ",countnum,". Add item In Else -----------------",add_item)
                            r = requests.post(accountingurl, json=add_item, headers=headers)
                            res = r.json()
                            print("\n Accounting Response ---->",res)
                            if res['message'] == "Batch Data Added successfully":
                                message="Done"
                                a=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="SUCCESS",compid=compid,State=ledger_settings["state"],jsondata=add_item,branch=ledger_settings["branch"], synccl="JV")
                                a.save(using="consolidationxml")
                                data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="SUCCESS")
                                print("\n", countnum, "Sucessfully save IF ")
                            else:
                                if "fieldErrors" in res:
                                    fielderror=res['fieldErrors']
                                    message=""
                                    for l in fielderror:
                                        message+=l['message']
                                else:
                                    message=res['errorList'].values()
                                a=syncCreditList(number=voucher['INVOICE'],date=date,billAmount=abs(float(voucher['AMOUNT'])),remark=message,Status="FAILED",compid=compid,State=ledger_settings["state"],jsondata=add_item,branch=ledger_settings["branch"],synccl="JV")
                                print("\n hello- 3 -------",a)
                                a.save(using="consolidationxml")
                                data=XML_syncData.objects.using("consolidationxml").filter(id=id).update(status="FAILED")
                                print("\n", countnum, "Else save ")
                    except Exception as e:
                        print("\nExcept error is---- hello----------------",e)
            if res['message'] == "Batch Data Added successfully":
                return Response("Sync Credit List Successfully")
            else:
                return Response("Sync Credit List Failed")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("\nExcept error is--------------------",e)
            return Response(f"Error is {e}")


    if request.method == "DELETE":
        try:
            id = request.GET.get('id')
            if id!="":
                for i in str(id).split(","):
                    if request.GET.get('type') == "Customer":
                        cus=CustomerModelSync.objects.using("consolidationxml").filter(id=int(i))
                        cus.delete()
                        print(f"data : {i} -->",cus)
                    else:
                        data=syncCreditList.objects.using("consolidationxml").filter(id=int(i))
                        data.delete()
                        print(f"data : {i} -->",data)
                return Response("Deleted Successfully")
            else:
                return Response("Not selected data !!!")

        except  Exception as e:
            print("Error ------------",e)
            return Response("Not selected data !!!")
    
#  ---------------- Sync CL------------------

def syncCustomer(compid,preserve,valuetoken,references,acnumber,gstin,address1,city,state,zipcode,country,voucherno,date,branch,typeset):
    print("\n compid ------>",compid,"\npreserve----------->",preserve,"\nvaluetoken---------------",valuetoken)
    add_item= {
        "contactList": [
            {
                "name": references, #//ADDRESS TYPE="COMPANYNAME"><![CDATA[Travelguru/Desiya]]></ADDRESS>
                "accountNumber": acnumber, #//<OWNER TYPE="TA" CODE="A7">
                "employee": False,
                "vendor": False, 
                "customer": True, 
                "primaryType": "customer", #//"customer"For "Commission.json" and "cendor" for "Commission.json"
                "address": [
                    {
                        "addressGSTIN": gstin, #//Contact->CompanyGstin
                        "address1":address1 , #//<ADDRESS TYPE="ADDRESSLINE1"><![CDATA[Tonk Road, Durgapura]]></ADDRESS>+<ADDRESS TYPE="ADDRESSLINE2"><![CDATA[]]></ADDRESS>
                        "city": city, #//<ADDRESS TYPE="CITY"><![CDATA[Jaipur]]></ADDRESS>
                        "state": state, #<ADDRESS TYPE="STATE"><![CDATA[Rajasthan]]></ADDRESS>
                        "zip": zipcode, #//<ADDRESS TYPE="ZIP"><![CDATA[302018]]></ADDRESS>
                        "country": country,
                        "type": "PADR"
                    }
                ],
                "status": "COAC",
            }
            ]
        }
    print("\n \n ContactList Json ------>",add_item)
    
    accountingurl = acc_mas_url
    headers = {
        "x-auth-token": valuetoken,
        "x-preserveKey":  preserve,
        "x-company":  compid,
        "Content-Type": "application/json"
    }

    r = requests.post(accountingurl, json=add_item, headers=headers)
    res = r.json()
    print("\n Accounting Response in Contact Sync  ----------->",res)
    try:
        if "batch data added successfully" in res['message'].lower():
            message="Done"
            print("syncCustomer  is Save if ")
            a=CustomerModelSync(voucher_field=voucherno,date_field=date,compid_field=compid,remark_field=message,status_field="SUCCESS",jsondata_field=add_item,branch_field=branch,synctype_field=typeset)
            a.save(using="consolidationxml")
            result=True
            # print("Sync Customer batch is Save  successfully------->",result)
        else:
            if "fieldErrors" in res:
                fielderror=res['fieldErrors']
                message=""
                for l in fielderror:
                    message+=l['message']
            else:
                message=str(res['errorList'].values())
            result=False
            a=CustomerModelSync(voucher_field=voucherno,date_field=date,compid_field=compid,remark_field=message,status_field="FAILED",jsondata_field=add_item,branch_field=branch,synctype_field=typeset)
            a.save(using="consolidationxml")
    except Exception as e:
        print('Exception in syncCustomer ',e,'\n')

    return result




# ----------------- Downloads Response json ----------------------
@api_view(['GET'])  
def records(request,*args,**kwargs):
    if request.method=="GET":
        try: 
            print(request.data)
            id = request.GET.get('id')
            type=request.GET.get('type')
            print("Compid is and branch---------------",type)      
            if type == "RV":
                data=syncmanualJournal.objects.using("consolidationxml").filter(id=id).values("jsondata")
                print("data------",data[0]["jsondata"])
                return Response(data[0]["jsondata"])
            elif type=="CL":
                data=syncCreditList.objects.using("consolidationxml").filter(id=id).values("jsondata")
                print("data------",data[0]["jsondata"])
                return Response(data[0]["jsondata"])
            
            elif type=="Customer":
                data=CustomerModelSync.objects.using("consolidationxml").filter(id=id).values("jsondata_field")
                print("data------",data[0]["jsondata_field"])
                return Response(data[0]["jsondata_field"])
                
            else:
                data=CustomerModelSync.objects.using("consolidationxml").filter(id=id).values("jsondata_field")
                print("data------",data[0]["jsondata_field"])
                return Response(data[0]["jsondata_field"])
        except Exception as e:
            print(e)
            return Response("SyncManualJournal get request in except")
    
# ----------------- Downloads XML and Accounting Json ----------------------


# ---------------- Json Downloads  ------------------
@api_view(['GET', 'POST'])
def xmldatadownload(request,**kwargs):
    if request.method=="GET":
        try:
            id=request.GET.get('id')
            print("ID-------------",id)
            # if request.GET.get('getType')
            data= XML_syncData.objects.using("consolidationxml").filter(id=id).values("xmldata")
            print("data lenght--------->",data)
            return Response (data)
        except:
            return Response ("No Data Found")
# ---------------- Json Downloads  ------------------



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

            # ----------- syncmanualJournal Filter ---------------------
            if synctype=="RV":
                if "number" in searchby and searchby["number"]!="":
                    data=syncmanualJournal.objects.using("consolidationxml").filter(Q(Journalnumber__icontains=searchby["number"])).filter(compid=compid).values()
                    # data=syncmanualJournal.objects.filter(Q(Journalnumber__icontains=searchby["number"])).filter(compid=compid,branch=branch).values()
                    return Response(data)
                    
                if "amount" in searchby and searchby["amount"]!="":
                    # data=syncmanualJournal.objects.filter(Q(debitAmount__icontains=searchby["amount"])| Q(creditAmount__icontains=searchby["amount"]) ).filter(compid=compid,branch=branch).values()
                    data=syncmanualJournal.objects.using("consolidationxml").filter(Q(debitAmount__icontains=searchby["amount"])| Q(creditAmount__icontains=searchby["amount"]) ).filter(compid=compid).values()
                    return Response(data)
                    
                if "status" in searchby and searchby["status"]!="":
                    data=syncmanualJournal.objects.filter(Q(Status__icontains=searchby["status"])).filter(compid=compid,branch=branch).values()
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
                            data=syncmanualJournal.objects.using("consolidationxml").filter(Q(date__exact=date)).filter(compid=compid).values()
                            for da in data:
                                data1.append(da)
                        return Response(data1)
                
            elif synctype=="Customer":
                filtered_data = {key: value for key, value in searchby.items() if value is not None}
                print("Filter data is -------->",searchby)
                if "number" in filtered_data:
                    print("Hello")
                    data=CustomerModelSync.objects.using("consolidationxml").filter(Q(voucher_field__icontains=searchby["number"])).filter(compid_field=compid).values()
                    return Response(data)
                    
                if "type" in filtered_data:
                    data=CustomerModelSync.objects.using("consolidationxml").filter(Q(synctype_field__icontains=searchby["type"])).filter(compid_field=compid).values()
                    return Response(data)
                    
                if "status" in filtered_data:
                    data=CustomerModelSync.objects.using("consolidationxml").filter(Q(status_field__icontains=searchby["status"])).filter(compid_field=compid,branch_field=branch).values()
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
                            data=CustomerModelSync.objects.using("consolidationxml").filter(Q(date_field__exact=date)).filter(compid_field=compid).values()
                            for da in data:
                                data1.append(da)
                        return Response(data1)
                
            else:
                if "number" in searchby and searchby["number"]!="":
                    data=syncCreditList.objects.using("consolidationxml").filter(Q(number__icontains=searchby["number"])).filter(compid=compid).values()
                    return Response(data)
                    
                if "amount" in searchby and searchby["amount"]!="":
                    data=syncCreditList.objects.using("consolidationxml").filter(Q(billAmount__icontains=searchby["amount"])).filter(compid=compid).values()
                    return Response(data)
                    
                if "status" in searchby and searchby["status"]!="":
                    data=syncCreditList.objects.using("consolidationxml").filter(Q(Status__icontains=searchby["status"])).filter(compid=compid).values()
                    return Response(data)
                
                if "type" in searchby and searchby["type"]!="":
                    data=syncCreditList.objects.using("consolidationxml").filter(Q(synccl__icontains=searchby["type"])).filter(compid=compid).values()
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
                            data=syncCreditList.objects.using("consolidationxml").filter(Q(date__exact=date)).filter(compid=compid).values()
                            for da in data:
                                data1.append(da)
                        return Response(data1)
            return Response("Data Not Found!")
        except Exception as a:
            print(a)
            return Response("Data Not Found!")
# ------------ Searching -------------------------  
