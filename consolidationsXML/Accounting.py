import requests


# urls for local and sandbox server uses
acc_login="https://booksapi.hostbooks.in/securitycenter/user/login"
acc_val_user="https://booksapi.hostbooks.in/securitycenter/user/validateUserLogin"

# urls for live server uses
# acc_val_user="https://inapiaccounts.hostbooks.com/user/validateUserLogin"


# ------------- Function for local and sandbox server ------------------- 
def Accounting_login(preserve,compid,account_id):
    print("Compid---------->",compid)
    url1 =acc_login
    add_item = {
                "username": "amar.pal@hostbooks.com",
                "password":  "Hostbooks.com",
                # "username": "rahul.kumar@hostbooks.com",
                # "password":  "12345678"
                # "username": "ashish.baranwal@hostbooks.com",
                # "password":  "123456"
            }
    # https://books.hostbooks.in/?comp=
    r = requests.post(url1, json=add_item)
    token = r.json()
    valuetoken = token['data']['user']['accessToken']
    preserve = token['data']['user']['preserveKey']
    url2 =acc_val_user
    if account_id is None:
        compid="592723AC-96F8-148A-54FF-101DBDF3E3DF"
        # compid="3D4074E5-D1B5-8C4E-F035-6D03931BE809"
        headers = {
            "x-version": "IND",
            "x-preserveKey":  preserve,
            "x-company": compid,
            "x-forwarded-portal":  "true",
            "Content-Type": "application/json"
        }

    else:
        compid="EC2C6119-FA92-6DB7-884B-A968D9383CBB"
        # compid="3D4074E5-D1B5-8C4E-F035-6D03931BE809"
        headers = {
            "x-version": "IND",
            "x-preserveKey":  preserve,
            "x-company": compid,
            'x-account_id':account_id,
            "x-forwarded-portal":  "true",
            "Content-Type": "application/json"
        }

    r = requests.get(url2, headers=headers)
    print("Response data----------->",r.json())
    userfind=r.json()
    name=userfind['data']['user']['companyName']
    print("name is  --------->",name)
    print("preserve key ---------->",preserve)

    return {"compid":compid,"preservekey":preserve,"token":valuetoken,"username":name}

# ------------- Function for local and sandbox server ------------------- 


# ------------ function for live server ----------------------- 
# def Accounting_login(preserve,compid,account_id):
#     print("Compid---------->",compid)
#     print("preserve key ---------->",preserve)
#     accounting =acc_val_user
#     if account_id is None:
#         headers = {
#             "x-version": "IND",
#             "x-preserveKey":  preserve,
#             "x-company": compid,
#             "x-forwarded-portal":  "true",
#             "Content-Type": "application/json"
#         }

#     else:
#         headers = {
#             "x-version": "IND",
#             "x-preserveKey":  preserve,
#             "x-company": compid,
#             'x-account_id':account_id,
#             "x-forwarded-portal":  "true",
#             "Content-Type": "application/json"
#         }

#     r = requests.get(accounting, headers=headers)
#     token3 = r.json()
#     name=token3['data']['user']['companyName']
#     print("User name --------->",name)
#     valuetoken = token3['data']['user']['accessToken']
#     return {"compid":compid,"preservekey":preserve,"token":valuetoken,"username":name}
