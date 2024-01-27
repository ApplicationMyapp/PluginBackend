from django.conf.urls import url
from .views import filtertable, login,branchlist,search_acc_code,xmlToken,syncrv,synccl,xmldatadownload,records

urlpatterns =[
    url(r'^login/',login),
    url(r'^xmldata/',xmlToken),
    url(r'^branchList/',branchlist),
    url(r'^search_acc_code/',search_acc_code),
    url(r'^syncrv/',syncrv),
    url(r'^synccl/',synccl),
    url(r'^filtertable/',filtertable),
    url(r'^getxmldata/',xmldatadownload),
    url(r'^getjson/',records),
]



