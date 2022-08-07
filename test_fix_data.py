__author__ = "Gamer239"
__copyright__ = "Copyright (C) 2022 Gamer239"
__license__ = "General Public Licence v2"
__version__ = "1.0"

import pytest, importlib
fix_data = importlib.import_module("fix-data")

def get_basic_row():
    #define a basic row of valid data
    row = {
        'Practitioner': 'PractFirst PractLast', 
        'ContactName': '', 'EmailAddress': '', 
        'InvoiceNumber': 'CCLIENT-20220731-01', 
        'InvoiceDate': '07/31/2022', 
        'DueDate': '07/31/2022', 
        'Total': '', 
        'AmountDue': '', 
        'AmountPaid': 0.0, 
        'PaymentDate': '', 
        'Description': '', 
        'Notes': '', 
        'Quantity': '', 
        'UnitAmount': '', 
        'Discount': '', 
        'AccountCode': '', 
        'TaxDescription': '', 
        'TaxAmount': '', 
        'WriteOff': '', 
        'Currency': '', 
        'PaymentStatus': '', 
        'PaymentSource': '', 
        'TotalRefund': '', 
        'RefundSources': '', 
        'RefundDates': '', 
        'Fees': '', 
        'LineItemDescription': '* Supplement Company Supplement', 
        'LineItemAmount': '7.00', 
        'LineItemQuantity': '1', 
        'LineItemDiscount': '0.00', 
        'LineItemTaxDescription': '', 
        'LineItemTaxAmount': '0.00', 
        'LineItemSubTotal': '97.00', 
        'LineItemProfit': None
        }
    return row

def get_basic_filters():
    filters = [
        {
        'Supplement Name': 'Supplement', 
        'Supplement Company': 'Supplement Company', 
        'Variant Price': '68.37', 
        "Supplement's Cost to the Business": '40.94', 
        'Supplement Fee Percent': '0.15%', 
        'filter': '* Supplement Company Supplement'
        }
    ]
    return filters

def get_basic_profit_math():
    profit_math = {
        "cog" : "Supplement's Cost to the Business", 
        "fee" : "Supplement Fee Percent" 
        }
    return profit_math

def test_lineitemprofit():
    row = get_basic_row()
    filters = get_basic_filters()
    profit_math = get_basic_profit_math()
    calc_row = fix_data.compute_lineitemprofit(row, filters, profit_math)
    assert calc_row["LineItemProfit"] == "41.51"
