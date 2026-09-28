import csv
import os

base_dir = os.path.expanduser("~/ATHARV KOCHAREKAR/mariadb")
sql_file_path = os.path.join(base_dir, "shopping-db.sql")

tables = {
    "Customers": os.path.join(base_dir, "customers-100.csv"),
    "Organisations": os.path.join(base_dir, "organizations-100.csv"),
    "People": os.path.join(base_dir, "people-100.csv"),
    "Products": os.path.join(base_dir, "products-100.csv"),
}

def escape_sql_value(val):
    if val is None or val.strip() == "":
        return "NULL"
    # Escape single quotes for valid SQL syntax
    escaped_val = val.replace("'", "''")
    return f"'{escaped_val}'"

with open(sql_file_path, "a", encoding="utf-8") as sql_file:
    sql_file.write("\n-- =============================================\n")
    sql_file.write("-- Clear Old Records & Insert 100 New CSV Records\n")
    sql_file.write("-- =============================================\n\n")

    for table_name, csv_path in tables.items():
        if not os.path.exists(csv_path):
            print(f"Skipping {csv_path} (File not found)")
            continue

        # 1. Clear old records from the table
        sql_file.write(f"TRUNCATE TABLE `{table_name}`;\n")

        # 2. Append all 100 individual INSERT INTO statements
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row

            for row in reader:
                if not row:
                    continue
                formatted_values = [escape_sql_value(val) for val in row]
                values_str = ", ".join(formatted_values)
                
                sql_statement = f"INSERT INTO `{table_name}` VALUES ({values_str});\n"
                sql_file.write(sql_statement)
                
        sql_file.write("\n")

print("Added TRUNCATE statements and 100 INSERT queries per table successfully.")