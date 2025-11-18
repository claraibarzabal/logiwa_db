import pandas as pd
import sqlite3

# 1. Cargás los excels
df_receipts = pd.read_excel("Excels/ReceiptOrder1.xlsx")
df_status = pd.read_excel("Excels/Status.xlsx")

# 2. Conectar a SQLite (crea un archivo .db si no existe)
conn = sqlite3.connect("mydb.db")

# 3. Subir los excels como tablas a SQLite
df_receipts.to_sql("ReceiptOrder1", conn, if_exists="replace", index=False)
df_status.to_sql("Status", conn, if_exists="replace", index=False)

# 4. Ejecutar consulta SQL
query = """
SELECT
    r.RO_Status,
    i.id
FROM ReceiptOrder1 r
RIGHT JOIN Status i
    ON r.RO_Status = i.description;
"""

result = pd.read_sql_query(query, conn)

# 6. Mostrar resultados
print(result)

