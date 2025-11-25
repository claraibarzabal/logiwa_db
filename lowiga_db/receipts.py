import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(BASE_DIR, "Excels_Old")

# 1. Cargás los excels
df_receipts = pd.read_excel(os.path.join(EXCEL_DIR, "ReceiptOrder1.xlsx"))
df_status = pd.read_excel(os.path.join(EXCEL_DIR, "Status.xlsx"))
df_type = pd.read_excel(os.path.join(EXCEL_DIR, "Type.xlsx"))
df_users = pd.read_excel(os.path.join(EXCEL_DIR, "User1.xlsx"))
df_client = pd.read_excel(os.path.join(EXCEL_DIR, "Client1.xlsx"))

df_client['id'] = df_client.index + 1
df_receipts['id'] = df_receipts.index + 1
df_status['id'] = df_status.index + 1

df_receipts = df_receipts.merge(
    df_client[['Description', 'id']],
    left_on='Client',      # receipts column
    right_on='Description',  # clients column
    how='left'
).rename(columns={'id_y': 'client_id'})

df_receipts = df_receipts.merge(
    df_status[['description', 'id']],
    left_on='RO Status',      # receipts column
    right_on='description',  # status column
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
    ['Receipt Order # (RO)', 'Date Completed', 'client_id', 'status_id', 'type_id', 'user_id']
]

df_receipts = df_receipts.rename(columns={
    'Receipt Order # (RO)': 'receipt_order',
    'Date Completed': 'date_completed'
})

df_receipts['id'] = df_receipts.index + 1


# 2. Conectar a SQLite (crea un archivo .db si no existe)
conn = sqlite3.connect("mydb.db")

# 3. Subir los excels como tablas a SQLite
df_receipts.to_sql("ReceiptOrder", conn, if_exists="replace", index=False)
df_status.to_sql("Status", conn, if_exists="replace", index=False)
df_users.to_sql("User", conn, if_exists="replace", index=False)
df_type.to_sql("Type", conn, if_exists="replace", index=False)
df_client.to_sql("Client", conn, if_exists="replace", index=False)


# 4. Ejecutar consulta SQL para status
query_status = """
SELECT
    r.RO_Status,
    i.id
FROM ReceiptOrder r
RIGHT JOIN Status i
    ON r.RO_Status = i.description;
"""

result = pd.read_sql_query(query_status, conn)

# QUERY: usuarios
query_users = """
SELECT
    r.*,
    u.id AS user_id
FROM ReceiptOrder1 r
LEFT JOIN User u
    ON r.Entered_By = u.username;
"""

df_users = pd.read_sql_query(query_users, conn)

#Query: type
query_type = """
SELECT
    r."RO _Type",
    i.id
FROM ReceiptOrder r
RIGHT JOIN Type i
    ON r."RO _Type" = i.description;
"""

df_type = pd.read_sql_query(query_type, conn)

#query: client

query_client = """
SELECT
    r.Client,
    c.Code AS client_id
FROM ReceiptOrder r
LEFT JOIN Client1 c
    ON r.Client = c.Description;
"""

df_client = pd.read_sql_query(query_client, conn)


# 6. Mostrar resultados
print(result)
print(df_users)
print(df_type)
print(df_client)

