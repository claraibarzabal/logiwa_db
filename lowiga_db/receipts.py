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

receipt_files = [
    os.path.join(EXCEL_DIR, "ReceiptReport1.xlsx"),
    os.path.join(EXCEL_DIR, "ReceiptReport2.xlsx"),
    os.path.join(EXCEL_DIR, "ReceiptReport3.xlsx")
]

# Leer y concatenar
df_receipt_report = pd.concat([pd.read_excel(f) for f in receipt_files], ignore_index=True)
df_shipment_order = pd.read_excel(os.path.join(EXCEL_DIR, "ShipmentOrder1.xlsx"))
shipment_files = [
    os.path.join(EXCEL_DIR, "ShipmentReportAll1.xlsx"),
    os.path.join(EXCEL_DIR, "ShipmentReportAll2.xlsx")
]

shipment_report_all = pd.concat( [pd.read_excel(f) for f in shipment_files], ignore_index=True)

order_files = [
    os.path.join(EXCEL_DIR, "ShipmentOrderDetailStatusReport1.xlsx"),
    os.path.join(EXCEL_DIR, "ShipmentOrderDetailStatusReport2.xlsx")
]
df_order_details = pd.concat( [pd.read_excel(f) for f in order_files], ignore_index=True)

df_client['id'] = df_client.index + 1
df_status['id'] = df_status.index + 1
df_receipts['id'] = df_receipts.index + 1
df_item['id'] = df_item.index + 1
df_receipt_report['id'] = df_receipt_report.index + 1
df_compare_receipt['id'] = df_compare_receipt.index + 1
df_shipment_order['id'] = df_shipment_order.index + 1
df_order_details['id'] = df_order_details.index + 1

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
    "Pallet/Tote (LP)": "box",
    "Location": "location",
    "Return": "return",
    "Quantity (Unit)": "receipt_qty",
    "Entered By": "entered_by"
})

df_shipment_order = df_shipment_order.rename(columns={
    "Client": "client",
    "Logiwa Order #": "logiwa_order",
    "Customer": "customer",
    "Customer Order #": "customer_order",
    "Back Order #": "back_order",
    "Order Status": "order_status",
    "Operation Status": "operation_status",
    "Order Type": "order_type",
    "Nof Products": "nof_products",
    "Open Date": "open_date",
    "Channel Order Code": "channel_order_code",
    "Cancel Date": "close_date",
    "Actual Shipment Date": "actual_shipment_date",
    "Carrier Tracking Number": "carrier_tracking_number",
    "Document": "document",
    "Instructions": "instructions",
    "Carrier": "carrier",
    "Shipment Method": "shipment_method",
    "Store Name": "store_name",
    "Actual Delivery Date": "actual_delivery_date",
    "Notes": "notes",
    "Entered By": "entered_by",
    "FBA Status ID": "fba_status_id"
})

rename_to_orders = {
    "client": "client_id",
    "nof_products": "units",
    "actual_shipment_date": "shipment_date",
    "carrier_tracking_number": "tracking_number",
    "shipment_method": "shipping_method"
}

df_shipment_order = df_shipment_order.rename(columns=rename_to_orders)

import re

def to_snake(name):
    name = name.strip()
    name = re.sub(r'[^0-9a-zA-Z]+', '_', name)   # reemplaza espacios y símbolos por _
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)  # separa camelCase
    return name.lower()

shipment_report_all.columns = [to_snake(c) for c in shipment_report_all.columns]

rename_cols = {
    "order_date": "order_date",
    "carrier_rate": "carrier_rate",
    "total_shipping_rate": "total_rate",
    "state": "state",
    "city": "city",
    "zipcode": "zip_code",
    "weight": "weight",
    "width": "width",
    "length": "length",
    "height": "height"
}

shipment_report_all = shipment_report_all.rename(columns=rename_cols)

df_order_details = df_order_details.rename(columns={
    "Ordered Qty (Unit)": "ordered_qty",
    "Open Qty (Unit)": "open_qty",
    "Allocated Qty (Unit)": "allocated_qty",
    "Picked Qty (Unit)": "picked_qty",
    "Packed Qty (Unit)": "packed_qty",
    "Shipped Qty (Unit)": "shipped_qty",
    "Cancelled Qty (Unit)": "cancelled_qty"
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

df_receipt_report_consolidado = (
    df_receipt_report
    .groupby(["po_receipt_order", "sku"], as_index=False)
    .agg({
        "receipt_qty": "sum",          # sumar unidades
        "client": "first",
        "status": "first",
        "date_received": "first",
        "box": "first",
        "location": "first",
        "return": "first",
        "entered_by": "first"
    })
)
df_receipt_report_consolidado["id"] = df_receipt_report_consolidado.index + 1

cols_to_add = [
    "order_date",
    "carrier_rate",
    "total_rate",
    "state",
    "city",
    "zip_code",
    "weight",
    "width",
    "length",
    "height"
]

shipment_report_all_order = shipment_report_all[["customer_order"] + cols_to_add]

df_shipment_order = df_shipment_order.merge(
    shipment_report_all_order,
    on="customer_order",
    how="left"
)
# ---

df_shipment_order = df_shipment_order.merge(
    df_status,
    on="id",
    how="left"
)

df_shipment_order = df_shipment_order.merge(
    df_type,
    on="id",
    how="left"
)

df_shipment_order['open_date'] = pd.to_datetime(df_shipment_order['open_date'], errors='coerce', dayfirst=False)
df_shipment_order['close_date'] = pd.to_datetime(df_shipment_order['close_date'], errors='coerce', dayfirst=False)
df_shipment_order['actual_shipment_date'] = pd.to_datetime(df_shipment_order['actual_shipment_date'], errors='coerce', dayfirst=False)

cols_keep = [
    "order_id",
    "item_id",
    "ordered_qty",
    "open_qty",
    "allocated_qty",
    "picked_qty",
    "packed_qty",
    "shipped_qty",
    "cancelled_qty"
]

df_order_details = df_order_details[cols_keep]

df_order_details = df_order_details.merge(
    df_shipment_order[
        ["customer_order", "client", "order_status", "logiwa_order",
         "order_date", "actual_shipment_date"]
    ],
    on="customer_order",
    how="left"
)

df_order_details = df_order_details.rename(columns={"logiwa_order": "order_id"})

df_order_details = df_order_details.merge(
    df_item[["id", "sku", "description"]],  # columnas que queremos traer
    left_on="item_id",   # df_order_details.item_id = SKU
    right_on="sku",       # df_item.sku
    how="left"
)

df_order_details = df_order_details.rename(columns={"id": "item_id"})


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
df_shipment_order.to_sql("ShipmentOrder", conn, if_exists="replace", index=False)
shipment_report_all.to_sql("ShipmentReportAll", conn, if_exists="replace", index=False)
shipment_report_all_order.to_sql("ShipmentReportAllOrder", conn, if_exists="replace", index=False)

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





