import requests


# urls for local and sandbox server uses
acc_login="https://booksapi.hostbooks.in/securitycenter/user/login"
acc_val_user="https://booksapi.hostbooks.in/securitycenter/user/validateUserLogin"

# urls for live server uses
# acc_val_user="https://inapiaccounts.hostbooks.com/user/validateUserLogin"


# # function for local and sandbox server 
def Accounting_login(preserve,compid):
    print("Compid---------->",compid)
    print("preserve key ---------->",preserve)
    url1 =acc_login
    add_item = {
                "username": "amar.pal@hostbooks.com",
                "password":  "Hostbooks.com"
                
                # "username": "ashish.baranwal@hostbooks.com",
                # "password":  "123456"

            }
    r = requests.post(url1, json=add_item)
    token = r.json()
    valuetoken = token['data']['user']['accessToken']
    preserve = token['data']['user']['preserveKey']
    # compid="389B7CCF-2F78-AC7B-ECD8-87FDEDE3E083"
    compid="592723AC-96F8-148A-54FF-101DBDF3E3DF"
    # compid="3D4074E5-D1B5-8C4E-F035-6D03931BE809"
    # compid="16D0C587-0060-36A0-503B-C7546121E517"
    url2 =acc_val_user
    headers = {
        "x-version": "IND",
        "x-preserveKey":  preserve,
        "x-company": compid,
        "x-forwarded-portal":  "true",
        "Content-Type": "application/json"
    }
    r = requests.get(url2, headers=headers)
    return {"compid":compid,"preservekey":preserve,"token":valuetoken}



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
