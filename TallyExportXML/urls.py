from django.conf.urls import url
from .views import branchlist,search_acc_code,SyncLedgerHBtotally,SyncTransactionHBtotally,SyncLedgerTallytoHB,SyncTransactionTallytoHB,getJsondata

urlpatterns =[
    url(r'^branchList/',branchlist),
    url(r'^search_acc_code/',search_acc_code),
    url(r'^syncacc/',SyncLedgerHBtotally),
    url(r'^synctrans/',SyncTransactionHBtotally),
    url(r'^syncledgertallyhb/',SyncLedgerTallytoHB),
    url(r'^synctransactiontallyhb/',SyncTransactionTallytoHB),
    url(r'^getjson/',getJsondata),
]



