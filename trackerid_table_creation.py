import mysql.connector as m

# All table create Plugin wise 
def migrate_hotelogix(db_name):
    print("enter in function ")
    conn=m.connect(host="localhost",password="root",user="root",database=db_name)
    cur=conn.cursor()
    # create first table hotellogix_commfailedrecord
    cur.execute("show tables like 'hotellogix_commfailedrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_commfailedrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `invoicecode` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_commfailedrecord")
    else:
        print("hotellogix_commfailedrecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_commfailedrecord")

    
    # create second table hotellogix_commrecord
    cur.execute("show tables like 'hotellogix_commrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_commrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `invoicecode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_commrecord")
    else:
        print("hotellogix_commrecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_commrecord")

    # create third table hotellogix_depositfailedrecord
    cur.execute("show tables like 'hotellogix_depositfailedrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_depositfailedrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Narration` varchar(100) DEFAULT NULL,
                `Credit_Amount` varchar(100) DEFAULT NULL,
                `Debit_Amount` varchar(100) DEFAULT NULL,
                `depcode` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_depositfailedrecord")
    else:
        print("hotellogix_depositfailedrecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_depositfailedrecord")

    # create fourth table hotellogix_depositrecord
    cur.execute("show tables like 'hotellogix_depositrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_depositrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Narration` varchar(100) DEFAULT NULL,
                `Credit_Amount` varchar(100) DEFAULT NULL,
                `Debit_Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `depcode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_depositrecord")
    else:
        print("hotellogix_depositrecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_depositrecord")


    # create fifth table hotellogix_hotellogixlogin
    cur.execute("show tables like 'hotellogix_hotellogixlogin'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_hotellogixlogin` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `user` varchar(100) DEFAULT NULL,
                `password` varchar(100) DEFAULT NULL,
                `hotelid` varchar(100) DEFAULT NULL,
                `branch` varchar(100) DEFAULT NULL,
                `category` varchar(100) DEFAULT NULL,
                `gstin` varchar(100) DEFAULT NULL,
                `saveas` varchar(100) DEFAULT NULL,
                `state` varchar(100) DEFAULT NULL,
                `address1` varchar(100) DEFAULT NULL,
                `city` varchar(100) DEFAULT NULL,
                `zip` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `ledger_settings` json NOT NULL DEFAULT (_utf8mb3'"1"'),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_hotellogixlogin")
    else:
        print("hotellogix_hotellogixlogin already exists")
        # insertion_hotelogix(db_name,"hotellogix_hotellogixlogin")

    # create sixth table hotellogix_invoicerecord
    cur.execute("show tables like 'hotellogix_invoicerecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_invoicerecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Customer_Name` varchar(100) DEFAULT NULL,
                `Invoice_Amount` varchar(100) DEFAULT NULL,
                `Due_Amount` varchar(100) DEFAULT NULL,
                `Received_Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `invoicecode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_invoicerecord")
    else:
        print("hotellogix_invoicerecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_invoicerecord")


    # create seventh table hotellogix_invoicerecordfailed
    cur.execute("show tables like 'hotellogix_invoicerecordfailed'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_invoicerecordfailed` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Customer_Name` varchar(100) DEFAULT NULL,
                `Invoice_Amount` varchar(100) DEFAULT NULL,
                `invoicecode` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_invoicerecordfailed")
    else:
        print("hotellogix_invoicerecordfailed already exists")
        # insertion_hotelogix(db_name,"hotellogix_invoicerecordfailed")

    # create eighth table hotellogix_paymentfailedrecord
    cur.execute("show tables like 'hotellogix_paymentfailedrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_paymentfailedrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `paymentcode` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_paymentfailedrecord")
    else:
        print("hotellogix_paymentfailedrecord already exists")
        # insertion_hotelogix(db_name,"hotellogix_paymentfailedrecord")


    # create ninth table hotellogix_paymentrecord
    cur.execute("show tables like 'hotellogix_paymentrecord'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `hotellogix_paymentrecord` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `Number` varchar(100) DEFAULT NULL,
                `Date` varchar(100) DEFAULT NULL,
                `Amount` varchar(100) DEFAULT NULL,
                `Remark` varchar(500) DEFAULT NULL,
                `Status` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `Requested_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `Response_json` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `branchid` varchar(100) DEFAULT NULL,
                `paymentcode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_hotelogix(db_name,"hotellogix_paymentrecord")
    else:
        print("hotellogix_paymentrecord already exists")


def migrate_shiprocket(db_name):
    print("enter in function ")
    conn=m.connect(host="localhost",password="root",user="root",database=db_name)

    cur=conn.cursor()

    # create first table shiprocket_check_availability_data
    cur.execute("show tables like 'shiprocket_check_availability_data'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_check_availability_data` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `SalesOrderNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `orderdate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `ordertype` varchar(100) NOT NULL,
                `mode` varchar(100) NOT NULL,
                `availability` varchar(100) NOT NULL,
                `returnable` varchar(100) NOT NULL,
                `courier_agent` varchar(100) NOT NULL,
                `weight` varchar(100) DEFAULT NULL,
                `length` varchar(100) DEFAULT NULL,
                `breadth` varchar(100) DEFAULT NULL,
                `height` varchar(100) DEFAULT NULL,
                `shipmentno` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_check_availability_data")
    else:
        print("shiprocket_check_availability_data already exists")
        # insertion_shiprocket(db_name,"shiprocket_check_availability_data")


    # create second table shiprocket_credit_awb
    cur.execute("show tables like 'shiprocket_credit_awb'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_credit_awb` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `status` varchar(100) DEFAULT NULL,
                `CreditnoteNo` varchar(100) NOT NULL,
                `credit_data` json NOT NULL,
                `awb_data` json NOT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_credit_awb")
    else:
        print("shiprocket_credit_awb already exists")
        # insertion_shiprocket(db_name,"shiprocket_credit_awb")

    
    # create third table shiprocket_credit_check_availability
    cur.execute("show tables like 'shiprocket_credit_check_availability'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_credit_check_availability` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `CreditnoteNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `Creditnotedate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `json` json DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `mode` varchar(100) NOT NULL,
                `availability` varchar(100) NOT NULL,
                `courier_agent` varchar(100) NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_credit_check_availability")
    else:
        print("shiprocket_credit_check_availability already exists")
        # insertion_shiprocket(db_name,"shiprocket_credit_check_availability")

    
    # create fourth table shiprocket_credit_popup_check_data
    cur.execute("show tables like 'shiprocket_credit_popup_check_data'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_credit_popup_check_data` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `statusid` varchar(100) DEFAULT NULL,
                `courier_id` varchar(100) DEFAULT NULL,
                `courier_name` varchar(100) DEFAULT NULL,
                `etd` varchar(100) DEFAULT NULL,
                `freight_charge` varchar(100) DEFAULT NULL,
                `min_weight` varchar(100) DEFAULT NULL,
                `pickup_availability` varchar(100) DEFAULT NULL,
                `pod_available` varchar(100) DEFAULT NULL,
                `rating` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_credit_popup_check_data")
    else:
        print("shiprocket_credit_popup_check_data already exists")
        # insertion_shiprocket(db_name,"shiprocket_credit_popup_check_data")


    # create fifth table shiprocket_creditnotedetails
    cur.execute("show tables like 'shiprocket_creditnotedetails'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_creditnotedetails` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `CreditnoteNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `Creditnotedate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `json` json DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_creditnotedetails")
    else:
        print("shiprocket_creditnotedetails already exists")
        # insertion_shiprocket(db_name,"shiprocket_creditnotedetails")

    
    # create sixth table shiprocket_invoice_awb
    cur.execute("show tables like 'shiprocket_invoice_awb'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_invoice_awb` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `status` varchar(100) DEFAULT NULL,
                `InvoiceNo` varchar(100) NOT NULL,
                `invoice_data` json NOT NULL,
                `awb_data` json NOT NULL,
                `dispatch_data` json NOT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_invoice_awb")
    else:
        print("shiprocket_invoice_awb already exists")
        # insertion_shiprocket(db_name,"shiprocket_invoice_awb")


    # create seventh table shiprocket_invoice_awb_failed
    cur.execute("show tables like 'shiprocket_invoice_awb_failed'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_invoice_awb_failed` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `status` varchar(100) DEFAULT NULL,
                `InvoiceNo` varchar(100) NOT NULL,
                `invoice_data` json NOT NULL,
                `awb_data` json NOT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_invoice_awb_failed")
    else:
        print("shiprocket_invoice_awb_failed already exists")
        # insertion_shiprocket(db_name,"shiprocket_invoice_awb_failed")


    # create eighth table shiprocket_invoicedetails
    cur.execute("show tables like 'shiprocket_invoicedetails'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_invoicedetails` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `InvoiceNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `Invoicedate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `shipWeight` varchar(100) DEFAULT NULL,
                `shipHeight` varchar(100) DEFAULT NULL,
                `shipBreadth` varchar(100) DEFAULT NULL,
                `shipLength` varchar(100) DEFAULT NULL,
                `shipSurface` varchar(100) DEFAULT NULL,
                `pinCodeAvailability` varchar(100) DEFAULT NULL,
                `json` json DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_invoicedetails")
    else:
        print("shiprocket_invoicedetails already exists")
        # insertion_shiprocket(db_name,"shiprocket_invoicedetails")


    # create ninth table shiprocket_popup_check_data
    cur.execute("show tables like 'shiprocket_popup_check_data'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_popup_check_data` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `statusid` varchar(100) DEFAULT NULL,
                `courier_id` varchar(100) DEFAULT NULL,
                `courier_name` varchar(100) DEFAULT NULL,
                `etd` varchar(100) DEFAULT NULL,
                `freight_charge` varchar(100) DEFAULT NULL,
                `min_weight` varchar(100) DEFAULT NULL,
                `pickup_availability` varchar(100) DEFAULT NULL,
                `pod_available` varchar(100) DEFAULT NULL,
                `rating` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_popup_check_data")
    else:
        print("shiprocket_popup_check_data already exists")
        # insertion_shiprocket(db_name,"shiprocket_popup_check_data")


    # create tenth table shiprocket_shiprocketlogin
    cur.execute("show tables like 'shiprocket_shiprocketlogin'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_shiprocketlogin` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `email` varchar(254) NOT NULL,
                `password` varchar(100) NOT NULL,
                `gstin` varchar(100) NOT NULL,
                `branch` varchar(100) NOT NULL,
                `cemail` varchar(100) NOT NULL,
                `cphone` varchar(100) NOT NULL,
                `cname` varchar(100) NOT NULL,
                `channelid` varchar(100) NOT NULL,
                `pickup_location` varchar(100) NOT NULL,
                `companyid` varchar(100) NOT NULL,
                `dimension_status` varchar(100) NOT NULL,
                `weight` varchar(100) NOT NULL,
                `length` varchar(100) NOT NULL,
                `breadth` varchar(100) NOT NULL,
                `height` varchar(99) NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_shiprocketlogin")
    else:
        print("shiprocket_shiprocketlogin already exists")
        # insertion_shiprocket(db_name,"shiprocket_shiprocketlogin")

    # create eleventh table shiprocket_showorderdetails
    cur.execute("show tables like 'shiprocket_showorderdetails'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_showorderdetails` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `SalesOrderNo` varchar(100) NOT NULL,
                `customername` varchar(100) DEFAULT NULL,
                `orderdate` varchar(100) DEFAULT NULL,
                `frompincode` varchar(100) DEFAULT NULL,
                `topincode` varchar(100) DEFAULT NULL,
                `state` varchar(100) DEFAULT NULL,
                `city` varchar(100) DEFAULT NULL,
                `shippingaddress` varchar(254) DEFAULT NULL,
                `posted_at` varchar(100) DEFAULT NULL,
                `ordertype` varchar(100) DEFAULT NULL,
                `weight` varchar(100) DEFAULT NULL,
                `length` varchar(100) DEFAULT NULL,
                `breadth` varchar(100) DEFAULT NULL,
                `height` varchar(100) DEFAULT NULL,
                `shipmentno` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_showorderdetails")
    else:
        print("shiprocket_showorderdetails already exists")
        # insertion_shiprocket(db_name,"shiprocket_showorderdetails")


    # create twelveth table shiprocket_validate_credit_data
    cur.execute("show tables like 'shiprocket_validate_credit_data'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_validate_credit_data` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `CreditnoteNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `Creditnotedate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `json` json DEFAULT NULL,
                `Remark` longtext NOT NULL,
                `mode` varchar(100) DEFAULT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_validate_credit_data")
    else:
        print("shiprocket_validate_credit_data already exists")
        # insertion_shiprocket(db_name,"shiprocket_validate_credit_data")


    # create thirteen table shiprocket_validate_invoice_data
    cur.execute("show tables like 'shiprocket_validate_invoice_data'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shiprocket_validate_invoice_data` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `InvoiceNo` varchar(100) NOT NULL,
                `customername` varchar(100) NOT NULL,
                `Invoicedate` varchar(100) NOT NULL,
                `frompincode` varchar(100) NOT NULL,
                `topincode` varchar(100) NOT NULL,
                `state` varchar(100) NOT NULL,
                `city` varchar(100) NOT NULL,
                `shippingaddress` varchar(254) NOT NULL,
                `shipWeight` varchar(100) DEFAULT NULL,
                `shipHeight` varchar(100) DEFAULT NULL,
                `shipBreadth` varchar(100) DEFAULT NULL,
                `shipLength` varchar(100) DEFAULT NULL,
                `shipSurface` varchar(100) DEFAULT NULL,
                `pinCodeAvailability` varchar(100) DEFAULT NULL,
                `json` json DEFAULT NULL,
                `Remark` longtext NOT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_shiprocket(db_name,"shiprocket_validate_invoice_data")
    else:
        print("shiprocket_validate_invoice_data already exists")
        # insertion_shiprocket(db_name,"shiprocket_validate_invoice_data")


def migrate_consolidate(db_name):
    print("enter in function ")
    conn=m.connect(host="localhost",password="root",user="root",database=db_name)

    cur=conn.cursor()

    # create first table consolidate_hotelogix_hotellogixlogin
    cur.execute("show tables like 'consolidate_hotelogix_hotellogixlogin'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `consolidate_hotelogix_hotellogixlogin` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `branch` varchar(100) DEFAULT NULL,
                `category` varchar(100) DEFAULT NULL,
                `gstin` varchar(100) DEFAULT NULL,
                `state` varchar(100) DEFAULT NULL,
                `saveas` varchar(100) DEFAULT NULL,
                `city` varchar(100) DEFAULT NULL,
                `zip` varchar(100) DEFAULT NULL,
                `address1` varchar(100) DEFAULT NULL,
                `ledger_settings` json NOT NULL,
                `companyid` varchar(100) DEFAULT NULL,
                `sundryaccode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_consolidate(db_name,"consolidate_hotelogix_hotellogixlogin")
    else:
        print("consolidate_hotelogix_hotellogixlogin already exists")
        # insertion_consolidate(db_name,"consolidate_hotelogix_hotellogixlogin")


    # create second table consolidate_hotelogix_synccreditlist
    cur.execute("show tables like 'consolidate_hotelogix_synccreditlist'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `consolidate_hotelogix_synccreditlist` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `State` varchar(100) DEFAULT NULL,
                `date` varchar(100) DEFAULT NULL,
                `number` varchar(100) DEFAULT NULL,
                `billAmount` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `remark` varchar(400) DEFAULT NULL,
                `Status` varchar(400) DEFAULT NULL,
                `jsondata` longtext,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_consolidate(db_name,"consolidate_hotelogix_synccreditlist")
    else:
        print("consolidate_hotelogix_synccreditlist already exists")
        # insertion_consolidate(db_name,"consolidate_hotelogix_synccreditlist")

    # create third table consolidate_hotelogix_syncmanualjournal
    cur.execute("show tables like 'consolidate_hotelogix_syncmanualjournal'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `consolidate_hotelogix_syncmanualjournal` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `date` varchar(100) DEFAULT NULL,
                `Revenuecode` varchar(100) DEFAULT NULL,
                `Revenuename` varchar(100) DEFAULT NULL,
                `Narration` varchar(100) DEFAULT NULL,
                `creditAmount` varchar(100) DEFAULT NULL,
                `debitAmount` varchar(100) DEFAULT NULL,
                `Journalnumber` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `Status` varchar(400) DEFAULT NULL,
                `jsondata` longtext,
                `remark` varchar(400) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        insertion_consolidate(db_name,"consolidate_hotelogix_syncmanualjournal")
    else:
        print("consolidate_hotelogix_syncmanualjournal already exists")
        # insertion_consolidate(db_name,"consolidate_hotelogix_syncmanualjournal")



def migrate_shopify(db_name):
    print("enter in function ")
    conn=m.connector.connect(host="localhost",password="root",user="root",database=db_name)

    cur=conn.cursor()

    # create first table hotellogix_commfailedrecord
    cur.execute("show tables like 'shopify_shopify'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shopify_shopify` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `token` varchar(100) DEFAULT NULL,
                `storename` varchar(100) DEFAULT NULL,
                `gstin` varchar(100) DEFAULT NULL,
                `transaction1` varchar(100) DEFAULT NULL,
                `storecode` varchar(100) DEFAULT NULL,
                `branch` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `lastsync` varchar(100) DEFAULT NULL,
                `datetime1` varchar(100) DEFAULT NULL,
                `ccode` varchar(100) DEFAULT NULL,
                `ccodepre` varchar(100) DEFAULT NULL,
                `stage` varchar(100) DEFAULT NULL,
                `gst_rates` varchar(100) DEFAULT NULL,
                `manage_attribute` varchar(100) DEFAULT NULL,
                `gst_param` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `suspense` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")

    else:
        print("Shopify_Shopify table already exists")
    
    # create second table shopify Customer 
    cur.execute("show tables like 'shopify_customer'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shopify_customer` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `code` varchar(100) DEFAULT NULL,
                `customer_name` varchar(100) DEFAULT NULL,
                `state` varchar(100) DEFAULT NULL,
                `batch` varchar(100) DEFAULT NULL,
                `mobile` varchar(100) DEFAULT NULL,
                `email` varchar(100) DEFAULT NULL,
                `status` varchar(100) DEFAULT NULL,
                `remark` varchar(500) DEFAULT NULL,
                `module_type` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `storecode` varchar(100) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
    else:
        print("Shopify_Customer table already exists")

    # create third table shopify Sales 
    cur.execute("show tables like 'shopify_sales'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shopify_sales` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `invoice_no` varchar(100) DEFAULT NULL,
                `customer_name` varchar(100) DEFAULT NULL,
                `amount` varchar(100) DEFAULT NULL,
                `date` varchar(100) DEFAULT NULL,
                `status` varchar(100) DEFAULT NULL,
                `remark` varchar(500) DEFAULT NULL,
                `batch` varchar(100) DEFAULT NULL,
                `module_type` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `storecode` varchar(100) DEFAULT NULL,
                `postjson` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
        # insertion_hotelogix(db_name,"hotellogix_depositfailedrecord")
    else:
        print("Shopify_Sales Table already exists")
        # insertion_hotelogix(db_name,"hotellogix_depositfailedrecord")

    # create fourth table hotellogix_depositrecord
    cur.execute("show tables like 'shopify_sales_order'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shopify_sales_order` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `so_no` varchar(100) DEFAULT NULL,
                `customer_name` varchar(100) DEFAULT NULL,
                `so_amount` varchar(100) DEFAULT NULL,
                `so_date` varchar(100) DEFAULT NULL,
                `status` varchar(100) DEFAULT NULL,
                `remark` varchar(500) DEFAULT NULL,
                `batch` varchar(100) DEFAULT NULL,
                `module_type` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `storecode` varchar(100) DEFAULT NULL,
                `postjson` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
    else:
        print("Sales_order table already exists")


    # create fifth table Shopify in Sync
    cur.execute("show tables like 'shopify_sync'")
    if cur.fetchone() is None:
        print("before start creating table")
        cur.execute('''
                CREATE TABLE `shopify_sync` (
                `id` bigint NOT NULL AUTO_INCREMENT,
                `batch` varchar(100) DEFAULT NULL,
                `module_type` varchar(100) DEFAULT NULL,
                `date` varchar(100) DEFAULT NULL,
                `status` varchar(100) DEFAULT NULL,
                `total_record` varchar(500) DEFAULT NULL,
                `success_record` varchar(100) DEFAULT NULL,
                `fail_record` varchar(100) DEFAULT NULL,
                `compid` varchar(100) DEFAULT NULL,
                `storecode` varchar(100) DEFAULT NULL,
                `recordjson` json NOT NULL DEFAULT (_utf8mb3'"No Data Found"'),
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                )
        ''')
        print("after start creating table")
    else:
        print("Shopify_Sync table already exists")





# All Insert values start Plugin wise 
def insertion_hotelogix(db_name,table_name):
    # Database connection parameters
    source_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin2',
    }

    destination_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': db_name,
    }

    tracker_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin_trackerid',
    }

    try:
        # Connect to the source database
        source_connection = m.connect(**source_db_config)
        source_cursor = source_connection.cursor()

        # Connect to the destination database
        destination_connection = m.connect(**destination_db_config)
        destination_cursor = destination_connection.cursor()

        # Connect to the tracker database
        tracker_connection = m.connect(**tracker_db_config)
        tracker_cursor = tracker_connection.cursor()


        tracker_cursor.execute("select company_id,db_name from tracker_id_hotelogix")
        for i in tracker_cursor.fetchall():
            if i[1] == db_name:
                print(i[0])
                source_cursor.execute(f"select * from `{table_name}` where companyid = %s",(i[0],))
                for row in source_cursor.fetchall():
                    print(row)
                    # Fetch the column names for the specified table
                    source_cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in source_cursor.fetchall()]
                    # Construct the SQL query dynamically
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                    # Execute the query with the provided values
                    destination_cursor.execute(query, row)
                    print("teri behen ka kutta kaatu")
                    destination_connection.commit()
                    print("data tranfer successfully")

    except m.Error as err:
        print(f"Error: {err}")

    finally:
        # Close database connections and cursors
        source_cursor.close()
        source_connection.close()
        destination_cursor.close()
        destination_connection.close()


def insertion_shiprocket(db_name,table_name):
    # Database connection parameters
    source_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin2',
    }

    destination_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': db_name,
    }

    tracker_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin_trackerid',
    }

    try:
        # Connect to the source database
        source_connection = m.connect(**source_db_config)
        source_cursor = source_connection.cursor()

        # Connect to the destination database
        destination_connection = m.connect(**destination_db_config)
        destination_cursor = destination_connection.cursor()

        # Connect to the tracker database
        tracker_connection = m.connect(**tracker_db_config)
        tracker_cursor = tracker_connection.cursor()


        tracker_cursor.execute("select company_id,db_name from tracker_id_shiprocket")
        for i in tracker_cursor.fetchall():
            if i[1] == db_name:
                print(i[0])
                source_cursor.execute(f"select * from `{table_name}` where companyid = %s",(i[0],))
                for row in source_cursor.fetchall():
                    print(row)
                    # Fetch the column names for the specified table
                    source_cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in source_cursor.fetchall()]
                    # Construct the SQL query dynamically
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                    # Execute the query with the provided values
                    destination_cursor.execute(query, row)
                    print("teri behen ka kutta kaatu")
                    destination_connection.commit()
                    print("data tranfer successfully")

    except m.Error as err:
        print(f"Error: {err}")

    finally:
        # Close database connections and cursors
        source_cursor.close()
        source_connection.close()
        destination_cursor.close()
        destination_connection.close()


def insertion_consolidate(db_name,table_name):
    # Database connection parameters
    source_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin2',
    }

    destination_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': db_name,
    }

    tracker_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin_trackerid',
    }

    try:
        # Connect to the source database
        source_connection = m.connect(**source_db_config)
        source_cursor = source_connection.cursor()

        # Connect to the destination database
        destination_connection = m.connect(**destination_db_config)
        destination_cursor = destination_connection.cursor()

        # Connect to the tracker database
        tracker_connection = m.connect(**tracker_db_config)
        tracker_cursor = tracker_connection.cursor()


        tracker_cursor.execute("select company_id,db_name from tracker_id_consolidate_hotelogix")
        for i in tracker_cursor.fetchall():
            if i[1] == db_name:
                print(i[0])
                if table_name == "consolidate_hotelogix_hotellogixlogin":
                    source_cursor.execute(f"select * from `{table_name}` where companyid = %s",(i[0],))
                else:
                    source_cursor.execute(f"select * from `{table_name}` where compid = %s",(i[0],))
                for row in source_cursor.fetchall():
                    print(row)
                    # Fetch the column names for the specified table
                    source_cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in source_cursor.fetchall()]
                    # Construct the SQL query dynamically
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                    # Execute the query with the provided values
                    destination_cursor.execute(query, row)
                    print("teri behen ka kutta kaatu")
                    destination_connection.commit()
                    print("data tranfer successfully")

    except m.Error as err:
        print(f"Error: {err}")

    finally:
        # Close database connections and cursors
        source_cursor.close()
        source_connection.close()
        destination_cursor.close()
        destination_connection.close()


def insertion_shopify(db_name,table_name):
    # Database connection parameters
    source_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin2',
    }

    destination_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': db_name,
    }

    tracker_db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hbplugin_trackerid',
    }

    try:
        # Connect to the source database
        source_connection = m.connect(**source_db_config)
        source_cursor = source_connection.cursor()

        # Connect to the destination database
        destination_connection = m.connect(**destination_db_config)
        destination_cursor = destination_connection.cursor()

        # Connect to the tracker database
        tracker_connection = m.connect(**tracker_db_config)
        tracker_cursor = tracker_connection.cursor()


        tracker_cursor.execute("select company_id,db_name from tracker_id_shopify")
        for i in tracker_cursor.fetchall():
            if i[1] == db_name:
                print(i[0])
                # if table_name == "Shopify_login":
                #     source_cursor.execute(f"select * from `{table_name}` where companyid = %s",(i[0],))
                # else:
                #     source_cursor.execute(f"select * from `{table_name}` where compid = %s",(i[0],))
                source_cursor.execute(f"select * from `{table_name}` where compid = %s",(i[0],))
                for row in source_cursor.fetchall():
                    print(row)
                    # Fetch the column names for the specified table
                    source_cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in source_cursor.fetchall()]
                    # Construct the SQL query dynamically
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                    # Execute the query with the provided values
                    destination_cursor.execute(query, row)
                    destination_connection.commit()
                    print("data tranfer successfully")

    except m.Error as err:
        print(f"Error: {err}")

    finally:
        # Close database connections and cursors
        source_cursor.close()
        source_connection.close()
        destination_cursor.close()
        destination_connection.close()






if __name__ == '__main__':

    conn=m.connect(host="localhost",password="root",user="root",database="hbplugin2")
    cur=conn.cursor()
    cur.execute("SHOW TABLES ")

    for x in cur.fetchall():
        try:
            # print("start")
            cur.execute("show databases like 'hbplugin_trackerid'")
            if cur.fetchone() is None:
                print("in")
                cur.execute("create database hbplugin_trackerid")
                cur.execute("use hbplugin_trackerid")

            else:
                # print("hbplugin_trackerid database already exists")
                cur.execute("use hbplugin_trackerid")

            # Hotelogix tables created
            if "hotellogix_hotellogixlogin" == x[0]:
                print("Hotelogix tables created started ...")
                cur.execute("show tables like 'tracker_id_hotelogix'")
                if cur.fetchone() is None:
                    cur.execute('''
                                    CREATE TABLE tracker_id_hotelogix (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    company_id VARCHAR(500),
                                    db_name VARCHAR(250),
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

                    # for hbplugin database access
                    cur.execute("use hbplugin2")
                    cur.execute(f"SELECT DISTINCT companyid FROM hotellogix_hotellogixlogin")
                    for compid in cur.fetchall():
                        cur.execute("use hbplugin_trackerid")
                        company_id=compid[0]
                        db_name="db_"+company_id[len(company_id)-5:]
                        print("kalash is here")
                        insert_query = "INSERT INTO tracker_id_hotelogix (company_id, db_name) VALUES (%s, %s)"
                        # Execute the query with the variables
                        cur.execute(insert_query, (company_id, db_name))
                        conn.commit()
                        print("insert successfully")
                        cur.execute(f"show databases like '{db_name}'")
                        if cur.fetchone() is None:
                            cur.execute(f"create database {db_name}")
                            # migrate_hotelogix(db_name)
                        else:
                            print("DB already exists")
                            # migrate_hotelogix(db_name)
                        print("create database successfully")                    
                else:
                    print("tracker_id_hotelogix is already exists")

            # Shiprocket tables Created 
            elif "shiprocket_shiprocketlogin" == x[0]:
                print("Ship rocket tables created...")
                cur.execute("show tables like 'tracker_id_shiprocket'")
                if cur.fetchone() is None:
                    cur.execute('''
                                    CREATE TABLE tracker_id_shiprocket (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    company_id VARCHAR(500),
                                    db_name VARCHAR(250),
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

                    # for hbplugin database access
                    cur.execute("use hbplugin2")
                    cur.execute(f"SELECT DISTINCT companyid FROM shiprocket_shiprocketlogin")
                    for compid in cur.fetchall():
                        cur.execute("use hbplugin_trackerid")
                        company_id=compid[0]
                        db_name="db_"+company_id[len(company_id)-5:]
                        insert_query = "INSERT INTO tracker_id_shiprocket (company_id, db_name) VALUES (%s, %s)"

                        # Execute the query with the variables
                        cur.execute(insert_query, (company_id, db_name))
                        conn.commit()
                        print("insert successfully")
                        cur.execute(f"show databases like '{db_name}'")
                        if cur.fetchone() is None:
                            cur.execute(f"create database {db_name}")
                            # migrate_shiprocket(db_name)
                        else:
                            print("DB already exists")
                            # migrate_shiprocket(db_name)
                        print("create database successfully")
                    
                else:
                    print("tracker_id_shiprocket is already exists")

            # Shopify tables created
            elif "shopify_shopify" == x[0]:
                print("Shopify tables created started ....")
                cur.execute("show tables like 'tracker_id_shopify'")
                if cur.fetchone() is None:
                    cur.execute('''
                                    CREATE TABLE tracker_id_shopify (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    company_id VARCHAR(500),
                                    db_name VARCHAR(250),
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

                    # for hbplugin database access
                    cur.execute("use hbplugin2")
                    cur.execute(f"SELECT DISTINCT compid FROM shopify_shopify")
                    for compid in cur.fetchall():
                        cur.execute("use hbplugin_trackerid")
                        company_id=compid[0]
                        db_name="db_"+company_id[len(company_id)-5:]
                        insert_query = "INSERT INTO tracker_id_shopify (company_id, db_name) VALUES (%s, %s)"
                        # Execute the query with the variables
                        cur.execute(insert_query, (company_id, db_name))
                        conn.commit()
                        print("insert successfully")
                        cur.execute(f"show databases like '{db_name}'")
                        if cur.fetchone() is None:
                            cur.execute(f"create database {db_name}")
                            # migrate_shopify(db_name)
                        else:
                            print("DB already exists")
                            # migrate_shopify(db_name)
                        print("create database successfully")
                else:
                    print("tracker_id_shopify is already exists")

            # Consolidation tables created
            elif "consolidate_hotelogix_hotellogixlogin" == x[0]:
                print("Consolidation tables created Started ....")
                cur.execute("show tables like 'tracker_id_consolidate_hotelogix'")
                if cur.fetchone() is None:
                    cur.execute('''
                                    CREATE TABLE tracker_id_consolidate_hotelogix (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    company_id VARCHAR(500),
                                    db_name VARCHAR(250),
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')

                    # for hbplugin database access
                    cur.execute("use hbplugin2")
                    cur.execute(f"SELECT DISTINCT companyid FROM consolidate_hotelogix_hotellogixlogin")
                    for compid in cur.fetchall():
                        cur.execute("use hbplugin_trackerid")
                        company_id=compid[0]
                        db_name="db_"+company_id[len(company_id)-5:]
                        insert_query = "INSERT INTO tracker_id_consolidate_hotelogix (company_id, db_name) VALUES (%s, %s)"

                        # Execute the query with the variables
                        cur.execute(insert_query, (company_id, db_name))
                        conn.commit()
                        print("insert successfully")
                        cur.execute(f"show databases like '{db_name}'")
                        if cur.fetchone() is None:
                            cur.execute(f"create database {db_name}")
                            # migrate_consolidate(db_name)
                        else:
                            print("DB already exists")
                            # migrate_consolidate(db_name)
                        print("create database successfully")                    
                else:
                    print("tracker_id_consolidate_hotelogix is already exists")               
        except:
            # print(x[0]+ " have no data")
            pass