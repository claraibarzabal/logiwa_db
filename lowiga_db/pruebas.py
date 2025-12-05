import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(BASE_DIR, "Excels_Old")

# 1. Cargás los excels
df_receipts = pd.read_excel(os.path.join(EXCEL_DIR, "ReceiptOrder1.xlsx"))
df_compare_receipt = pd.read_excel(os.path.join(EXCEL_DIR, "CompareReceipt1.xlsx"))
df_status = pd.read_excel(os.path.join(EXCEL_DIR, "Status.xlsx"))
df_type = pd.read_excel(os.path.join(EXCEL_DIR, "Type.xlsx"))
df_users = pd.read_excel(os.path.join(EXCEL_DIR, "User1.xlsx"))
df_client = pd.read_excel(os.path.join(EXCEL_DIR, "Client1.xlsx"))
df_item = pd.read_excel(os.path.join(EXCEL_DIR, "Items.xlsx"))

df_receipts['id'] = df_receipts.index + 1
df_item['id'] = df_item.index + 1

df_receipts = df_receipts.rename(columns={
    "Client_id": "client_id",
    "Status_id": "status_id",
    "Type_id": "type_id",
    "User_id": "user_id",
    "Receipt_Order# (RO)": "receipt_order_ro",
    "Formatted_date": "formatted_date",
    'id': 'id'
})

df_compare_receipt = df_compare_receipt.rename(columns={
    "Warehouse": "warehouse",
    "Client": "client",
    "Vendor": "vendor",
    "Receipt Order": "receipt_order",
    "Item Code": "item_code",
    "Item": "item",
    "Barcode": "barcode",
    "Package Type": "package_type",
    "Receipt Order Quantity": "receipt_order_quantity",
    "Receipt Quantity": "receipt_quantity",
    "Receipt Difference": "receipt_difference",
    "Difference": "difference",
    "Status": "status"
})

df_item = df_item.rename(columns={
    "CLIENT": "client",
    "SKU": "sku",
    "DESCRIPTION": "description",
    "BARCODE": "barcode",
    "SALESUNITPRICE": "sales_unit_price",
    "ITEMMASTERWEIGHT": "item_master_weight"
})

df_compare_receipt = df_compare_receipt.merge(
    df_receipts[['receipt_order_ro', 'id']],
    left_on='receipt_order',      # compare receipts column
    right_on='receipt_order_ro',  # receipt column
    how='left'
).rename(columns={'id': 'receipt_id'})

df_compare_receipt = df_compare_receipt.dropna(subset=['receipt_id'])
df_compare_receipt['receipt_id'] = df_compare_receipt['receipt_id'].astype('Int64')

df_compare_receipt = df_compare_receipt.merge(
    df_item[['id', 'sku', 'barcode']],
    on='barcode',
    how='left'
).rename(columns={'id': 'item_id'})

#df_compare_receipt = df_compare_receipt.merge(
#    df_item[['sku', 'barcode','id']],
#    left_on='barcode',      # compare receipts column
#    right_on='barcode',  # item column
#    how='left'
#).rename(columns={'id': 'item_id'})

#---------------------------------------------------------------
print(df_compare_receipt.columns.tolist())
print(df_compare_receipt.head())
print(df_item.columns.tolist())
#---------------------------------------------------------------
df_compare_receipt = df_compare_receipt.dropna(subset=['item_id'])
df_compare_receipt['item_id'] = df_compare_receipt['item_id'].astype('Int64')

df_compare_receipt['receipt_quantity'] = df_compare_receipt['receipt_quantity'].astype('Int64')
df_compare_receipt['receipt_difference'] = df_compare_receipt['receipt_difference'].astype('Int64')

df_compare_receipt = df_compare_receipt[
    ['receipt_id', 'client_id', 'status_id', 'item_id', 'receipt_quantity', 'receipt_difference', 'receipt_order_quantity', 'difference']
]