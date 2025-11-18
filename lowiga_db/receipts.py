import pandas as pd
import sqlite3

# 1. Cargás los excels
df_receipts = pd.read_excel("Excels/ReceiptOrder1.xlsx")
df_status = pd.read_excel("Excels/Status.xlsx")
df_users = pd.read_excel("Excels/User1.xlsx")
df_type = pd.read_excel("Excels/Type.xlsx")
df_client = pd.read_excel("Excels/Client1.xlsx")

# 2. Conectar a SQLite (crea un archivo .db si no existe)
conn = sqlite3.connect("mydb.db")

# 3. Subir los excels como tablas a SQLite
df_receipts.to_sql("ReceiptOrder1", conn, if_exists="replace", index=False)
df_status.to_sql("Status", conn, if_exists="replace", index=False)
df_users.to_sql("User1", conn, if_exists="replace", index=False)
df_type.to_sql("Type", conn, if_exists="replace", index=False)
df_client.to_sql("Client1", conn, if_exists="replace", index=False)

# 4. Ejecutar consulta SQL para status
query_status = """
SELECT
    r.RO_Status,
    i.id
FROM ReceiptOrder1 r
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
LEFT JOIN User1 u
    ON r.Entered_By = u.username;
"""

df_users = pd.read_sql_query(query_users, conn)

#Query: type
query_type = """
SELECT
    r."RO _Type",
    i.id
FROM ReceiptOrder1 r
RIGHT JOIN Type i
    ON r."RO _Type" = i.description;
"""

df_type = pd.read_sql_query(query_type, conn)

#query: client

query_client = """
SELECT
    r.Client,
    c.Code AS client_id
FROM ReceiptOrder1 r
LEFT JOIN Client1 c
    ON r.Client = c.Description;
"""

df_client = pd.read_sql_query(query_client, conn)


# 6. Mostrar resultados
print(result)
print(df_users)
print(df_type)
print(df_client)

