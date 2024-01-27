from django.conf.urls import url

from .views import login,branchlist,SyncManualJournal,SyncCreditList,search_acc_code,filtertable,records


urlpatterns = [
    url(r'^login/',login),
    url(r'^branchList/',branchlist),
    url(r'^syncJV/',SyncManualJournal),
    url(r'^syncCredit/',SyncCreditList),
    url(r'^search_acc_code/',search_acc_code),
    url(r'^filtertable/',filtertable),
    url(r'^getjson/',records),
    ]
