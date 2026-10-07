import os
import pandas as pd
import pymysql

# Get the directory where import_data.py is saved
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'leads-100.csv')

# Read CSV using the dynamic absolute path
df = pd.read_csv(csv_path)

# Replace NaN/NAT with None for SQL NULLs
df = df.where(pd.notnull(df), None)

# Connect to custom MariaDB socket
socket_path = os.path.expanduser('~/.local/mariadb/data/mariadb.sock')
conn = pymysql.connect(
    user='atharvmscds',
    unix_socket=socket_path,
    db='app',
    autocommit=True
)

cursor = conn.cursor()

# Prepare parameterized SQL query
sql = """
INSERT INTO Leads (
    `Index`, `Account Id`, `Lead Owner`, `First Name`, `Last Name`,
    `Company`, `Phone 1`, `Phone 2`, `Email 1`, `Email 2`,
    `Website`, `Source`, `Deal Stage`, `Notes`
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE `First Name` = VALUES(`First Name`);
"""

# Convert DataFrame rows into a list of tuples
records = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Execute bulk insert
cursor.executemany(sql, records)

print("Data imported successfully!")
cursor.close()
conn.close()


# import os
# import pymysql

# socket_path = os.path.expanduser('~/.local/mariadb/data/mariadb.sock')
# conn = pymysql.connect(user='atharvmscds', unix_socket=socket_path, db='app')
# cursor = conn.cursor()

# cursor.execute("SELECT COUNT(*), `Lead Owner` FROM Leads GROUP BY `Lead Owner` LIMIT 5;")
# print(cursor.fetchall())

# conn.close()