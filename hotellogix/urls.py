from django.conf.urls import url 
from .views import hotelogixlogin,branchlist,SyncDeposit,SyncInvoice,syncCommission,syncPayment,failedinv,faileddep,failedpay,failedcomm,search_acc_code,getjsonrecord,filtertable

urlpatterns = [
    url(r'^login/',hotelogixlogin),
    url(r'^branchList/',branchlist),
    url(r'^syncdeposit/',SyncDeposit),
    url(r'^syncinvoice/',SyncInvoice),
    url(r'^synccomm/',syncCommission),
    url(r'^syncpay/',syncPayment),
    url(r'^syncinvoicefailed/',failedinv),
    url(r'^syncdepositfailed/',faileddep),
    url(r'^syncpayfailed/',failedpay),
    url(r'^synccommfailed/',failedcomm),
    url(r'^search_acc_code/',search_acc_code),
    url(r'^getjsonrecord/',getjsonrecord),
    url(r'^filtertable/',filtertable),
]
