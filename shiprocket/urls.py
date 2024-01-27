from django.urls import path
from .views import shiprocketlogin,show_order,check_availability,get_invoice,get_creditnote,credit_availabilitycheck,generate_awb_invoice,generate_awb_creditnote,get_popup_check_data,branchapi,updateshipment,updateinvoice,get_popup_credit_data,validatecredit,validateinvoice,updatecredit,dispatch_status_inv

urlpatterns = [
    path('shiprocketlogin/',shiprocketlogin),
    path('showorder/',show_order),
    path('check_avail/',check_availability),
    path('check_invoice/',get_invoice),
    path('check_creditnote/',get_creditnote),
    path('availabilitycheckcredit/',credit_availabilitycheck),
    path('awb_generate_invoice/',generate_awb_invoice),
    path('awb_generate_creditnote/',generate_awb_creditnote),
    path('get_check_popupdata/',get_popup_check_data),
    path('get_credit_popupdata/',get_popup_credit_data),
    path('shipbranch/',branchapi),
    path('updateship/',updateshipment),
    path('updateinv/',updateinvoice),
    path('validate_creditnote/',validatecredit),
    path('validate_invoice/',validateinvoice),
    path('update_creditnote/',updatecredit),
    path('dispstatus_inv/',dispatch_status_inv),



    ]
