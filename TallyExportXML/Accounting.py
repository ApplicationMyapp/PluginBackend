import requests


# urls for local and sandbox server uses
acc_login="https://booksapi.hostbooks.in/securitycenter/user/login"
acc_val_user="https://booksapi.hostbooks.in/securitycenter/user/validateUserLogin"

# urls for live server uses
# acc_val_user="https://inapiaccounts.hostbooks.com/user/validateUserLogin"


# # function for local and sandbox server 
def Accounting_login(preserve,compid):
    url1 =acc_login
    add_item = {

                "username": "amar.pal@hostbooks.com",
                "password":  "Hostbooks.com",
                # "username": "rahul.kumar@hostbooks.com",
                # "password":  "12345678"
            }
    # https://books.hostbooks.in/?comp=
    r = requests.post(url1, json=add_item)
    token = r.json()
    valuetoken = token['data']['user']['accessToken']
    preserve = token['data']['user']['preserveKey']
    compid="592723AC-96F8-148A-54FF-101DBDF3E3DF"
    # compid="B60C026C-2E6B-94A5-E141-350659539984"
    url2 =acc_val_user
    headers = {
        "x-version": "IND",
        "x-preserveKey":  preserve,
        "x-company": compid,
        "x-forwarded-portal":  "true",
        "Content-Type": "application/json"
    }
    r = requests.get(url2, headers=headers)
    print("Response data----------->",r.json())
    userfind=r.json()
    name=userfind['data']['user']['companyName']
    print("User name --------->",name)
    print("preserve key ---------->",preserve)
    return {"compid":compid,"preservekey":preserve,"token":valuetoken,"username":name}



# function for live server 
# def Accounting_login(preserve,compid):
#     print("Compid---------->",compid)
#     print("preserve key ---------->",preserve)
#     accounting =acc_val_user
#     headers = {
#         "x-version": "IND",
#         "x-preserveKey":  preserve,
#         "x-company":  compid,
#         "x-forwarded-portal":  "true",
#         "Content-Type": "application/json"
#     }
#     r = requests.get(accounting, headers=headers)
#     token3 = r.json()
#     valuetoken = token3['data']['user']['accessToken']
#     return {"compid":compid,"preservekey":preserve,"token":valuetoken}
