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

files = [
    "Excels/ReceiptReport1.xlsx",
    "Excels/ReceiptReport2.xlsx",
    "Excels/ReceiptReport3.xlsx"
]

# Leer y concatenar
df_receipt_report = pd.concat([pd.read_excel(f) for f in files], ignore_index=True)

df_client['id'] = df_client.index + 1
df_status['id'] = df_status.index + 1
df_receipts['id'] = df_receipts.index + 1
df_item['id'] = df_item.index + 1
df_receipt_report['id'] = df_receipt_report.index + 1
df_compare_receipt['id'] = df_compare_receipt.index + 1

df_receipts = df_receipts.rename(columns={
    "Client": "client",
    "Receipt Order # (RO)": "receipt_order_ro",
    "Client Receipt No": "client_receipt_no",
    "Planned Arrival Date": "planned_arrival_date",
    "RO Type": "ro_type",
    "RO Status": "ro_status",
    "Date Completed": "date_completed",
    "Entered By": "entered_by",
    "Notes": "notes",
    'id_x': 'id'
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

df_users = df_users.rename(columns={
    "username": "username",
    "description": "description",
    "Email": "email",
    "Active": "active",
    "Client_User": "client_user",
    "API_User": "api_user",
    "id": "id"
})

df_client = df_client.rename(columns={
    "Code": "code",
    "Description": "description",
    "Tax Code": "tax_code",
    "Tax Office": "tax_office",
    "Packing Type Selection Algorithm": "packing_type_selection_algorithm",
    "Issue Single Order For Packing": "issue_single_order_for_packing",
    "Company": "company"
})

df_item = df_item.rename(columns={
    "CLIENT": "client",
    "SKU": "sku",
    "DESCRIPTION": "description",
    "BARCODE": "barcode",
    "SALESUNITPRICE": "sales_unit_price",
    "ITEMMASTERWEIGHT": "item_master_weight"
})

cols = [
    "Client",
    "Status",
    "Date Received",
    "PO / Receipt Order #",
    "SKU",
    "Pallet/Tote (LP)",
    "Location",
    "Return",
    "Quantity (Unit)",
    "Entered By"
]

df_receipt_report = df_receipt_report[cols]

df_receipt_report = df_receipt_report.rename(columns={
    "Client": "client",
    "Status": "status",
    "Date Received": "date_received",
    "PO / Receipt Order #": "po_receipt_order",
    "SKU": "sku",
    "Pallet/Tote (LP)": "pallet_tote_lp",
    "Location": "location",
    "Return": "return",
    "Quantity (Unit)": "quantity_unit",
    "Entered By": "entered_by"
})

df_receipts = df_receipts.merge(
    df_client[['description', 'id']],
    left_on='client',      # receipts column
    right_on='description',  # clients column
    how='left'
).rename(columns={'id_y': 'client_id'})

df_receipts = df_receipts.merge(
    df_status[['status_name', 'id']],
    left_on='ro_status',      # receipts column
    right_on='status_name',  # status column
    how='left'
).rename(columns={'id': 'status_id'})

df_receipts = df_receipts.merge(
    df_type[['description', 'id']],
    left_on='ro_type',      # receipts column
    right_on='description',  # type column
    how='left'
).rename(columns={'id': 'type_id'})

df_receipts = df_receipts.merge(
    df_users[['email', 'id']],
    left_on='entered_by',      # receipts column
    right_on='email',  # users column
    how='left'
).rename(columns={'id': 'user_id'})

df_receipts['date_completed'] = pd.to_datetime(df_receipts['date_completed'], errors='coerce', dayfirst=False)

df_receipts = df_receipts[
    ['receipt_order_ro', 'date_completed', 'client_id', 'status_id', 'type_id', 'user_id', 'id_x']
]

df_compare_receipt = df_compare_receipt.merge(
    df_receipts[['receipt_order', 'id']],
    left_on='receipt_order',      # compare receipts column
    right_on='receipt_order',  # receipt column
    how='left'
).rename(columns={'id': 'receipt_id'})

df_compare_receipt = df_compare_receipt.dropna(subset=['receipt_id'])
df_compare_receipt['receipt_id'] = df_compare_receipt['receipt_id'].astype('Int64')

df_compare_receipt = df_compare_receipt.merge(
    df_item[['sku', 'id']],
    left_on='item_code',      # compare receipts column
    right_on='sku',  # item column
    how='left'
).rename(columns={'id': 'item_id'})

df_compare_receipt = df_compare_receipt.dropna(subset=['item_id'])
df_compare_receipt['item_id'] = df_compare_receipt['item_id'].astype('Int64')

df_compare_receipt['receipt_quantity'] = df_compare_receipt['receipt_quantity'].astype('Int64')
df_compare_receipt['receipt_difference'] = df_compare_receipt['receipt_difference'].astype('Int64')

df_compare_receipt = df_compare_receipt[
    ['receipt_id', 'client_id', 'status_id', 'item_id', 'receipt_quantity', 'receipt_difference', 'receipt_order_quantity', 'difference']
]

df_receipt_report = df_receipt_report.merge(
    df_receipts[['receipt_order', 'id']],
    left_on='po_receipt_order',      # compare receipts column
    right_on='receipt_order',  # receipt column
    how='left'
).rename(columns={'id': 'receipt_id'})

df_receipt_report = df_receipt_report.merge(
    df_item[['sku', 'id']],
    left_on='sku',      # compare receipts column
    right_on='sku',  # item column
    how='left'
).rename(columns={'id': 'item_id'})

# 2. Conectar a SQLite (crea un archivo .db si no existe)
conn = sqlite3.connect("mydb.db")

# 3. Subir los excels como tablas a SQLite
df_receipts.to_sql("ReceiptOrder", conn, if_exists="replace", index=False)
df_status.to_sql("Status", conn, if_exists="replace", index=False)
df_users.to_sql("User", conn, if_exists="replace", index=False)
df_type.to_sql("Type", conn, if_exists="replace", index=False)
df_client.to_sql("Client", conn, if_exists="replace", index=False)
df_item.to_sql("Item", conn, if_exists="replace", index=False)
df_compare_receipt.to_sql("CompareReceipt", conn, if_exists="replace", index=False)
df_receipt_report.to_sql("ReceiptReport", conn, if_exists="replace", index=False)

# 4. Ejecutar consulta SQL para status
query_status = """
SELECT 
    r.id,
    r.receipt_order,
    r.date_completed,
    c.Description AS client_name,
    s.status_name,
    t.description AS type_name,
    u.description AS entered_by
FROM ReceiptOrder r
LEFT JOIN Client c ON r.client_id = c.id
LEFT JOIN Status s ON r.status_id = s.id
LEFT JOIN Type t ON r.type_id = t.id
LEFT JOIN User u ON r.user_id = u.id
LIMIT 5;
"""

result = pd.read_sql_query(query_status, conn)
print(result)

query_status2 = """
SELECT 
    rc.id,
    r.receipt_order,
    r.date_completed,
    c.Description AS client_name,
    s.status_name,
    i.SKU AS item_sku
FROM CompareReceipt rc
LEFT JOIN Client c ON rc.client_id = c.id
LEFT JOIN Status s ON rc.status_id = s.id
LEFT JOIN Item i ON rc.item_id = i.id
LEFT JOIN ReceiptOrder r ON rc.receipt_id = r.id
LIMIT 5;
"""

result2 = pd.read_sql_query(query_status2, conn)
print(result2)


# # QUERY: usuarios
# query_users = """
# SELECT
#     r.*,
#     u.id AS user_id
# FROM ReceiptOrder1 r
# LEFT JOIN User u
#     ON r.Entered_By = u.username;
# """

# df_users = pd.read_sql_query(query_users, conn)

# #Query: type
# query_type = """
# SELECT
#     r."RO _Type",
#     i.id
# FROM ReceiptOrder r
# RIGHT JOIN Type i
#     ON r."RO _Type" = i.description;
# """

# df_type = pd.read_sql_query(query_type, conn)

# #query: client

# query_client = """
# SELECT
#     r.Client,
#     c.Code AS client_id
# FROM ReceiptOrder r
# LEFT JOIN Client1 c
#     ON r.Client = c.Description;
# """

# df_client = pd.read_sql_query(query_client, conn)


# # 6. Mostrar resultados
# print(result)
# print(df_users)
# print(df_type)
# print(df_client)





