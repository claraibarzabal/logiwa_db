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

df_client['id'] = df_client.index + 1
df_status['id'] = df_status.index + 1
df_receipts['id'] = df_receipts.index + 1
df_item['id'] = df_item.index + 1


df_receipts = df_receipts.merge(
    df_client[['Description', 'id']],
    left_on='Client',      # receipts column
    right_on='Description',  # clients column
    how='left'
).rename(columns={'id_y': 'client_id'})

df_receipts = df_receipts.merge(
    df_status[['status_name', 'id']],
    left_on='RO Status',      # receipts column
    right_on='status_name',  # status column
    how='left'
).rename(columns={'id': 'status_id'})

df_receipts = df_receipts.merge(
    df_type[['description', 'id']],
    left_on='RO Type',      # receipts column
    right_on='description',  # type column
    how='left'
).rename(columns={'id': 'type_id'})

df_receipts = df_receipts.merge(
    df_users[['Email', 'id']],
    left_on='Entered By',      # receipts column
    right_on='Email',  # users column
    how='left'
).rename(columns={'id': 'user_id'})

df_receipts['Date Completed'] = pd.to_datetime(df_receipts['Date Completed'], errors='coerce', dayfirst=False)

df_receipts = df_receipts[
    ['Receipt Order # (RO)', 'Date Completed', 'client_id', 'status_id', 'type_id', 'user_id', 'id_x']
]

df_receipts = df_receipts.rename(columns={
    'Receipt Order # (RO)': 'receipt_order',
    'Date Completed': 'date_completed',
    'id_x': 'id'
})

df_compare_receipt = df_compare_receipt.merge(
    df_client[['Description', 'id']],
    left_on='Client',      # compare receipts column
    right_on='Description',  # client column
    how='left'
).rename(columns={'id': 'client_id'})

df_compare_receipt = df_compare_receipt.merge(
    df_receipts[['receipt_order', 'id']],
    left_on='Receipt Order',      # compare receipts column
    right_on='receipt_order',  # receipt column
    how='left'
).rename(columns={'id': 'receipt_id'})

df_compare_receipt = df_compare_receipt.dropna(subset=['receipt_id'])
df_compare_receipt['receipt_id'] = df_compare_receipt['receipt_id'].astype('Int64')

df_compare_receipt = df_compare_receipt.merge(
    df_item[['SKU', 'id']],
    left_on='Item Code',      # compare receipts column
    right_on='SKU',  # item column
    how='left'
).rename(columns={'id': 'item_id'})

df_compare_receipt = df_compare_receipt.dropna(subset=['item_id'])
df_compare_receipt['item_id'] = df_compare_receipt['item_id'].astype('Int64')

df_compare_receipt = df_compare_receipt.merge(
    df_status[['status_name', 'id']],
    left_on='Status',      # compare receipts column
    right_on='status_name',  # status column
    how='left'
).rename(columns={'id': 'status_id'})

df_compare_receipt['Receipt Quantity'] = df_compare_receipt['Receipt Quantity'].astype('Int64')
df_compare_receipt['Receipt Difference'] = df_compare_receipt['Receipt Difference'].astype('Int64')

df_compare_receipt = df_compare_receipt[
    ['receipt_id', 'client_id', 'status_id', 'item_id', 'Receipt Quantity', 'Receipt Difference', 'Receipt Order Quantity', 'Difference']
]

df_compare_receipt = df_compare_receipt.rename(columns={
    'Receipt Quantity': 'receipt_quantity',
    'Receipt Difference': 'receipt_difference',
    'Receipt Order Quantity': 'receipt_order_quantity', 
    'Difference': 'difference'
})

df_compare_receipt['id'] = df_compare_receipt.index + 1

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

print('Client', df_client.columns)
print('Status', df_status.columns)
print('Item', df_item.columns)  
print('CompareReceipt', df_compare_receipt.columns)
print('ReceiptOrder', df_receipts.columns)

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

