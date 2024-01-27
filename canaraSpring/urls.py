from django.conf.urls import url
from .views import customerLogin, filtertable,search_acc_code,branchList,SyncCustomer,SyncInvoice,SyncCreditNote,SyncReceipt,SyncExpenses,SyncInventoryGroupMaster,SyncProduct,branchData,getJsondata

urlpatterns = [
    url(r'^login/',customerLogin),
    url(r'^search_acc_code/',search_acc_code),
    url(r'^branch/',branchList),
    url(r'^customer/',SyncCustomer),
    url(r'^invoice/',SyncInvoice),
    url(r'^creditnote/',SyncCreditNote),
    url(r'^receipt/',SyncReceipt),
    url(r'^expenses/',SyncExpenses),
    url(r'^inventorygroupmaster/',SyncInventoryGroupMaster),
    url(r'^product/',SyncProduct),
    url(r'^branchData/',branchData),
    url(r'^jsondata/',getJsondata),
    url(r'^filtertable/',filtertable),
]