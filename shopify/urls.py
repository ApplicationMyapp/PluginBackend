from django.conf.urls import url, include
from .views import shopifylogin, syncItem,syncInvoice,sync,syncsalesorder,branchlist
urlpatterns = [
    url(r'^shopifylogin/',shopifylogin),
    url(r'^syncitem/',syncItem),
    url(r'^syncinvoice/',syncInvoice),
    url(r'^sync/',sync),
    url(r'^syncsalesorder/',syncsalesorder),
    url(r'^branchlist/',branchlist),
    # url(r'^getjson/',getjson),
    # url(r'^invoicejson/',post_invoice),
    # url(r'^orderjson/',post_salesorder),
]

